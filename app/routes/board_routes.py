from flask import Blueprint, request, abort, make_response
from ..db import db
from app.models.board import Board
from ..models.card import Card
from .route_utilities import validate_model, create_model
'''
GET /boards
POST /boards
GET /boards/<board_id>/cards
POST /boards/<board_id>/cards
'''

bp = Blueprint("boards_bp", __name__, url_prefix="/boards")

@bp.get("")
def get_all_boards():
    '''
    request: None -> response: json of all boards
    boards (db returns board object) which is turned into list of dict to return
    '''
    query = db.select(Board).order_by(Board.id)
    boards = db.session.scalars(query)

    boards_response = []
    for board in boards:
        boards_response.append(board.to_dict())
    return boards_response

@bp.post("")
def create_board():
    '''
    request: Board object to create -> response: Board obj (dict) and status code
    takes request body, creates Board instance, adds+commits to db
    '''
    request_body = request.get_json()

    try:
        new_board = Board.from_dict(request_body)
    
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_board)
    db.session.commit()

    return new_board.to_dict(), 200

@bp.post("/<board_id>/cards")
def create_card_of_select_board(board_id):
    '''
    request: Card to create, board_id
    create a card of board specified with the board_id
    '''
    board = validate_model(Board, board_id)

    request_body = request.get_json()
    # add board_id (column in Card model)to the req body dict
    request_body["board_id"] = board_id
    return create_model(Card, request_body)
