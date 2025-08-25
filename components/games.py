import streamlit as st
from textwrap import dedent

def render_snake_game():
    html = dedent("""
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          body { margin:0; background:#000; color:#0F0; font-family:monospace; }
          .wrap { display:flex; flex-direction:column; align-items:center; gap:8px; padding:8px; }
          canvas { background:#06080d; display:block; margin:0 auto; box-shadow:0 0 12px rgba(0,255,0,0.2); border:1px solid #2a2f47; border-radius:10px; }
          .bar { text-align:center; padding:6px; color:#8df }
          .title { color:#39ff14 }
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="title">Neon Snake — get score ≥ 10, then type: score X (your actual score)</div>
          <div class="bar">Arrows to move. Eat neon dots.</div>
          <canvas id="c" width="320" height="320"></canvas>
          <div class="bar" id="score">Score: 0</div>
          <div class="bar">Submit your score in the chat: e.g., score 12</div>
        </div>
        <script>
          const c = document.getElementById("c");
          const ctx = c.getContext("2d");
          const grid = 16;
          let count = 0;
          let score = 0;
          let snake = { x: 160, y: 160, dx: grid, dy: 0, cells: [], maxCells: 3 };
          let apple = { x: 160, y: 160 };

          function rand(min, max) { return Math.floor(Math.random() * (max - min)) + min; }
          function resetApple() { apple.x = rand(0, c.width / grid) * grid; apple.y = rand(0, c.height / grid) * grid; }
          resetApple();

          document.addEventListener("keydown", function(e) {
            if (e.key === "ArrowLeft" && snake.dx === 0) { snake.dx = -grid; snake.dy = 0; }
            else if (e.key === "ArrowUp" && snake.dy === 0) { snake.dy = -grid; snake.dx = 0; }
            else if (e.key === "ArrowRight" && snake.dx === 0) { snake.dx = grid; snake.dy = 0; }
            else if (e.key === "ArrowDown" && snake.dy === 0) { snake.dy = grid; snake.dx = 0; }
          });

          function loop() {
            requestAnimationFrame(loop);
            if (++count < 6) return;
            count = 0;

            ctx.clearRect(0, 0, c.width, c.height);

            snake.x += snake.dx;
            snake.y += snake.dy;

            if (snake.x < 0) snake.x = c.width - grid;
            else if (snake.x >= c.width) snake.x = 0;
            if (snake.y < 0) snake.y = c.height - grid;
            else if (snake.y >= c.height) snake.y = 0;

            snake.cells.unshift({x: snake.x, y: snake.y});
            if (snake.cells.length > snake.maxCells) snake.cells.pop();

            // apple
            ctx.fillStyle = "#0F0";
            ctx.fillRect(apple.x, apple.y, grid-1, grid-1);

            // snake
            ctx.fillStyle = "#0a8";
            snake.cells.forEach(function(cell, index) {
              ctx.fillRect(cell.x, cell.y, grid-1, grid-1);

              if (cell.x === apple.x && cell.y === apple.y) {
                snake.maxCells++;
                score++;
                document.getElementById("score").innerText = "Score: " + score;
                resetApple();
              }

              for (let i = index + 1; i < snake.cells.length; i++) {
                if (cell.x === snake.cells[i].x && cell.y === snake.cells[i].y) {
                  snake.x = 160; snake.y = 160;
                  snake.cells = []; snake.maxCells = 3;
                  snake.dx = grid; snake.dy = 0;
                  score = 0;
                  document.getElementById("score").innerText = "Score: 0";
                  resetApple();
                }
              }
            });
          }
          requestAnimationFrame(loop);
        </script>
      </body>
    </html>
    """)
    # Critical: use the HTML component so JS executes
    st.components.v1.html(html, height=440, scrolling=False)



def render_typing_game():
    html = dedent("""
    <html>
      <head>
        <meta charset="utf-8" />
        <style>
          body { margin:0; background:#000; color:#0F0; font-family:monospace; }
          .wrap { max-width: 680px; margin: 0 auto; padding: 10px; }
          .title { color:#39ff14; margin-bottom: 6px; }
          .prompt { background:#06080d; padding:8px; border:1px solid #233; border-radius:8px; margin: 6px 0; }
          input { width: 100%; padding: 10px; background:#0b0f1a; color:#0F0; border:1px solid #233; border-radius:8px; outline:none; }
          .stats { margin-top:6px; color:#8df; }
        </style>
      </head>
      <body>
        <div class="wrap">
          <div class="title">Typing Reflex — reach CPM ≥ 25, then type: score X (your actual CPM)</div>
          <div>Type the phrase below, fast. Press Enter to submit; a new phrase appears.</div>
          <div class="prompt" id="p"></div>
          <input id="i" placeholder="Start typing..." />
          <div class="stats" id="s">CPM: 0 | Correct: 0</div>
          <div class="stats">Submit your best CPM in the chat: e.g., score 30</div>
        </div>
        <script>
          const phrases = [
            "the neon grid hums under rain",
            "ghosts of packets drift in alleys",
            "cipher sparks and static breathes",
            "terminals sing in midnight code",
            "edges hide keys in pale green"
          ];
          let typed = 0;
          let correct = 0;
          let startTime = null;

          function randPhrase() { return phrases[Math.floor(Math.random() * phrases.length)]; }

          const p = document.getElementById("p");
          const i = document.getElementById("i");
          const s = document.getElementById("s");
          let current = randPhrase();
          p.innerText = current;

          i.addEventListener("focus", () => { if (!startTime) startTime = Date.now(); });
          i.addEventListener("keydown", (e) => {
            if (!startTime) startTime = Date.now();
            if (e.key === "Enter") {
              const t = i.value;
              typed += t.length;
              if (t.trim() === current.trim()) correct++;
              current = randPhrase();
              p.innerText = current;
              i.value = "";
              const elapsedMin = Math.max(0.001, (Date.now() - startTime) / 60000.0);
              const cpm = Math.floor(typed / elapsedMin);
              s.innerText = "CPM: " + (isFinite(cpm)? cpm: 0) + " | Correct: " + correct;
            }
          });
        </script>
      </body>
    </html>
    """)
    st.components.v1.html(html, height=300, scrolling=False)

