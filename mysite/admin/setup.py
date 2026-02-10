from .view import CategoryAdmin, UserProfileAdmin, ProductAdmin, SubCategoryAdmin
from sqladmin import Admin
from fastapi import FastAPI
from mysite.db.database import engine


def setup_admin(app:FastAPI):
    admin = Admin(app, engine)
    admin.add_view(UserProfileAdmin)
    admin.add_view(CategoryAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(SubCategoryAdmin)


