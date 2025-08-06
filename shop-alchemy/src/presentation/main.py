from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.application import schemas, services
from src.infrastructure import database
from src.domain import models

# 데이터베이스 테이블 생성 (애플리케이션 시작 시)
# 이미 init_db()로 생성했지만, 안전을 위해 추가
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(
    title="Shop Alchemy API",
    description="회원가입, 상품 주문을 위한 쇼핑몰 백엔드 API",
    version="1.0.0"
)

# 의존성 주입: 데이터베이스 세션 제공
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ===============================================
# Member Endpoints
# ===============================================
@app.post("/members", response_model=schemas.Member, status_code=201, tags=["Member"])
def create_member(member: schemas.MemberCreate, db: Session = Depends(get_db)):
    """신규 회원 등록"""
    # 이메일 중복 체크
    db_member = db.query(models.Member).filter(models.Member.email == member.email).first()
    if db_member:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    return services.add_member(db, member)

@app.get("/members", response_model=List[schemas.Member], tags=["Member"])
def read_members(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """회원 목록 조회"""
    members = services.get_members(db, skip=skip, limit=limit)
    return members

@app.get("/members/{member_id}", response_model=schemas.Member, tags=["Member"])
def read_member(member_id: int, db: Session = Depends(get_db)):
    """회원 정보 조회"""
    db_member = services.get_member(db, member_id=member_id)
    if db_member is None:
        raise HTTPException(status_code=404, detail="회원을 찾을 수 없습니다.")
    return db_member

# ===============================================
# Item/Book Endpoints
# ===============================================
@app.post("/items/books", response_model=schemas.Book, status_code=201, tags=["Item"])
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """신규 도서 등록"""
    return services.add_book(db, book)

@app.get("/items/books", response_model=List[schemas.Book], tags=["Item"])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """도서 목록 조회"""
    books = services.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/items/books/{book_id}", response_model=schemas.Book, tags=["Item"])
def read_book(book_id: int, db: Session = Depends(get_db)):
    """도서 정보 조회"""
    db_book = services.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="도서를 찾을 수 없습니다.")
    return db_book

# ===============================================
# Order Endpoints
# ===============================================
@app.post("/orders", response_model=schemas.Order, status_code=201, tags=["Order"])
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """신규 주문 생성"""
    try:
        return services.place_order(db, order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/{order_id}", response_model=schemas.Order, tags=["Order"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    """주문 정보 조회"""
    db_order = services.get_order(db, order_id=order_id)
    if db_order is None:
        raise HTTPException(status_code=404, detail="주문을 찾을 수 없습니다.")
    return db_order

# ===============================================
# Category Endpoints
# ===============================================
@app.post("/categories", response_model=schemas.Category, status_code=201, tags=["Category"])
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    """신규 카테고리 등록"""
    return services.add_category(db, category)

@app.get("/categories", response_model=List[schemas.Category], tags=["Category"])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """카테고리 목록 조회"""
    categories = db.query(models.Category).offset(skip).limit(limit).all()
    return categories

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
