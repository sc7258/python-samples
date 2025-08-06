# 데이터베이스 모델 명세

이 문서는 `prd.md`를 기반으로 쇼핑몰 백엔드 서버의 데이터베이스 모델을 상세히 정의한다.

## 1. 전체 모델 관계

*   **회원(Member)** 과 **주문(Order)** 은 `1:N` 관계이다. 한 명의 회원은 여러 주문을 할 수 있다.
*   **주문(Order)** 과 **주문항목(OrderItem)** 은 `1:N` 관계이다. 하나의 주문은 여러 주문항목을 포함한다.
*   **주문항목(OrderItem)** 과 **상품(Item)** 은 `N:1` 관계이다. 여러 주문항목이 하나의 상품을 가리킬 수 있다.
*   **상품(Item)** 과 **카테고리(Category)** 는 `N:M` 관계이다. 하나의 상품은 여러 카테고리에 속할 수 있고, 하나의 카테고리는 여러 상품을 포함할 수 있다. 이를 위해 `item_category` 연결 테이블을 사용한다.

## 2. 모델별 상세 명세

### 2.1. Member (회원)

회원 정보를 저장하는 테이블.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| id | Integer | Primary Key, Auto Increment | 회원 고유 식별자 |
| name | String(50) | Not Null | 회원 이름 |
| email | String(120) | Not Null, Unique | 회원 이메일 (로그인 ID로 사용 가능) |
| created_at | DateTime | Not Null, Default: current_timestamp | 가입일 |

### 2.2. Item (상품)

모든 상품의 공통 정보를 저장하는 테이블. 단일 테이블 상속 전략을 사용하여 `Book`과 같은 하위 타입을 구분한다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| id | Integer | Primary Key, Auto Increment | 상품 고유 식별자 |
| name | String(100) | Not Null | 상품명 |
| price | Integer | Not Null | 상품 가격 |
| stock_quantity | Integer | Not Null, Default: 0 | 재고 수량 |
| item_type | String(50) | Not Null | 상품 타입 (예: 'book') |

### 2.3. Book (도서)

`Item` 테이블을 상속받아 도서 상품의 추가 정보를 저장한다. 실제로는 `Item` 테이블 내에 컬럼으로 존재한다.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| author | String(50) | Nullable | 저자 |
| isbn | String(20) | Nullable | 국제 표준 도서 번호 |

### 2.4. Order (주문)

회원의 주문 정보를 저장하는 테이블.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| id | Integer | Primary Key, Auto Increment | 주문 고유 식별자 |
| member_id | Integer | Foreign Key (Member.id), Not Null | 주문한 회원의 ID |
| order_date | DateTime | Not Null, Default: current_timestamp | 주문일 |
| status | String(20) | Not Null, Default: 'ORDERED' | 주문 상태 (예: ORDERED, CANCELED) |

### 2.5. OrderItem (주문 항목)

각 주문에 포함된 상품의 정보를 저장하는 테이블.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| id | Integer | Primary Key, Auto Increment | 주문 항목 고유 식별자 |
| order_id | Integer | Foreign Key (Order.id), Not Null | 주문 ID |
| item_id | Integer | Foreign Key (Item.id), Not Null | 주문된 상품 ID |
| order_price | Integer | Not Null | 주문 당시 상품 가격 |
| count | Integer | Not Null | 주문 수량 |

### 2.6. Category (카테고리)

상품을 분류하기 위한 카테고리 정보를 저장하는 테이블.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| id | Integer | Primary Key, Auto Increment | 카테고리 고유 식별자 |
| name | String(50) | Not Null, Unique | 카테고리명 |

### 2.7. item_category (상품-카테고리 연결 테이블)

`Item`과 `Category`의 `N:M` 관계를 위한 연결 테이블.

| 컬럼명 | 데이터 타입 | 제약 조건 | 설명 |
| --- | --- | --- | --- |
| item_id | Integer | Primary Key, Foreign Key (Item.id) | 상품 ID |
| category_id | Integer | Primary Key, Foreign Key (Category.id) | 카테고리 ID |
