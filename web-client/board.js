let canvas, ctx;
let board = [];
let rows = 0, cols = 0;
let cellSize = 40;

function initBoard(r, c) {
    rows = r;
    cols = c;

    canvas = document.getElementById("gameCanvas");
    ctx = canvas.getContext("2d");

    canvas.width = cols * cellSize;
    canvas.height = rows * cellSize;

    canvas.onclick = (e) => {
        const rect = canvas.getBoundingClientRect();
        let x = Math.floor((e.clientX - rect.left) / cellSize);
        let y = Math.floor((e.clientY - rect.top) / cellSize);

        sendMessage({ type: "move", r: y, c: x });
    };
}

function drawBoard() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {

            ctx.strokeStyle = "#555";
            ctx.strokeRect(c * cellSize, r * cellSize, cellSize, cellSize);

            let cell = board[r][c];

            if (cell.count > 0) {
                ctx.fillStyle = getPlayerColor(cell.owner);
                ctx.beginPath();
                ctx.arc(
                    c * cellSize + cellSize/2,
                    r * cellSize + cellSize/2,
                    10 + (cell.count * 4),
                    0,
                    Math.PI * 2
                );
                ctx.fill();
            }
        }
    }
}

function getPlayerColor(pid) {
    const colors = [
        "#ff595e", "#ffca3a", "#8ac926", "#1982c4", "#6a4c93",
        "#e76f51", "#2a9d8f", "#f4a261", "#e9c46a", "#264653"
    ];
    return colors[parseInt(pid.replace("player", "")) % 10];
}

function updateBoard(newBoard) {
    board = newBoard;
    drawBoard();
}
