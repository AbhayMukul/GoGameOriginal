var gameState,move;

function updateGameState(gameState, move) {
  var newGameState = {...gameState};
  newGameState.board = newGameState.board.apply_move(move);
  newGameState.nextPlayer = newGameState.nextPlayer.other;
  newGameState.previousMove = move;
  return newGameState;
}

// Function to update the board display with the new move
function updateBoardDisplay(move) {
  // Get the element with the ID "board"
  var board = document.getElementById("board");

  // Check if the element exists
  if(board){
    // Get the row and column of the new move
    var row = move.row;
    var col = move.col;

    // Get the color of the stone for the new move
    var color = (move.color == "black") ? "black" : "white";

    // Update the board display to reflect the new move
    board.rows[row].cells[col].style.backgroundColor = color;
  }
}



// making the bot move

// Send an HTTP POST request to the '/make_move' route on the server
async function makeBotMove() {
  // Send an HTTP POST request to the '/make_move' route on the server
  try {
    const response = await fetch('http://127.0.0.1:5000/make_move', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(gameState)
    });

    if (response.ok) {
      // If the request was successful, update the game state and board display with the bot's move
      const moveData = await response.json();
      updateBoardDisplay(moveData);
      gameState = updateGameState(gameState,move);
    } else {
      console.log(`Error: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    console.log(error);
  }
}

setInterval(makeBotMove, 5000);
