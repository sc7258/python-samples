from sqlalchemy.orm import Session
from src.domain import models
from src.application import schemas

# ===============================================
# Member Services
# ===============================================
def add_member(db: Session, member: schemas.MemberCreate) -> models.Member:
    """신규 회원을 등록합니다."""
    db_member = models.Member(name=member.name, email=member.email)
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return db_member

def get_member(db: Session, member_id: int) -> models.Member:
    """ID로 회원을 조회합니다."""
    return db.query(models.Member).filter(models.Member.id == member_id).first()

def get_members(db: Session, skip: int = 0, limit: int = 100):
    """회원 목록을 조회합니다."""
    return db.query(models.Member).offset(skip).limit(limit).all()

# ===============================================
# Item/Book Services
# ===============================================
def add_book(db: Session, book: schemas.BookCreate) -> models.Book:
    """신규 도서를 등록합니다."""
    db_book = models.Book(
        name=book.name,
        price=book.price,
        stock_quantity=book.stock_quantity,
        author=book.author,
        isbn=book.isbn
    )
    if book.category_ids:
        categories = db.query(models.Category).filter(models.Category.id.in_(book.category_ids)).all()
        db_book.categories.extend(categories)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int) -> models.Book:
    """ID로 도서를 조회합니다."""
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """도서 목록을 조회합니다."""
    return db.query(models.Book).offset(skip).limit(limit).all()

# ===============================================
# Order Services
# ===============================================
def place_order(db: Session, order: schemas.OrderCreate) -> models.Order:
    """신규 주문을 생성합니다."""
    member = db.query(models.Member).get(order.member_id)
    if not member:
        raise ValueError("존재하지 않는 회원입니다.")

    order_items_info = []
    for item_data in order.items:
        item = db.query(models.Item).get(item_data.item_id)
        if not item:
            raise ValueError(f"존재하지 않는 상품입니다: id={item_data.item_id}")
        order_items_info.append({"item": item, "count": item_data.count})

    db_order = models.Order.create_order(member, order_items_info)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> models.Order:
    """ID로 주문을 조회합니다."""
    return db.query(models.Order).filter(models.Order.id == order_id).first()

# ===============================================
# Category Services
# ===============================================
def add_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    """신규 카테고리를 등록합니다."""
    db_category = models.Category(name=category.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category
