let socket = null;
let roomId = null;
let playerId = null;

function connectWebSocket(room, player) {
    roomId = room;
    playerId = player;

    socket = new WebSocket(`ws://localhost:8000/ws/${room}/${player}`);

    socket.onopen = () => console.log("Connected to server");

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleServerMessage(data);
    };

    socket.onclose = () => alert("Disconnected from server");
}

function sendMessage(msg) {
    socket.send(JSON.stringify(msg));
}
