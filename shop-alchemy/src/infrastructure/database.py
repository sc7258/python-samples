from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

# 데이터베이스 연결 URL (개발용 SQLite)
# 실제 프로덕션 환경에서는 환경 변수 등을 통해 관리해야 합니다.
DATABASE_URL = "sqlite:///./shop.db"

# 데이터베이스 엔진 생성
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite 사용 시 필요
    echo=True  # 실행되는 SQL 쿼리를 로그로 출력
)

# 세션 생성
# autocommit=False, autoflush=False로 설정하여 트랜잭션을 명시적으로 관리
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 스레드-로컬 세션
# 웹 애플리케이션의 각 요청마다 별도의 세션을 사용하도록 보장
db_session = scoped_session(SessionLocal)

def get_db():
    """
    FastAPI 등 웹 프레임워크에서 의존성 주입으로 사용할 데이터베이스 세션 제공 함수
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """
    데이터베이스와 테이블을 초기화합니다.
    (애플리케이션 시작 시 한 번만 호출)
    """
    from src.domain.models import Base
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    # 이 파일을 직접 실행하면 데이터베이스가 초기화됩니다.
    print("데이터베이스를 초기화합니다...")
    init_db()
    print("데이터베이스 초기화 완료.")
