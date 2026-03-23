from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# 1. Tự động dò tìm đường dẫn tuyệt đối đến thư mục 'backend'
# Cấu trúc: backend/app/core/config.py -> lùi 3 cấp (.parent) sẽ ra thư mục backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

class Settings(BaseSettings):
    # Thông tin cơ bản của Project
    PROJECT_NAME: str = "PhoBERT Sentiment Analysis API"
    API_V1_STR: str = "/api/v1"
    
    # Các biến này sẽ tự động được đọc từ file .env
    DB_SERVER: str
    DB_NAME: str
    DB_DRIVER: str

    @property
    def DATABASE_URL(self) -> str:
        """Build chuỗi kết nối cho Windows Authentication."""
        driver = self.DB_DRIVER.replace(" ", "+")
        return f"mssql+pyodbc://{self.DB_SERVER}/{self.DB_NAME}?driver={driver}&Trusted_Connection=yes"

    # 2. CẬP NHẬT CÚ PHÁP CHO PYDANTIC V2
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE_PATH), 
        env_file_encoding='utf-8',
        extra='ignore' # Tránh báo lỗi nếu file .env có chứa những biến khác chưa khai báo
    )

# Khởi tạo instance
settings = Settings()
