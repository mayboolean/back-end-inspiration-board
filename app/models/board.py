from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Board(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    # boards can have multiple cards
    cards: Mapped[list["Card"]] = relationship(back_populates="board")

    def to_dict(self):
        '''
        board obj -> dict 
        '''
        board_as_dict = {}
        board_as_dict["id"] = self.id
        board_as_dict["title"] = self.title
        board_as_dict["owner"] = self.owner

        return board_as_dict

    @classmethod
    def from_dict(cls, board_data):
        '''
        request_body (board_data) -> new instance of Board class with info
        '''
        new_board = cls(
            title=board_data["title"],
            owner=board_data["owner"]
        )
        return new_board