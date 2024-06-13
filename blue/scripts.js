// scripts.js

const gameId = 1; // This should be dynamically set when creating/joining a game
const player = "player1"; // This should be set based on the current player

const ws = new WebSocket(`ws://localhost:8000/ws/${gameId}`);

ws.onmessage = function(event) {
    const message = event.data;
    console.log(message);
    // Update the game state based on the message
};

async function createGame(players) {
    const response = await fetch('/create_game/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(players)
    });
    const data = await response.json();
    console.log(data);
}

async function takeTurn(action) {
    const response = await fetch(`/take_turn/${gameId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ player, action })
    });
    const data = await response.json();
    console.log(data);
}

// Example of creating a game
createGame(["player1", "player2", "player3", "player4"]);

// Example of taking a turn
takeTurn({ type: 'take_tiles', tiles: ['blue', 'red'] });
