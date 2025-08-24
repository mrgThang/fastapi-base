from typing import Optional, TypeVar, Generic
from pydantic.generics import GenericModel

from pydantic import BaseModel
from humps import camelize

T = TypeVar("T")


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = '000'
        self.message = 'Thành công'
        return self


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T):
        self.code = '000'
        self.message = 'Thành công'
        self.data = data
        return self


class MetadataSchema(BaseModel):
    current_page: int
    page_size: int
    total_items: int

def to_camel(string):
    return camelize(string)

class MyFormBaseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        orm_mode = True
        allow_population_by_field_name = True
        use_enum_values = True
