from fastapi import APIRouter

from app.api import api_login, api_register, api_healthcheck, api_product_group, api_product

router = APIRouter()

router.include_router(api_healthcheck.router, tags=["health-check"], prefix="/healthcheck")
router.include_router(api_login.router, tags=["login"], prefix="/api/login")
router.include_router(api_register.router, tags=["register"], prefix="/api/register")
router.include_router(api_product_group.router, tags=["product_groups"], prefix="/api/product-groups")
router.include_router(api_product.router, tags=["products"], prefix="/api/products")
