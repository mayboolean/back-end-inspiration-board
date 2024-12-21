from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from sqlalchemy import ForeignKey

class Card(db.Model):
    card_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    message: Mapped[str]
    likes_count: Mapped[int]
    board_id: Mapped[int] = mapped_column(ForeignKey('board_id'))
    board: Mapped["Board"] = relationship(back_populates="cards")