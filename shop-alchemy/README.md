# Shop Alchemy

회원가입 및 상품 주문을 위한 쇼핑몰 백엔드 서버입니다.

## 주요 기술

*   Python 3.x
*   SQLAlchemy (ORM)
*   Poetry (패키지 관리)
*   FastAPI (예정)
*   클린 아키텍처

## 실행 방법

1.  **의존성 설치:**
    ```bash
    poetry install
    ```

2.  **데이터베이스 초기화:**
    ```bash
    poetry run python src/infrastructure/database.py
    ```

3.  **애플리케이션 실행 (예정):**
    ```bash
    poetry run uvicorn src.presentation.main:app --reload
    ```
