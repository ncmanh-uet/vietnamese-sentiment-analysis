from app.ai_models.predictor import ai_predictor

def test_prediction():
    print("-" * 50)
    comments = [
        "Sản phẩm dùng chán lắm, pin tuột như tụt quần, thất vọng",
        "Giao hàng nhanh, máy đẹp, cầm rất đầm tay, shop tư vấn nhiệt tình",
        "Máy xài cũng được, không có gì đặc sắc so với giá tiền"
    ]
    
    for cmt in comments:
        result = ai_predictor.predict(cmt)
        print(f"Khách nói: {result['original_text']}")
        print(f"AI hiểu là: {result['processed_text']}")
        print(f"Kết quả: {result['sentiment']} (Tin cậy: {result['confidence']*100:.1f}%)")
        print("-" * 50)

if __name__ == "__main__":
    test_prediction()