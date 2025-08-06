import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.presentation.main import app, get_db
from src.domain.models import Base

# 테스트용 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 테스트용 데이터베이스 의존성 오버라이드
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# 테스트 클라이언트 생성
client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    """테스트마다 데이터베이스를 초기화하는 픽스처"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ===============================================
# Member API Tests
# ===============================================
def test_create_and_read_member(db_session):
    """회원 생성 및 조회 테스트"""
    # 1. 회원 생성
    response = client.post(
        "/members",
        json={"name": "testuser", "email": "test@example.com"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "testuser"
    assert data["email"] == "test@example.com"
    member_id = data["id"]

    # 2. 생성된 회원 조회
    response = client.get(f"/members/{member_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "testuser"
    assert data["email"] == "test@example.com"

def test_read_members(db_session):
    """회원 목록 조회 테스트"""
    # 회원 2명 생성
    client.post("/members", json={"name": "user1", "email": "user1@example.com"})
    client.post("/members", json={"name": "user2", "email": "user2@example.com"})

    response = client.get("/members")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

# ===============================================
# Book API Tests
# ===============================================
def test_create_and_read_book(db_session):
    """도서 생성 및 조회 테스트"""
    # 1. 도서 생성
    response = client.post(
        "/items/books",
        json={
            "name": "Test Book",
            "price": 10000,
            "stock_quantity": 10,
            "author": "Test Author",
            "isbn": "1234567890"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Book"
    book_id = data["id"]

    # 2. 생성된 도서 조회
    response = client.get(f"/items/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Book"

# ===============================================
# Order API Tests
# ===============================================
def test_place_order(db_session):
    """주문 생성 테스트"""
    # 1. 사전 데이터 준비: 회원 및 도서 생성
    member_res = client.post("/members", json={"name": "order_user", "email": "order@example.com"})
    book_res = client.post("/items/books", json={"name": "Order Book", "price": 20000, "stock_quantity": 5})
    member_id = member_res.json()["id"]
    book_id = book_res.json()["id"]

    # 2. 주문 생성
    response = client.post(
        "/orders",
        json={
            "member_id": member_id,
            "items": [{"item_id": book_id, "count": 2}]
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["member_id"] == member_id
    assert len(data["order_items"]) == 1
    assert data["order_items"][0]["item_id"] == book_id

    # 3. 재고 감소 확인
    response = client.get(f"/items/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["stock_quantity"] == 3 # 5 - 2 = 3

def test_place_order_insufficient_stock(db_session):
    """재고 부족 시 주문 실패 테스트"""
    member_res = client.post("/members", json={"name": "stock_user", "email": "stock@example.com"})
    book_res = client.post("/items/books", json={"name": "Stock Book", "price": 100, "stock_quantity": 1})
    member_id = member_res.json()["id"]
    book_id = book_res.json()["id"]

    response = client.post(
        "/orders",
        json={
            "member_id": member_id,
            "items": [{"item_id": book_id, "count": 2}] # 재고(1)보다 많은 수량 주문
        },
    )
    assert response.status_code == 400
    assert "재고가 부족합니다." in response.json()["detail"]
