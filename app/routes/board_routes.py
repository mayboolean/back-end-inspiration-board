from flask import Blueprint, request, abort, make_response
from ..db import db
from app.models.board import Board
from ..models.card import Card
from .route_utilities import validate_model, create_model
import os
import requests
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
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
    return create_model(Board, request_body)

@bp.post("/<board_id>/cards")
def create_card_of_select_board(board_id):
    '''
    request: Card to create, board_id
    create a card of board specified with the board_id
    '''
    board = validate_model(Board, board_id)

    request_body = request.get_json()
    # add board_id (column in Card model)to the req body dict
    request_body["board"] = board
    send_slack_message(request_body)
    print("success posting slack")

    return create_model(Card, request_body)

@bp.get("/<board_id>/cards")
def get_cards_of_select_board(board_id):
    '''
    req: board_id -> response: cards (dict) of selected board
    '''
    board = validate_model(Board, board_id)
    response = [card.to_dict() for card in board.cards]
    return response

def send_slack_message(request_body):
    path = "https://slack.com/api/chat.postMessage"
    token = os.environ.get("SLACK_BOT_TOKEN")
    channel_id = "C086R818Q0G"

    headers = {
        "Authorization": f"Bearer {token}"
    }
    data = {
        "channel": channel_id, 
        "text": f"New dream card: {request_body['message']}"
    }

    response = requests.post(path, headers=headers, json=data)
    logging.info("posting...")

    if response.status_code != 200 or not response.json().get("ok"):
        logging.error(f"Failed to send message to Slack: {response.text}")
    else:
        logging.info("Message posted successfully to Slack")

    return request_body, 200
