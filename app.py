from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    output = {"game_id": game_id, "board": game.board}

    return jsonify(output)

@app.post("/api/score-word")
def scoring():
    """For existing game, check if word is legal and score it"""
    #need to parse out JSON form-data for game_id and word
    curr_game_id = request.json["game_id"]
    word = request.json["word"]
    curr_game = games[curr_game_id]
   
    if not curr_game.is_word_in_word_list(word):
        return jsonify({"result": "not word"})
    if not curr_game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})
    return jsonify({"result": "ok"})
