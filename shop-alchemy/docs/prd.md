# 프로젝트 목표
회원가입을 하고, 상품을 주문하는 쇼핑몰을 위한 백엔드 서버 프로젝트이다.

## 주요기능

- 회원(Member): 회원 등록, 조회
- 상품(Item/Book): 도서 등록, 조회, 재고 관리
- 주문(Order): 회원이 도서를 주문, 주문 항목 관리
- 카테고리(Category): 도서를 카테고리로 분류
 
## 기술스택
- Python 3.x
- SQLAlchemy (ORM)
- SQLite (개발용, 추후 MySQL/MariaDB로 변경 가능)
- (옵션) Flask/FastAPI로 API 구현 가능

# 프로젝트 구조
클린 아키텍처를 적용하여, 프로그램을 개발한다.

## 데이터베이스 및 모델 설계
### 모델

- Member: 회원 정보 (이름, 이메일)
- Item / Book: 상품과 도서 (상속 관계 구현)
- Order / OrderItem: 주문과 주문 항목
- Category: 상품 분류 (다대다 관계)


### 연관관계

- Member ↔ Order: 일대다
- Order ↔ OrderItem: 일대다
- OrderItem ↔ Item: 다대일
- Item ↔ Category: 다대다 (연결 테이블 사용)

### 서비스

- add_member: 회원 등록
- add_book: 도서 등록
- place_order: 주문 생성 및 재고 관리

## API 설계

# 기타
## 테스트
단위 테스트를 추가해 CRUD 기능 검증 (예: pytest)


## 환경설정
dev, qa, prod 환경별로 DB 설정 분리 (예: 환경 변수로 DB URL 관리)