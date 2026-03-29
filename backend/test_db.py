from app.database.session import SessionLocal
from app.database.base import User, Product

def test_connection():
    db = SessionLocal()
    try:
        first_user = db.query(User).first()
        print(f"User đầu tiên lấy từ DB: {first_user.Username} - {first_user.FullName}")
        
        product_count = db.query(Product).count()
        print(f"Tổng số sản phẩm trong DB: {product_count}")
        print("KẾT NỐI DATABASE THÀNH CÔNG")
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_connection()