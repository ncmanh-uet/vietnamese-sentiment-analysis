from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, DECIMAL, Text, UnicodeText
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

# Lớp cơ sở để các class Model kế thừa
Base = declarative_base()

class User(Base):
    __tablename__ = "Users"
    
    UserID = Column(Integer, primary_key=True, index=True)
    Username = Column(String(50), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    FullName = Column(String(100))
    UserRole = Column(String(20), default="User")

    # Mối quan hệ: Một User có thể có nhiều Comments
    comments = relationship("Comment", back_populates="user")

class Product(Base):
    __tablename__ = "Products"
    
    ProductID = Column(Integer, primary_key=True, index=True)
    ProductName = Column(String(200), nullable=False)
    Description = Column(Text)
    Price = Column(DECIMAL(18, 2))
    ImageUrl = Column(String(500))

    # Mối quan hệ: Một Product có thể có nhiều Comments
    comments = relationship("Comment", back_populates="product")

class Comment(Base):
    __tablename__ = "Comments"
    
    CommentID = Column(Integer, primary_key=True, index=True)
    ProductID = Column(Integer, ForeignKey("Products.ProductID"))
    UserID = Column(Integer, ForeignKey("Users.UserID"))
    Content = Column(UnicodeText, nullable=False)
    SentimentLabel = Column(String(20))
    ConfidenceScore = Column(Float)
    CreatedAt = Column(DateTime, default=datetime.utcnow)

    # Mối quan hệ trỏ ngược lại User và Product
    user = relationship("User", back_populates="comments")
    product = relationship("Product", back_populates="comments")