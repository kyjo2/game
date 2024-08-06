import OnlineGame from "./game.js";

function init() {
  let ws = null;

  const button2P = document.getElementById('2P');
  const button4P = document.getElementById('4P');
  const buttonTournament = document.getElementById('tournament');
  const gameCanvas = document.getElementById('gameCanvas');
  let type = null;

  button2P.addEventListener('click', () => {
    console.log('2P');
    type = '2P';
    ws = new WebSocket(`ws://localhost:8000/ws/rankgames/${type}/`);
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const sock = new WebSocket(`ws://localhost:8000/ws/games/start/${data.game_id}/${type}/`);
      ws.close();
      OnlineGame(sock, type);
      button2P.style.display = 'none';
      button4P.style.display = 'none';
      buttonTournament.style.display = 'none';
      // Make gameCanvas a square based on height
    };
  });

  button4P.addEventListener('click', () => {
    console.log('4P');
    type = '4P';
    ws = new WebSocket(`ws://localhost:8000/ws/rankgames/${type}/`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const sock = new WebSocket(`ws://localhost:8000/ws/games/start/${data.game_id}/${type}/`);
      ws.close();
      OnlineGame(sock, type);
      button2P.style.display = 'none';
      button4P.style.display = 'none';
      buttonTournament.style.display = 'none';

      // Make gameCanvas a square based on height
      const inGame = document.querySelector('.in-game');
      const sideLength = inGame.offsetHeight;
      gameCanvas.style.width = `${sideLength}px`;
      gameCanvas.style.height = `${sideLength}px`;
    };
  });

  buttonTournament.addEventListener('click', () => {
    console.log('토너먼트');
    type = 'tournament';
    ws = new WebSocket(`ws://localhost:8000/ws/rankgames/${type}/`);

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const sock = new WebSocket(`ws://localhost:8000/ws/games/start/${data.game_id}/${type}/`);
      ws.close();
      OnlineGame(sock, type);
      button2P.style.display = 'none';
      button4P.style.display = 'none';
      buttonTournament.style.display = 'none';
    };
  });
}

init();
