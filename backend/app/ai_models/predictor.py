import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from peft import PeftModel
from pathlib import Path
from app.ai_models.dataPreprocessingPipeline import preprocess_text

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "final_shopee_model_lora"

class SentimentPredictor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.id2label = {0: "NEG", 1: "POS", 2: "NEU"}
        
        base_model_name = "wonrax/phobert-base-vietnamese-sentiment"
        self.tokenizer = AutoTokenizer.from_pretrained(base_model_name)
        
        base_model = AutoModelForSequenceClassification.from_pretrained(
            base_model_name, 
            num_labels=3, 
            ignore_mismatched_sizes=True
        )
        
        try:
            self.model = PeftModel.from_pretrained(base_model, str(MODEL_PATH))
        except Exception as e:
            self.model = base_model
            
        self.model.to(self.device)
        self.model.eval() # Chuyển sang chế độ dự đoán


    def predict(self, text: str):
        processed_text = preprocess_text(text)
        
        inputs = self.tokenizer(
            processed_text, 
            return_tensors="pt", 
            truncation=True, 
            max_length=128, 
            padding='max_length'
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            probs = F.softmax(logits, dim=-1)
            conf, pred_id = torch.max(probs, dim=-1)
            
        label = self.id2label[pred_id.item()]
        confidence = conf.item()
        
        return {
            "original_text": text,
            "processed_text": processed_text,
            "sentiment": label,
            "confidence": round(confidence, 4)
        }

ai_predictor = SentimentPredictor()