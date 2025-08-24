from sqlalchemy import Column, String, Text

from app.models.model_base import BareBaseModel


class Solution(BareBaseModel):
    name: str = Column(String(255))
    description: str = Column(Text)
