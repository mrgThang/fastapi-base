import json

from fastapi_sqlalchemy import db
from pydantic.tools import parse_obj_as
from sqlalchemy import func

from app.models import Product, Solution, Category
from app.models.model_product_group import ProductGroup
from app.schemas.schema import ProductGroupRespObject, UpsertProductGroupReq, GetProductsReq, ProductRespObject, \
    GetProductDetailResp, UpsertProductReq, SolutionObjectResp, GetSolutionDetailResp, UpsertSolutionReq, \
    CategoryObjectResp, UpsertCategoryReq, GetCategoriesReq


class Service:
    def get_product_groups(self) -> list[ProductGroupRespObject]:
        product_groups = db.session.query(ProductGroup).filter(ProductGroup.is_active != False).all()
        return [parse_obj_as(ProductGroupRespObject, product_group.__dict__) for product_group in product_groups]

    def upsert_product_groups(self, req: UpsertProductGroupReq):
        if req.id is not None:
            product_group = db.session.query(ProductGroup).filter_by(id=req.id).first()
            product_group.name = req.name
            product_group.is_active = req.is_active
            db.session.add(product_group)
            db.session.commit()
        else:
            product_group = db.session.query(ProductGroup).filter_by(name=req.name).first()
            if not product_group:
                product_group = ProductGroup(name=req.name)
            product_group.is_active = True
            db.session.add(product_group)
            db.session.commit()
        return

    def get_products(self, req: GetProductsReq) -> list[ProductRespObject]:
        query = db.session.query(Product).filter(
            Product.product_group_id == req.product_group_id,
            Product.is_active != False,
        )
        if req.child_category_ids and len(req.child_category_ids) > 0:
            query = query.filter(func.json_contains(Product.child_category_ids, json.dumps(req.child_category_ids)) == 1)
        products = query.all()
        products_resp = []
        for product in products:
            products_resp.append(ProductRespObject(
                id=product.id,
                name=product.name,
                image=product.images[0],
                comment=product.comment,
            ))
        return products_resp

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
            product.is_active = req.is_active
            db.session.add(product)
            db.session.commit()
        else:
            product = db.session.query(Product).filter_by(name=req.name).first()
            if product is None:
                product = Product()
            product.is_active = True
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
        solutions = db.session.query(Solution).filter(Solution.is_active != False).all()
        return [parse_obj_as(SolutionObjectResp, solution.__dict__) for solution in solutions]

    def get_solution_detail(self, solution_id: int) -> GetSolutionDetailResp:
        solution = db.session.query(Solution).filter_by(id=solution_id).first()
        return parse_obj_as(GetSolutionDetailResp, solution)

    def upsert_solution(self, req: UpsertSolutionReq):
        if req.id is not None:
            solution = db.session.query(Solution).filter_by(id=req.id).first()
            solution.name = req.name
            solution.description = req.description
            solution.is_active = req.is_active
            db.session.add(solution)
            db.session.commit()
        else:
            solution = db.session.query(Solution).filter_by(name=req.name).first()
            if not solution:
                solution = Solution()
            solution.is_active = True
            solution.name = req.name
            solution.description = req.description
            db.session.add(solution)
            db.session.commit()

    def get_categories(self, req: GetCategoriesReq) -> list[CategoryObjectResp]:
        categories = db.session.query(Category).filter(Category.is_active != False, Category.product_group_id == req.product_group_id).all()
        return [parse_obj_as(CategoryObjectResp, category) for category in categories]

    def upsert_category(self, req: UpsertCategoryReq):
        if req.id is not None:
            category = db.session.query(Category).filter_by(id=req.id).first()
            category.name = req.name
            category.parent_category_id = req.parent_category_id
            category.product_group_id = req.product_group_id
            category.is_active = req.is_active
            db.session.add(category)
            db.session.commit()
        else:
            category = db.session.query(Category).filter_by(name=req.name).first()
            if category is None:
                category = Category()
            category.is_active = True
            category.name = req.name
            category.product_group_id = req.product_group_id
            category.parent_category_id = req.parent_category_id
            db.session.add(category)
            db.session.commit()
