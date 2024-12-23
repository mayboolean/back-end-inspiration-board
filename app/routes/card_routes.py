from flask import Blueprint, Response, request
from .. db import db
from .route_utilities import validate_model
from ..models.card import Card

'''
GET /cards
DELETE /cards/<card_id>
PUT /cards/<card_id>/like
'''

bp = Blueprint("cards_bp", __name__, url_prefix="/cards")

@bp.get("")
def get_all_cards():
    '''
    request: None -> list of dict of card objects
    '''
    query = db.select(Card).order_by(Card.id)
    cards = db.session.scalars(query)

    cards_response = []
    for card in cards:
        cards_response.append(card.to_dict())
    return cards_response


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