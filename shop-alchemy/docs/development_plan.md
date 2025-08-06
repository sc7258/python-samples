# 개발 작업 계획

이 문서는 `prd.md` 요구사항을 기반으로 백엔드 애플리케e이션을 개발하기 위한 단계별 작업 계획을 정의한다.

## 1단계: 도메인 모델링 (`src/domain/models.py`)

- [ ] 1.1. `Member` 모델 정의 (id, name, email)
- [ ] 1.2. `Item` (Base), `Book` (Child) 모델 정의 (상속 관계)
- [ ] 1.3. `Category` 모델 정의
- [ ] 1.4. `Item`과 `Category` 간의 다대다 관계 설정을 위한 `item_category` 연관 테이블 정의
- [ ] 1.5. `Order` 및 `OrderItem` 모델 정의
- [ ] 1.6. 모델 간의 관계 설정
    - `Member`와 `Order` (1:N)
    - `Order`와 `OrderItem` (1:N)
    - `OrderItem`과 `Item` (N:1)

## 2단계: 인프라스트럭처 설정 (`src/infrastructure/database.py`)

- [ ] 2.1. SQLAlchemy 데이터베이스 엔진 및 세션 설정
- [ ] 2.2. 애플리케이션 실행 시 데이터베이스 및 테이블을 생성하는 초기화 함수 구현

## 3단계: 애플리케이션 서비스 및 스키마 (`src/application/`)

- [ ] 3.1. **스키마 정의 (`schemas.py`)**
    - [ ] `MemberCreate`, `MemberRead` Pydantic 스키마 정의
    - [ ] `BookCreate`, `BookRead` Pydantic 스키마 정의
    - [ ] `OrderCreate`, `OrderRead` Pydantic 스키마 정의
- [ ] 3.2. **서비스 구현 (`services.py`)**
    - [ ] `add_member`: 회원 등록 서비스
    - [ ] `add_book`: 도서 등록 서비스
    - [ ] `place_order`: 주문 생성 및 재고 관리 로직 포함 서비스
    - [ ] `get_member`, `get_book` 등 조회 서비스

## 4단계: 프레젠테이션 (API 엔드포인트) (`src/presentation/main.py`)

- [ ] 4.1. FastAPI 애플리케이션 초기화
- [ ] 4.2. 회원 생성을 위한 API 엔드포인트 구현 (`POST /members`)
- [ ] 4.3. 도서 등록을 위한 API 엔드포인트 구현 (`POST /books`)
- [ ] 4.4. 주문 생성을 위한 API 엔드포인트 구현 (`POST /orders`)
- [ ] 4.5. 데이터 조회를 위한 API 엔드포인트 구현 (예: `GET /members/{member_id}`)

## 5단계: 테스트 (`tests/`)

- [ ] 5.1. `pytest` 및 `httpx` (API 테스트용) 의존성 추가
- [ ] 5.2. 테스트용 데이터베이스 설정
- [ ] 5.3. 각 서비스 및 API 엔드포인트에 대한 단위/통합 테스트 작성

## 6단계: 환경 설정 관리

- [ ] 6.1. `.env` 파일을 사용하여 개발, QA, 운영 환경별 데이터베이스 연결 정보 분리
