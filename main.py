from fastapi import FastAPI
from mysite.api import (category, user, subcategory, product, imageproduct, review, cart,
                        cartitem, fovorite, favoriteitem, auth)
from mysite.admin.setup import setup_admin



hotel_app = FastAPI(title="Widberies FastApi Project")
setup_admin(hotel_app)
hotel_app.include_router(category.category_router)
hotel_app.include_router(user.user_router)
hotel_app.include_router(subcategory.subcategory_router)
hotel_app.include_router(product.product_router)
hotel_app.include_router(imageproduct.imageproduct_router)
hotel_app.include_router(review.review_router)
hotel_app.include_router(cart.cart_router)
hotel_app.include_router(cartitem.cartitem_router)
hotel_app.include_router(fovorite.favorite_router)
hotel_app.include_router(favoriteitem.favoriteitem_router)
hotel_app.include_router(auth.auth_router)
