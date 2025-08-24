from fastapi_sqlalchemy import db
from pydantic.tools import parse_obj_as

from app.models import Product, Solution, Category
from app.models.model_product_group import ProductGroup
from app.schemas.schema import ProductGroupRespObject, UpsertProductGroupReq, GetProductsReq, ProductRespObject, \
    GetProductDetailResp, UpsertProductReq, SolutionObjectResp, GetSolutionDetailResp, UpsertSolutionReq, \
    CategoryObjectResp, UpsertCategoryReq


class Service:
    def get_product_groups(self) -> list[ProductGroupRespObject]:
        product_groups = db.session.query(ProductGroup).all()
        return [parse_obj_as(ProductGroupRespObject, product_group.__dict__) for product_group in product_groups]

    def upsert_product_groups(self, req: UpsertProductGroupReq):
        if req.id is not None:
            product_group = db.session.query(ProductGroup).filter_by(id=req.id).first()
            product_group.name = req.name
            db.session.add(product_group)
            db.session.commit()
        else:
            product_group = ProductGroup(name=req.name)
            db.session.add(product_group)
            db.session.commit()
        return

    def get_products(self, req: GetProductsReq) -> list[ProductRespObject]:
        products = db.session.query(Product).filter(
            Product.child_category_ids.contains(req.child_category_ids),
            Product.product_group_id == req.product_group_id,
        ).all()
        return [parse_obj_as(ProductRespObject, product.__dict__) for product in products]

    def get_product_detail(self, product_id: int) -> GetProductDetailResp:
        product = db.session.query(Product).filter_by(id=product_id).first()
        return parse_obj_as(GetProductDetailResp, product.__dict__)

    def upsert_product(self, req: UpsertProductReq):
        if req.id is not None:
            product = db.session.query(Product).filter_by(id=req.id).first()
            product.name = req.name
            product.comment = req.comment
            product.description = req.description
            product.product_group_id = req.product_group_id
            product.detail_info = req.detail_info
            product.child_category_ids = req.child_category_ids
            product.images = req.images
            db.session.add(product)
            db.session.commit()
        else:
            product = Product()
            product.name = req.name
            product.comment = req.comment
            product.description = req.description
            product.product_group_id = req.product_group_id
            product.detail_info = req.detail_info
            product.child_category_ids = req.child_category_ids
            product.images = req.images
            db.session.add(product)
            db.session.commit()

    def get_solutions(self) -> list[SolutionObjectResp]:
        solutions = db.session.query(Solution).all()
        return [parse_obj_as(SolutionObjectResp, solution.__dict__) for solution in solutions]

    def get_solution_detail(self, solution_id: int) -> GetSolutionDetailResp:
        solution = db.session.query(Solution).filter_by(id=solution_id).first()
        return parse_obj_as(GetSolutionDetailResp, solution)

    def upsert_solution(self, req: UpsertSolutionReq):
        if req.id is not None:
            solution = db.session.query(Solution).filter_by(id=req.id).first()
            solution.name = req.name
            solution.description = req.description
            db.session.add(solution)
            db.session.commit()
        else:
            solution = Solution()
            solution.name = req.name
            solution.description = req.description
            db.session.add(solution)
            db.session.commit()

    def get_categories(self) -> list[CategoryObjectResp]:
        categories = db.session.query(Category).all()
        return [parse_obj_as(CategoryObjectResp, category) for category in categories]

    def upsert_category(self, req: UpsertCategoryReq):
        if req.id is not None:
            category = db.session.query(Category).filter_by(id=req.id).first()
            category.name = req.name
            category.parent_category_id = req.parent_category_id
            db.session.add(category)
            db.session.commit()
        else:
            category = Category()
            category.name = req.name
            category.parent_category_id = req.parent_category_id
            db.session.add(category)
            db.session.commit()
