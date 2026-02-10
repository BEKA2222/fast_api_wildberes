from pydantic import BaseModel
from mysite.db.models import UserStatus
from datetime import date


class UserProfileShema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int | None
    phone_number: str | None
    profile_image: str | None
    status: UserStatus
    created_at: date
    password: str


class UserProfileRegistrationShema(BaseModel):
    first_name: str
    last_name: str
    username: str
    age: int | None
    phone_number: str | None
    profile_image: str | None
    status: UserStatus
    created_at: date
    password: str



class UserProfileLoginShema(BaseModel):
    username: str
    password: str


class CategoryShema(BaseModel):
    category_name: str


class SubCategoryShema(BaseModel):
    sub_category_name: str
    category_id: int


class ProductShema(BaseModel):
    product_name: str
    description: str
    price: int
    product_image: str
    category_id: int
    sub_category_id: int


class ImageProductShema(BaseModel):
    image: str
    product_id: int


class ReviewShema(BaseModel):
    user_id: int
    product_id: int
    comment: str
    stars: int
    image: str
    video: str


class CartShema(BaseModel):
    user_id: int


class CartItemShema(BaseModel):
    cart_id: int
    product_id: int

class FavoriteShema(BaseModel):
    user_id: int

class FavoriteItemShema(BaseModel):
    favorite_id: int
    product_id: int
    like: bool

