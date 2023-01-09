var gameState

// Function to update the game state and board display
function updateGame(moveData) {
  // Parse the received JSON data
  var move = JSON.parse(moveData);

  // Update the game state with the new move
  gameState = updateGameState(gameState, move);

  // Update the board display to reflect the new move
  updateBoardDisplay(move);
}


// Function to update the game state with the new move
function updateGameState(gameState, move) {
  // Make a copy of the current game state
  var newGameState = copyGameState(gameState);

  // Update the copy of the game state with the new move
  newGameState = applyMoveToGameState(newGameState, move);

  // Return the updated game state
  return newGameState;
}

// Function to update the board display with the new move
function updateBoardDisplay(move) {
  // Get the row and column of the new move
  var row = move.point.row;
  var col = move.point.col;

  // Get the color of the stone for the new move
  var color = (move.color == "black") ? "black" : "white";

  // Update the board display to reflect the new move
  document.getElementById("board").rows[row].cells[col].style.backgroundColor = color;
}


// Function to make a deep copy of a game state object
function copyGameState(gameState) {
  // Make a deep copy of the game state object using JSON serialization
  return JSON.parse(JSON.stringify(gameState));
}

// Function to apply a move to a game state object
function applyMoveToGameState(gameState, move) {
  // Make a deep copy of the game state
  var newGameState = copyGameState(gameState);

  // Update the copy of the game state with the new move
  newGameState.board = newGameState.board.apply_move(move);
  newGameState.nextPlayer = newGameState.nextPlayer.other;
  newGameState.previousMove = move;

  return newGameState;
}


// making the bot move

// Send an HTTP POST request to the '/make_move' route on the server
function makeBotMove() {
  // Create a new XMLHttpRequest object
  var xhr = new XMLHttpRequest();

  // Set the callback function to handle the server's response
  xhr.onload = function() {
    if (xhr.status == 200) {
      // If the request was successful, update the game state and board display with the bot's move
      updateGame(xhr.responseText);
    }
  };

  // Set the request parameters
  xhr.open('GET', '/make_move', true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  // Send the request to the server, along with the current game state as JSON data
  xhr.send(JSON.stringify(gameState));
}

setInterval(makeBotMove,3000);