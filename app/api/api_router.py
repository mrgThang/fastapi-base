from fastapi import APIRouter

from app.api import api_login, api_healthcheck, api_product_group, api_product, api_solution, \
    api_category, api_file

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_login.router, tags=["login"], prefix="/api/login")
router.include_router(api_product_group.router, tags=["product_groups"], prefix="/api/product-groups")
router.include_router(api_product.router, tags=["products"], prefix="/api/products")
router.include_router(api_solution.router, tags=["solutions"], prefix="/api/solutions")
router.include_router(api_category.router, tags=["categories"], prefix="/api/categories")
router.include_router(api_file.router, tags=["files"], prefix="/api/files")
