from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey

class Card(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]
    board_id: Mapped[int] = mapped_column(ForeignKey('board.id'))
    board: Mapped["Board"] = relationship(back_populates="cards")

    def to_dict(self):
        '''
        instance of card -> dict
        '''
        card_as_dict = {}
        card_as_dict["message"] = self.message
        card_as_dict["likes_count"] = self.likes_count
        card_as_dict["board_id"] = self.board_id
        
        return card_as_dict


    @classmethod
    def from_dict(cls, request_body):
        '''
        dict (req body) -> instance of cls (Card in this case)
        '''
        new_card = cls(
            message=request_body["message"],
            likes_count=request_body["likes_count"],
            board_id=request_body["board_id"]
        )
        return new_card