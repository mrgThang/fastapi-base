from sqlalchemy import Column, String, Integer, JSON, Text

from app.models.model_base import BareBaseModel


class Product(BareBaseModel):
    name: str = Column(String(255))
    product_group_id: int = Column(Integer)
    comment: str = Column(String(255))
    description: str = Column(Text)
    detail_info: str = Column(Text)
    images: list[str] = Column(JSON)
    child_category_ids: list[int] = Column(JSON)
