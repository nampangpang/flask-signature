import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from PIL import Image, ImageFont, ImageDraw
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
    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        print(f"⚠️ 모델 로드 실패: {e}")
        model = None
else:
    model = None

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

# 허용된 이미지 확장자
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 한글 폰트 적용 함수
def draw_text(img, text, position, font_size=40, font_path="static/fonts/NanumGothic-Regular.ttf"):
    font = ImageFont.truetype(font_path, font_size)
    img_pil = Image.fromarray(img)
    draw = ImageDraw.Draw(img_pil)
    draw.text(position, text, font=font, fill=(0, 0, 0))
    return np.array(img_pil)

# 손글씨 필체 추출 함수
def extract_handwriting(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if image is None:
        raise ValueError(f"이미지를 불러올 수 없습니다: {image_path}")
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    return binary

def generate_signature(name, impact, usage, handwriting_image, complexity):
    handwriting_style = extract_handwriting(handwriting_image)
    height, width = handwriting_style.shape
    blank_canvas = np.ones((height, width, 3), dtype=np.uint8) * 255

    font_size = {"하": 30, "중": 40, "상": 50, "최상": 60}.get(complexity, 40)
    signature_text = f"{name}\n{impact}\n{usage}"
    blank_canvas = draw_text(blank_canvas, signature_text, (50, 100), font_size)
    
    return blank_canvas

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "파일이 없습니다.", 400
        
        file = request.files["file"]
        if file.filename == "":
            return "파일 이름이 비어 있습니다.", 400
        
        if not allowed_file(file.filename):
            return "허용되지 않은 파일 형식입니다.", 400

        name = request.form.get("name", "").strip()
        impact = request.form.get("impact", "").strip()
        usage = request.form.get("usage", "").strip()
        complexity = request.form.get("complexity", "중").strip()
        
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
    app.run(host="0.0.0.0", port=port, debug=False)

# cd "C:\Users\namkh\OneDrive\바탕 화면\python\.vs" 하고 python made_sign.py
# 아우 ㅗㅈ나힘드렌

# 파일 수정후 재업로드 방법법
# git add requirements.txt(파일 이름)
# git commit -m "Removed tensorflow_intel from requirements.txt"(파일 이름)
# git push origin main

# 파일 추가 후 업로드 방법법
'''
 git add runtime.txt
git commit -m "Added runtime.txt to specify Python version for Render"
git push origin main
 '''
 
'''
git add .
git commit -m "Render 배포를 위한 설정 추가"
git push origin main

'''

'''
가상환경으로 이동 venv\Scripts\activate
'''
