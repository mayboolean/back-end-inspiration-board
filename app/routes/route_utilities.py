from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    '''
    checks if id is a valid integer
    then queries, returns if exists. If not, 404
    '''
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} is invalid"}
        abort(make_response(response, 404))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def create_model(cls, request_body):
    '''
    creates an instance of cls with the request body 
    if missing keys, throws an error
    if not, adds to db, and returns new_models dict rep. and 200
    '''
    try:
        new_model = cls.from_dict(request_body)
    except KeyError as error:
        response = {"message": "Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201

