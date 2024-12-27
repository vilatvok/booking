from typing import Annotated
from sqlalchemy.orm import Mapped, DeclarativeBase, mapped_column


class Base(DeclarativeBase):
    id: Mapped[Annotated[int, mapped_column(primary_key=True)]]
