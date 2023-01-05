function makeBotMove() {
    fetch('/make_move', {
      method: 'POST',
      body: JSON.stringify(gameState),
      headers: {
        'Content-Type': 'application/json'
      }
    }).then(response => response.json())
      .then(move => {
        // Find the cell that corresponds to the point where the move was played
        const row = move.point.row;
        const col = move.point.col;
        const cell = document.querySelector(`#row-${row}-col-${col}`);
  
        // Update the cell with the new move
        cell.innerHTML = 'X'; // or 'O' if the move was played by the other player
      });
  }
  
  setInterval(makeBotMove, 2000);