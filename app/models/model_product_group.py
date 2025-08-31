from sqlalchemy import Column, String

from app.models.model_base import BareBaseModel


class ProductGroup(BareBaseModel):
    __tablename__ = "product_group"

    name = Column(String(255))
