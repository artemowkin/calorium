from sqlalchemy.orm import mapped_column, Mapped

from ..project.db import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    height: Mapped[int] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    sex: Mapped[str] = mapped_column(nullable=True)
    activity: Mapped[str] = mapped_column(nullable=True)

