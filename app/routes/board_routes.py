from flask import Blueprint
from app.models.board import Board
from ..db import db
'''
GET /boards
POST /boards
GET /boards/<board_id>/cards
POST /boards/<board_id>/cards
'''

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get("")
def get_all_boards():
    query = db.select(Board).order_by(Board.board_id)
    boards = db.session.scalars(query)

    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    return boards_response