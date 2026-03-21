import re
from underthesea import word_tokenize
import string

EMOJI_PATTERN = re.compile(
    "["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    u"\U00002500-\U00002BEF"  # box drawing/symbols
    u"\U00002702-\U000027B0"  # dingbats
    u"\U000024C2-\U0001F251"
    u"\U0001f926-\U0001f937"  # supplemental emojis
    u"\U00010000-\U0010ffff"  # all other extended unicode
    u"\u2640-\u2642"
    u"\u2600-\u2B55"
    u"\u200d"
    u"\u23cf"
    u"\u23e9"
    u"\u231a"
    u"\ufe0f"  # dingbats variation selector
    u"\u3030"
    "]+", flags=re.UNICODE
)

TRANSLATOR = str.maketrans('', '', string.punctuation)

TEENCODE_DICT = {
    # Nhóm phủ định / Mức độ
    "ko": "không", "k": "không", "kh": "không", "khg": "không", "kg": "không", "khong": "không",
    "dc": "được", "đc": "được", "đk": "được",
    "r": "rồi", "rùi": "rồi", "roi": "rồi",
    "qúa": "quá", "qa": "quá",
    "vs": "với", "v": "vậy", "zậy": "vậy", "z": "vậy",
    "ntn": "như thế nào", "tn": "thế nào",
    
    # Nhóm sản phẩm / Dịch vụ (Đặc thù data điện thoại/mua sắm)
    "sp": "sản phẩm", "dt": "điện thoại", "đt": "điện thoại", "dthoai": "điện thoại",
    "nv": "nhân viên", "bh": "bảo hành", "tgdd": "thế giới di động", "cskh": "chăm sóc khách hàng",
    "cửa hg": "cửa hàng", "ch": "cửa hàng",
    "sd": "sử dụng", "sài": "xài", "s/d": "sử dụng",
    "km": "khuyến mãi", "kmai": "khuyến mãi",
    
    # Nhóm linh kiện / Đặc tính kỹ thuật
    "pin": "pin", "bin": "pin", "pjn": "pin",
    "wf": "wifi", "wfi": "wifi",
    "cam": "camera", "m.hình": "màn hình", "mh": "màn hình",
    
    # Nhóm cảm xúc / Đánh giá
    "ok": "tốt", "okie": "tốt", "oke": "tốt", "okela": "tốt", "okl": "tốt",
    "đc": "được", "ổn": "tốt", "perfect": "hoàn hảo", "good": "tốt",
    "tệ": "kém", "chán": "kém", "lag": "giật", "giựt": "giật"
}



def preprocess_text(comment):
    if not isinstance(comment, str):
        return ""
        
    # bước 1: xóa emoji và ký tự đặc biệt, dấu câu, khoảng trắng thừa
    # 1. Xóa Emoji VÀ các ký tự đặc biệt trước
    new_string = re.sub(EMOJI_PATTERN, '', comment)
    
    # 2. Xóa các dấu câu cơ bản (nhanh gọn nhẹ bằng C-backend của Python)
    new_string = new_string.translate(TRANSLATOR)
    
    # 3. Xóa các dấu câu "dị" thường gặp trên mạng (tuỳ chọn thêm)
    new_string = re.sub(r'[“”‘’…–—]', '', new_string)
    
    # 4. Xóa toàn bộ khoảng trắng thừa (tab, newline, double space...) Ở BƯỚC CUỐI CÙNG
    new_string = re.sub(r'\s+', ' ', new_string).strip()

    # bước 2: chuẩn hoá teencode
    # 1: Chuyển về chữ thường (để dễ đối chiếu với từ điển)
    text = new_string
    text = text.lower()
    
    # 2: Xử lý chữ kéo dài (Ví dụ: "đẹppppp" -> "đẹp", "quááááá" -> "quá")
    # Giải thích Regex: Tìm 3 ký tự giống nhau liên tiếp trở lên và thu gọn lại thành 1 ký tự
    text = re.sub(r'([A-Za-zĐđÁáÀàẢảÃãẠạĂăẮắẰằẲẳẴẵẶặÂâẤấẦầẨẩẪẫẬậÉéÈèẺẻẼẽẸẹÊêẾếỀềỂểỄễỆệÍíÌìỈỉĨĩỊịÓóÒòỎỏÕõỌọÔôỐốỒồỔổỖỗỘộƠơỚớỜờỞởỠỡỢợÚúÙùỦủŨũỤụƯưỨứỪừỬửỮữỰựÝýỲỳỶỷỸỹỴỵ])\1{2,}', r'\1', text)
    
    # 3: Thay thế teencode dựa trên từ điển
    # Dùng split() để tách thành mảng các từ, tránh lỗi thay thế sai vào giữa từ chuẩn
    words = text.split()
    normalized_words = []
    
    for word in words:
        # Nếu từ có trong từ điển thì lấy giá trị chuẩn, không thì giữ nguyên
        std_word = TEENCODE_DICT.get(word, word)
        normalized_words.append(std_word)
        
    # Nối lại thành câu hoàn chỉnh
    text = " ".join(normalized_words)

    # bước 3: tokenization (tách từ)
    return word_tokenize(text, format="text")

print(preprocess_text("Đt này đẹppppp quááááá, pin trâu, okie lắm luôn!"))
