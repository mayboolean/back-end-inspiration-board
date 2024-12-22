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

def validate_board_id(board_id):
    try: 
        board_id = int(board_id)
    except:
        response = {"message": f"Board {board_id} invalid."}
        abort(make_response(response, 400))

    query = db.select(Board).where(Board.board_id==board_id)
    board = db.session.scalar(query)
    
    if not board:
        response = {"message": f"Board {board_id} not found."}
        abort(make_response(response, 404))
    return board


@boards_bp.delete("/<board_id>")
def delete_board(board_id):
    board = validate_board_id(board_id)
    db.session.delete(board)
    db.session.commit()

    response_message = f'Board {board.board_id} {board.title} successfully deleted.'
    response_body = {'details': response_message}

    return response_body, 200

@boards_bp.get("/<board_id>")
def get_one_board(board_id):
    board = validate_board_id(board_id)

    return {"board":{
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner}
            }

@boards_bp.put("/<board_id>")
def update_board(board_id):
    board = validate_board_id(board_id)
    request_body = request.get_json()
    title = request_body.get("title")
    owner = request_body.get("owner")

    if title is None or owner is None:
        response = {"details": "Invalid data. 'title' and 'owner' are required."}
        return response, 400

    board.title = title
    board.owner = owner

    db.session.commit()

    response =  {"board":{
        "board_id": board.board_id,
        "title": board.title,
        "owner": board.owner}
            }
    return response, 200










