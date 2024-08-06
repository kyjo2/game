import asyncio
import json
import logging
import uuid
from channels.generic.websocket import AsyncWebsocketConsumer
import redis.asyncio as redis

logger = logging.getLogger('django')

class RankGameRoomConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.game_type = self.scope["url_route"]["kwargs"]["type"]
        self.room_group_name = 'game_queue'
        logger.info("hihi")
        self.redis = redis.from_url('redis://localhost')
        self.game_id = str(uuid.uuid4())  # 고유한 game_id 생성

        # 방 그룹에 추가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name,
        )
        await self.accept()

        await self.increment_and_check_group_size(self.room_group_name)

        logger.info(f'[RANK] 사용자 연결됨: {self.channel_name}, Game ID: {self.game_id}')

    async def disconnect(self, close_code):
        await self.decrement_group_size(self.room_group_name)

        # 방 그룹에서 제거
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

        logger.info(f'[RANK] 사용자 연결 해제됨: {self.channel_name}')

    async def increment_and_check_group_size(self, group_name):
        lua_script = """
        local size = redis.call('INCR', KEYS[1])
        return size
        """
        group_size = await self.redis.eval(lua_script, 1, group_name)
        logger.info(f'[RANK] 사용자 연결됨: {group_size}')
        
        if self.game_type == '2P':
            num = 2
        elif self.game_type == '4P':
            num = 4
        
        if group_size == num:
            try:
                await self.create_game()
            except Exception as e:
                logger.error(f'게임 생성 오류: {e}')

    async def decrement_group_size(self, group_name):
        await self.redis.decr(group_name)

    async def create_game(self):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'data',
                'game_id': self.game_id,
            }
        )

    async def data(self, event):
        await self.send(text_data=json.dumps(event))
