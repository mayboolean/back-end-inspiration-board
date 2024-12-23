from flask import Blueprint, Response, request
from .. db import db
from .route_utilities import validate_model
from ..models.card import Card

'''
DELETE /cards/<card_id>
PUT /cards/<card_id>/like
'''

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.delete("/<card_id>")
def delete_card(card_id):
    '''
    validate id, db delete, return Response(status=204, mimetype="application/json")
    '''
    card = validate_model(Card, card_id)
    db.session.delete(card)
    db.session.commit()

    return Response(status=204, mimetype="application/json")

@bp.put("/<card_id>/like")
def update_likes(card_id):
    '''
    validate card id, take in request body (with likes count), card's like count should update according to req. body, db commit
    return Response(status=204, mimetype="application/json")
    '''    
    card = validate_model(Card, card_id)
    request_body = request.get_json()

    card.likes_count = request_body["likes_count"]
    db.session.commit()
    return Response(status=204, mimetype="application/json")