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

