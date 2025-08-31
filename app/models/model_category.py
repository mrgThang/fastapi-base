from sqlalchemy import Column, String, Integer

from app.models.model_base import BareBaseModel


class Category(BareBaseModel):
    name: str = Column(String(255))
    parent_category_id: int = Column(Integer)
    product_group_id: int = Column(Integer)
