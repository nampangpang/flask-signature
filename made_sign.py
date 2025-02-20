import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import pytesseract
import random
import tensorflow as tf
from tensorflow.keras.models import load_model

app = Flask(__name__, static_folder="static")
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# AI 모델 로드 (손글씨 스타일 분석 및 서명 생성)
MODEL_PATH = "signature_model.h5"
if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
else:
    model = None  # 모델이 없는 경우 기본 OpenCV 처리 사용

# 분위기 키워드 매칭 (다양한 표현 추가)
IMPACT_MAP = {
    "강렬한": "bold", "파워풀한": "bold", "강한": "bold", "인상적인": "bold",
    "부드러운": "soft", "우아한": "soft", "편안한": "soft", "따뜻한": "soft",
    "아름다운": "elegant", "세련된": "elegant", "품격 있는": "elegant", "고급스러운": "elegant",
    "전문적인": "professional", "비즈니스적인": "professional", "신뢰감 있는": "professional", "공식적인": "professional",
    "캐주얼한": "casual", "가벼운": "casual", "친근한": "casual", "일상적인": "casual",
    "모던한": "modern", "미니멀한": "modern", "심플한": "modern", "트렌디한": "modern",
    "고전적인": "classic", "전통적인": "classic", "유서 깊은": "classic", "역사적인": "classic"
}

# 사용처 키워드 매칭 (다양한 사용처 추가)
USAGE_MAP = {
    "회사": "corporate", "비즈니스": "corporate", "직장": "corporate", "업무용": "corporate",
    "계약서": "legal", "법률 문서": "legal", "공증": "legal", "공식 서류": "legal",
    "예술 작품": "artistic", "디자인": "artistic", "일러스트": "artistic", "갤러리": "artistic",
    "개인 서명": "personal", "사적인": "personal", "편지": "personal", "일기": "personal",
    "공식 문서": "official", "정부 문서": "official", "공문": "official", "행정 문서": "official",
    "쇼핑몰": "ecommerce", "온라인 쇼핑": "ecommerce", "마켓": "ecommerce", "비즈니스 사이트": "ecommerce",
    "소셜 미디어": "social", "SNS": "social", "인스타그램": "social", "트위터": "social",
    "게임": "gaming", "e스포츠": "gaming", "스트리밍": "gaming", "유튜브": "gaming"
}

def extract_handwriting(image_path):
    """손글씨만 추출하는 함수"""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"이미지를 불러올 수 없습니다: {image_path}")
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    return binary

def generate_signature(name, impact, usage, handwriting_image, complexity):
    """AI가 분석한 스타일을 기반으로 서명을 생성하는 함수"""
    handwriting_style = extract_handwriting(handwriting_image)
    height, width = handwriting_style.shape
    blank_canvas = np.ones((height, width), dtype=np.uint8) * 255
    
    if model:
        input_data = np.expand_dims(handwriting_style, axis=0) / 255.0
        generated_signature = model.predict(input_data)[0]
        generated_signature = (generated_signature * 255).astype(np.uint8)
        return generated_signature
    else:
        font = {
            "하": cv2.FONT_HERSHEY_SIMPLEX,
            "중": cv2.FONT_HERSHEY_COMPLEX,
            "상": cv2.FONT_HERSHEY_SCRIPT_SIMPLEX,
            "최상": cv2.FONT_HERSHEY_SCRIPT_COMPLEX
        }.get(complexity, cv2.FONT_HERSHEY_SIMPLEX)
        
        thickness = {"하": 1, "중": 2, "상": 3, "최상": 4}.get(complexity, 1)
        font_scale = {"하": 1, "중": 1.5, "상": 2, "최상": 2.5}.get(complexity, 1)
        
        cv2.putText(blank_canvas, name, (50, 100), font, font_scale, (0, 0, 0), thickness)
        return blank_canvas

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        impact = request.form.get("impact", "").strip()
        usage = request.form.get("usage", "").strip()
        complexity = request.form.get("complexity", "중").strip()
        file = request.files.get("file")
        
        impact = IMPACT_MAP.get(impact, "default")
        usage = USAGE_MAP.get(usage, "general")
        
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        
        processed_image = generate_signature(name, impact, usage, file_path, complexity)
        output_path = os.path.join(PROCESSED_FOLDER, "signature.png")
        cv2.imwrite(output_path, processed_image)
        
        return render_template("result.html", image_url=f"/processed/signature.png")
    
    return render_template("index.html")

@app.route("/processed/<filename>")
def processed_file(filename):
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

# cd "C:\Users\namkh\OneDrive\바탕 화면\python\.vs" 하고 python made_sign.py
# 아우 ㅗㅈ나힘드렌

# 파일 수정후 재업로드 방법법
# git add requirements.txt(파일 이름)
# git commit -m "Removed tensorflow_intel from requirements.txt"(파일 이름)
# git push origin main

# 파일 추가 후 업로드 방법법
# git add runtime.txt
#git commit -m "Added runtime.txt to specify Python version for Render"
#git push origin main
 
'''
git add .
git commit -m "Render 배포를 위한 설정 추가"
git push origin main

'''

