from flask import Blueprint, abort, make_response, request, Response
from app.models.board import Board
from app.models.card import Card
from app import db

boards_bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@boards_bp.get("")
def get_all_boards():
    query = db.select(Board)
    boards = db.session.scalars(query)
    boards_response = []
    for board in boards:
        boards_response.append(
            {
                "board_id": board.board_id,
                "title": board.title,
                "owner": board.owner,
            }
        )
    return boards_response, 200
    
@boards_bp.post("")
def create_board():
    try:
        request_body = request.get_json()
    except Exception:
        return {"details": "Invalid request"}, 400

    title = request_body.get("title")
    owner = request_body.get("owner")

    if title is None or owner is None:
        response = {"details": "Invalid data"}
        return response, 400
    
    new_board = Board(title=title, owner=owner)
    db.session.add(new_board)
    db.session.commit()

    response = {
        "board": {
            "board_id":new_board.board_id,
            "title": new_board.title,
            "owner": new_board.owner, }
    }

    return response, 201