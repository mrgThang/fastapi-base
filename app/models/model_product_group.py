from sqlalchemy import Column, String

from app.models.model_base import BareBaseModel


class ProductGroup(BareBaseModel):
    name = Column(String(255))
