from typing import Optional

from app.schemas.sche_base import MyFormBaseModel


class ProductGroupRespObject(MyFormBaseModel):
    id: int
    name: str

class UpsertProductGroupReq(MyFormBaseModel):
    id: Optional[int]
    name: str

class GetProductsReq(MyFormBaseModel):
    child_category_ids: Optional[list[int]]
    product_group_id: int

class ProductRespObject(MyFormBaseModel):
    id: int
    name: str
    image: str
    comment: Optional[str]

class GetProductDetailResp(MyFormBaseModel):
    id: int
    name: str
    images: list[str]
    comment: Optional[str]
    description: Optional[str]
    detail_info: str
    child_category_ids: Optional[list[int]]
    product_group_id: int

class UpsertProductReq(MyFormBaseModel):
    id: Optional[int]
    name: str
    images: list[str]
    comment: Optional[str]
    description: Optional[str]
    detail_info: str
    child_category_ids: Optional[list[int]]
    product_group_id: int

class SolutionObjectResp(MyFormBaseModel):
    id: int
    name: str

class GetSolutionDetailResp(MyFormBaseModel):
    id: int
    name: str
    description: str

class UpsertSolutionReq(MyFormBaseModel):
    id: Optional[int]
    name: str
    description: str

class CategoryObjectResp(MyFormBaseModel):
    id: int
    name: str
    parent_category_id: Optional[int]

class UpsertCategoryReq(MyFormBaseModel):
    id: Optional[int]
    name: str
    parent_category_id: Optional[int]
