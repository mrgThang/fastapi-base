# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  # noqa
from app.models.model_product_group import ProductGroup #noqa
from app.models.model_product import Product #noqa
from app.models.model_category import Category #noqa
from app.models.model_solution import Solution #noqa
