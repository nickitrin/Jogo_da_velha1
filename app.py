from flask import Flask, render_template

app = Flask(__name__)

board = [""] * 9
current_player = "X"  # Primeiro jogador

@app.route("/game_state", methods=["GET"])
def game_state():
    return jsonify({"board": board, "current_player": current_player})

@app.route("/make_move", methods=["POST"])
def make_move():
    global board, current_player

    data = request.json
    position = data.get("position")
    if 0 <= position < 9 and board[position] == "":
            board[position] = current_player
            if check_winner():
                return jsonify({"status": "win", "winner": current_player})
            elif "" not in board:
                return jsonify({"status": "draw"})
            else:
                # Troca de jogador
                current_player = "O" if current_player == "X" else "X"
                return jsonify({"status": "continue", "board": board, "current_player": current_player})
    return jsonify({"status": "invalid"})

def check_winner():
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Colunas
        [0, 4, 8], [2, 4, 6]              # Diagonais
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
            return True
    return False


# Rota para a página inicial
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)