from ..db import db
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Board(db.Model):
    board_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    owner: Mapped[str]
    # boards can have multiple cards
    cards: Mapped[list["Card"]] = relationship(back_populates="board")