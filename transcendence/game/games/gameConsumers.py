import asyncio
import json
import logging
import redis.asyncio as redis
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import PingPongGame

logger = logging.getLogger('django')

class GameConsumer(AsyncWebsocketConsumer):
    class Games:
        pass

    async def connect(self):
        self.player1 = False
        self.player2 = False
        self.player3 = False
        self.player4 = False
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        self.type = self.scope["url_route"]["kwargs"]["type"]
        self.game_group = f'game_{self.game_id}'
        self.my_match = 1
        self.redis = redis.from_url('redis://localhost')
        max = 2 if self.type == '2P' else 4

        await self.channel_layer.group_add(self.game_group, self.channel_name)
        await self.accept()
        group_size = await self._increment_and_get_group_size(self.game_group)

        if group_size == max:
            self.player1 = True
            await self.channel_layer.group_send(
                self.game_group,
                {
                    'type': 'game_start',
                    'game_type': self.type,
                }
            )
        elif group_size == 1:
            self.player2 = True
        elif group_size == 2:
            self.player3 = True
        elif group_size == 3:
            self.player4 = True
        logger.info(self.player1)

    async def receive(self, text_data):
        data = json.loads(text_data)
        type = data.get('type')
        if type == 'start' and self.player1:
            asyncio.create_task(self._game_start(data.get('data', {})))
        elif type == 'keyboard':
            asyncio.create_task(self._accept_key(data.get('data', {})))

    async def disconnect(self, close_code):
        logger.info("User disconnected")
        await self._decrement_group_size(self.game_group)
        await self.channel_layer.group_discard(self.game_group, self.channel_name)
        group_size = await self._get_group_size(self.game_group)
        logger.info(f"Group size after disconnection: {group_size}")

    async def _get_group_size(self, group_name):
        size = await self.redis.get(group_name)
        if size is None:
            return 0
        return int(size)
    
    async def _increment_group_size(self, group_name):
        await self.redis.incr(group_name)

    async def _increment_and_get_group_size(self, group_name):
        lua_script = """
        local size = redis.call('INCR', KEYS[1])
        return size
        """
        group_size = await self.redis.eval(lua_script, 1, group_name)
        return group_size

    async def _decrement_group_size(self, group_name):
        await self.redis.decr(group_name)

    async def _game_start(self, message_data):
        match = await self._make_game_object(message_data)
        if self.type == '2P':
            await self._play_game(match, self.game_group)
        elif self.type == '4P':
            await self._play_game_four(match, self.game_group)

    async def _make_game_object(self, message_data):
        await self._init_object(message_data)
        match = await self._get_object()
        await asyncio.sleep(1)
        return match

    async def _play_game(self, match, group_name):
        while not match.finished:
            await self._update_game(match)
            await self._send_state(match, group_name)
            await asyncio.sleep(0.05)


    async def _accept_key(self, message_data):
        position = None

        match True:
            case self.player1:
                position = 'left'
            case self.player2:
                position = 'right'
            case self.player3:
                position = 'up'
            case self.player4:
                position = 'down'
            case _:
                position = 'undefined'  # 모든 플레이어가 False일 때 기본값
        if position == 'left' or position == 'right':
            await self._move_bar_row(message_data, position)
        if position == 'up' or position == 'down':
            await self._move_bar_col(message_data, position)

    async def _move_bar_row(self, key, position):
        match = await self._get_object()
        player = getattr(match, f'{position}')

        if key == 'up' and player.bar.y >= 0:
            player.bar._up()
        elif key == 'down' and player.bar.y + match.map.height / 4 <= match.map.height:
            player.bar._down()

    async def _move_bar_col(self, key, position):
        match = await self._get_object()
        player = getattr(match, f'{position}')

        if key == 'left' and player.bar.x >= 0:
            player.bar._left()
        elif key == 'right' and player.bar.x + match.map.width / 4 <= match.map.width:
            player.bar._right()

    async def _update_game(self, match):
        match.ball.hit_wall(match.map)
        if match.is_left_win():
            match.plus_score('left_win')
            match.ball.reset(match.map)
        elif match.is_right_win():
            match.plus_score('right_win')
            match.ball.reset(match.map)
        # if match.left.score == 5 or match.right.score == 5:
        #     match.finished = True
        match.ball.move()

    async def _send_state(self, match, group_name):
        data = {
            'type': 'two_player',
            'ball': {
                'x': match.ball.x / match.map.width,
                'y': match.ball.y / match.map.height,
            },
            'left': {
                'x': match.left.bar.x / match.map.width,
                'y': match.left.bar.y / match.map.height,
                'score': match.left.score
            },
            'right': {
                'x': match.right.bar.x / match.map.width,
                'y': match.right.bar.y / match.map.height,
                'score': match.right.score
            }
        }
        logger.info(f"Sending in-game message: {data}")
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'two_player',
                'data': data
            }
        )

    async def _play_game_four(self, match, group_name):
        while not match.finished:
            await self._update_game_four(match)
            await self._send_state_four(match, group_name)
            await asyncio.sleep(0.04)

    async def _update_game_four(self, match):
        if match.is_left_win():
            match.plus_score('left_win')
            match.ball.reset(match.map)
        elif match.is_right_win():
            match.plus_score('right_win')
            match.ball.reset(match.map)
        elif match.is_up_win():
            match.plus_score('up_win')
            match.ball.reset(match.map)
        elif match.is_down_win():
            match.plus_score('down_win')
            match.ball.reset(match.map)
        # if match.left.score + match.up.score == 5 or match.right.score + match.down.score == 5:
        #     match.finished = True
        match.ball.move()

    async def _send_state_four(self, match, group_name):
        data = {
            'type': 'four_player',
            'ball': {
                'x': match.ball.x / match.map.width,
                'y': match.ball.y / match.map.height,
            },
            'left': {
                'x': match.left.bar.x / match.map.width,
                'y': match.left.bar.y / match.map.height,
                'score': match.left.score
            },
            'right': {
                'x': match.right.bar.x / match.map.width,
                'y': match.right.bar.y / match.map.height,
                'score': match.right.score
            },
            'up': {
                'x': match.up.bar.x / match.map.width,
                'y': match.up.bar.y / match.map.height,
                'score': match.up.score
            },
            'down': {
                'x': match.down.bar.x / match.map.width,
                'y': match.down.bar.y / match.map.height,
                'score': match.down.score
            },
        }
        logger.info(f"Sending in-game message: {data}")
        await self.channel_layer.group_send(
            self.game_group,
            {
                'type': 'four_player',
                'data': data
            }
        )

    async def _init_object(self, message_data):
        map_width = message_data['map_width']
        map_height = message_data['map_height']
        setattr(self.Games,
                f'{self.game_group}',
                PingPongGame(map_width, map_height))
        return True

    async def _get_object(self):
        match_object = getattr(self.Games, f'{self.game_group}')
        return match_object

    async def close_connection(self, event):
        self.close()

    async def two_player(self, event):
        await self.send(text_data=json.dumps(event))

    async def four_player(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_end(self, event):
        await self.send(text_data=json.dumps(event))

    async def url(self, event):
        await self.send(text_data=json.dumps(event))

    async def game_start(self, event):
        await self.send(text_data=json.dumps(event))