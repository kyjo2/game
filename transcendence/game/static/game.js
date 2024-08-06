/**
 * @param {HTMLElement} $container
 * @param {Object} info
 * @constructor
 */
export default function OnlineGame(sock, game_type) {
  const $container = document.querySelector('.game-mode');
  const ws = sock;
  let keyState = { up: false, down: false };
  let left, right, up, down, ball, canvas, ctx;

  let keyRepeatTimers = {
    up: null,
    down: null
  };

  ws.onmessage = (event) => {
    console.log('Message received from server:', event.data);
    const data = JSON.parse(event.data);
    if (data.type === "two_player") {
      canvas.width = document.body.clientWidth;
      canvas.height = document.body.clientHeight;
      left.height = canvas.height / 4;
      right.height = canvas.height / 4;
      left.width = canvas.width / 80;
      right.width = canvas.width / 80;
      const gameData = data.data;
      left.x = gameData.left.x * canvas.width;
      left.y = gameData.left.y * canvas.height;
      right.x = gameData.right.x * canvas.width;
      right.y = gameData.right.y * canvas.height;
      ball.x = gameData.ball.x * canvas.width;
      ball.y = gameData.ball.y * canvas.height;
      draw(left, right, ball);
    } else if (data.type === "four_player") {
      console.log('Parsed data:', data);
      canvas.width = document.body.clientWidth;
      canvas.height = document.body.clientHeight;
      left.height = canvas.height / 4;
      right.height = canvas.height / 4;
      left.width = canvas.width / 80;
      right.width = canvas.width / 80;
      up.width = canvas.width / 4;
      down.width = canvas.width / 4;
      up.height = canvas.height / 80;
      down.height = canvas.height / 80;
      const gameData = data.data;
      left.x = gameData.left.x * canvas.width;
      left.y = gameData.left.y * canvas.height;
      right.x = gameData.right.x * canvas.width;
      right.y = gameData.right.y * canvas.height;
      up.x = gameData.up.x * canvas.width;
      up.y = gameData.up.y * canvas.height;
      down.x = gameData.down.x * canvas.width;
      down.y = gameData.down.y * canvas.height;
      ball.x = gameData.ball.x * canvas.width;
      ball.y = gameData.ball.y * canvas.height;
      draw_four(left, right, up, down, ball);
    } else if (data.type === "game_end") {
      endGame(data, ws);
    } else if (data.type === "game_start") {
      startGame(ws);
    }
  };

  // 초기화 함수
  const init = async () => {
    console.log($container);
    console.log('this is game');
    console.log(ws);

    document.addEventListener("keydown", keyDownHandler);
    document.addEventListener("keyup", keyUpHandler);

    window.addEventListener("beforeunload", disconnectWebSocket);
    canvas = $container.querySelector("#gameCanvas");
    ctx = canvas.getContext("2d");
    canvas.width = document.body.clientWidth;
    canvas.height = document.body.clientHeight;
    if (game_type == '4P')
    {
      canvas.width = canvas.height;
      up = { x: canvas.width / 2, y: 0, width: 300, height: 10 };
      down = { x: canvas.width / 2, y: canvas.height - 10, width: 300, height: 10 };
    }
    left = { x: 0, y: canvas.height / 2, width: 10, height: 300 };
    right = { x: canvas.width - 10, y: canvas.height / 2, width: 10, height: 300 };
    ball = { x: canvas.width / 2, y: canvas.height / 2, radius: 10 };
  };

  ws.onopen = () => {
    console.log('WebSocket is connected');
  };

  ws.onerror = (error) => {
    console.error('WebSocket error:', error);
  };

  ws.onclose = (event) => {
      console.log('WebSocket connection closed:', event);
  };

  const disconnectWebSocket = () => {
    if (ws) {
      ws.close();
    }
  };

  const keyDownHandler = (e) => {
    if (e.key === "ArrowUp") {
      if (!keyState.up) {
        keyState.up = true;
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "up" }));
        }
        // 키 반복 타이머 시작
        keyRepeatTimers.up = setInterval(() => {
          if (keyState.up && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "keyboard", data: "up" }));
          }
        }, 100); // 100ms마다 반복
      }
    } else if (e.key === "ArrowDown") {
      if (!keyState.down) {
        keyState.down = true;
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "down" }));
        }
        // 키 반복 타이머 시작
        keyRepeatTimers.down = setInterval(() => {
          if (keyState.down && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "keyboard", data: "down" }));
          }
        }, 100); // 100ms마다 반복
      }
    } else if (e.key === "ArrowLeft") {
      if (!keyState.left) {
        keyState.left = true;
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "left" }));
        }
        // 키 반복 타이머 시작
        keyRepeatTimers.left = setInterval(() => {
          if (keyState.left && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "keyboard", data: "left" }));
          }
        }, 100); // 100ms마다 반복
      }
    } else if (e.key === "ArrowRight") {
      if (!keyState.right) {
        keyState.right = true;
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "right" }));
        }
        // 키 반복 타이머 시작
        keyRepeatTimers.right = setInterval(() => {
          if (keyState.right && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: "keyboard", data: "right" }));
          }
        }, 100); // 100ms마다 반복
      }
    }
  };
  
  // 키가 떼졌을 때 실행되는 핸들러
  const keyUpHandler = (e) => {
    if (e.key === "ArrowUp") {
      if (keyState.up) {
        keyState.up = false;
        clearInterval(keyRepeatTimers.up); // 키 반복 타이머 중지
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "up" }));
        }
      }
    } else if (e.key === "ArrowDown") {
      if (keyState.down) {
        keyState.down = false;
        clearInterval(keyRepeatTimers.down); // 키 반복 타이머 중지
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "down" }));
        }
      }
    } else if (e.key === "ArrowLeft") {
      if (keyState.left) {
        keyState.left = false;
        clearInterval(keyRepeatTimers.left); // 키 반복 타이머 중지
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "left" }));
        }
      }
    } else if (e.key === "ArrowRight") {
      if (keyState.right) {
        keyState.right = false;
        clearInterval(keyRepeatTimers.right); // 키 반복 타이머 중지
        if (ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: "keyboard", data: "right" }));
        }
      }
    }
  };

  function draw(left, right, ball) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#000000";
    ctx.fillRect(left.x, left.y, left.width, left.height);

    ctx.fillStyle = "#000000";
    ctx.fillRect(right.x, right.y, right.width, right.height);

    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2, true);
    ctx.fillStyle = "#000000";
    ctx.fill();
    ctx.strokeStyle = 'black';  // 테두리 색상 설정
    ctx.lineWidth = 5;    // 테두리 두께 설정
    ctx.strokeRect(0, 0, canvas.width, canvas.height);  // 캔버스 테두리 그리기
  }

  function draw_four(left, right, up, down, ball) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = "#000000";
    ctx.fillRect(left.x, left.y, left.width, left.height);

    ctx.fillStyle = "#000000";
    ctx.fillRect(right.x, right.y, right.width, right.height);

    ctx.fillStyle = "#000000";
    ctx.fillRect(up.x, up.y, up.width, up.height);

    ctx.fillStyle = "#000000";
    ctx.fillRect(down.x, down.y, down.width, down.height);

    ctx.beginPath();
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2, true);
    ctx.fillStyle = "#000000";
    ctx.fill();
    ctx.strokeStyle = 'black';  // 테두리 색상 설정
    ctx.lineWidth = 5;    // 테두리 두께 설정
    ctx.strokeRect(0, 0, canvas.width, canvas.height);  // 캔버스 테두리 그리기
  }

  init();

  function startGame(ws) {
    ws.send(
      JSON.stringify({
        type: "start",
        data: {
          map_width: canvas.width,
          map_height: canvas.height,
        },
      }),
    );
    
  }

  function endGame(data, ws) {
    if (ws) {
      ws.close();
    }
  }
}
