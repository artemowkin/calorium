from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import DateTime

from ..auth.models import User
from ..products.models import Product
from ..project.db import Base


class EatingProduct(Base):
    __tablename__ = "eating_products"

    id: Mapped[int] = mapped_column(primary_key=True)
    eating_id: Mapped[int] = mapped_column(ForeignKey("eatings.id"))
    eating: Mapped["Eating"] = relationship(back_populates="products")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product: Mapped[Product] = relationship()
    mass: Mapped[float] = mapped_column()


class Eating(Base):
    __tablename__ = "eatings"

    id: Mapped[int] = mapped_column(primary_key=True)
    timestamp = mapped_column(DateTime(timezone=True), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship()
    products: Mapped[list["EatingProduct"]] = relationship(back_populates="eating", lazy="joined")
