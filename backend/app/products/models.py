from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from ..project.db import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    title_vector = mapped_column(TSVECTOR())
    kkal: Mapped[float] = mapped_column()
    file_url: Mapped[str] = mapped_column(nullable=True)
    owner_id: Mapped[int] = mapped_column(nullable=True)
