const gameBoard = document.getElementById("game-board");
const statusText = document.getElementById("status");

// Inicializa o tabuleiro
function initBoard() {
    fetch("/game_state")
        .then(response => response.json())
        .then(data => {
            gameBoard.innerHTML = "";
            data.board.forEach((cell, index) => {
                const cellDiv = document.createElement("div");
                cellDiv.textContent = cell;
                if (cell !== "") cellDiv.classList.add("taken");
                cellDiv.addEventListener("click", () => makeMove(index));
                gameBoard.appendChild(cellDiv);
            });
            statusText.textContent = `Vez do jogador: ${data.current_player}`;
        });
}

// Faz uma jogada
function makeMove(position) {
    fetch("/make_move", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ position })
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === "win") {
                statusText.textContent = `Jogador ${data.winner} venceu!`;
                gameBoard.innerHTML = ""; // Desabilitar tabuleiro
            } else if (data.status === "draw") {
                statusText.textContent = "Empate!";
            } else if (data.status === "continue") {
                initBoard();
            } else {
                alert("Jogada inválida!");
            }
        });
}

// Inicia o jogo ao carregar
initBoard();
