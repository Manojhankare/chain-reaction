document.getElementById("joinBtn").onclick = () => {
    const room = document.getElementById("roomInput").value;
    const player = document.getElementById("playerInput").value;
    const grid = document.getElementById("gridSelect").value;

    if (!room || !player) {
        alert("Enter room and name");
        return;
    }

    connectWebSocket(room, player);

    sendMessage({
        type: "select_grid",
        grid: grid
    });
};

document.getElementById("startBtn").onclick = () => {
    sendMessage({ type: "start_game" });
};

function handleServerMessage(data) {

    if (data.type === "lobby_update") {
        document.getElementById("playersList").innerHTML =
            "<b>Players:</b><br>" + data.players.join("<br>");
    }

    if (data.type === "game_started") {
        let [rows, cols] = data.grid;

        initBoard(rows, cols);

        document.getElementById("setup-screen").style.display = "none";
        document.getElementById("game-screen").style.display = "block";

        document.getElementById("turnDisplay").innerText =
            "Turn: " + data.turn;
    }

    if (data.type === "board_update") {
        updateBoard(data.board);
        document.getElementById("turnDisplay").innerText =
            "Turn: " + data.turn;
    }

    if (data.type === "game_over") {
        alert("Winner: " + data.winner);
    }
}
