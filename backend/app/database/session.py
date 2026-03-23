from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# 1. Khởi tạo Engine (Động cơ kết nối)
# pool_pre_ping=True giúp tự động kiểm tra xem kết nối có bị rớt không trước khi gửi query
engine = create_engine(
    settings.DATABASE_URL, 
    pool_pre_ping=True,
    echo=False # Đổi thành True nếu bạn muốn nhìn thấy các câu lệnh SQL thuần được in ra terminal
)

# 2. Khởi tạo SessionLocal
# Mỗi lần có request từ Frontend, chúng ta sẽ tạo ra một SessionLocal để làm việc với DB
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Hàm Dependency để tự động mở/đóng kết nối an toàn cho FastAPI sau này
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()