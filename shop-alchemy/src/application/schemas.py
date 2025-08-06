from pydantic import BaseModel, EmailStr
from typing import List, Optional
import datetime

# ===============================================
# Member Schemas
# ===============================================
class MemberCreate(BaseModel):
    name: str
    email: EmailStr

class Member(BaseModel):
    id: int
    name: str
    email: EmailStr
    created_at: datetime.datetime

    class Config:
        from_attributes = True

# ===============================================
# Item/Book Schemas
# ===============================================
class BookCreate(BaseModel):
    name: str
    price: int
    stock_quantity: int
    author: Optional[str] = None
    isbn: Optional[str] = None
    category_ids: Optional[List[int]] = []

class Book(BaseModel):
    id: int
    name: str
    price: int
    stock_quantity: int
    author: Optional[str] = None
    isbn: Optional[str] = None

    class Config:
        from_attributes = True

# ===============================================
# Order Schemas
# ===============================================
class OrderItemCreate(BaseModel):
    item_id: int
    count: int

class OrderCreate(BaseModel):
    member_id: int
    items: List[OrderItemCreate]

class OrderItem(BaseModel):
    item_id: int
    order_price: int
    count: int

    class Config:
        from_attributes = True

class Order(BaseModel):
    id: int
    member_id: int
    order_date: datetime.datetime
    status: str
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True

# =_=============================================
# Category Schemas
# ===============================================

class CategoryCreate(BaseModel):
    name: str

class Category(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
