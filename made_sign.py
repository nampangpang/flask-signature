import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import pytesseract
import random

app = Flask(__name__, static_folder="static")
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

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
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)
    return binary

def generate_signature(name, impact, usage, handwriting_image, complexity):
    """AI가 분석한 스타일을 기반으로 서명을 생성하는 함수"""
    handwriting_style = extract_handwriting(handwriting_image)
    height, width = handwriting_style.shape
    blank_canvas = np.ones((height, width), dtype=np.uint8) * 255
    y_offset = 50
    
    font = cv2.FONT_HERSHEY_SIMPLEX if complexity == "하" else cv2.FONT_HERSHEY_SCRIPT_COMPLEX
    thickness = 1 if complexity == "하" else 2 if complexity == "중" else 3
    
    signature_text = f"{name}"
    if impact: signature_text += f" {impact}"
    if usage: signature_text += f" ({usage})"
    
    cv2.putText(blank_canvas, signature_text, (50, y_offset), font, 1, (0, 0, 0), thickness)
    return blank_canvas

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        impact = request.form.get("impact", "").strip()
        usage = request.form.get("usage", "").strip()
        complexity = request.form.get("complexity", "중").strip()
        file = request.files.get("file")
        
        # AI가 이해할 수 있도록 변환
        impact = IMPACT_MAP.get(impact, "default")  # 미리 정의된 분위기 키워드 없으면 default
        usage = USAGE_MAP.get(usage, "general")  # 미리 정의된 사용처 키워드 없으면 general
        
        print(f"📌 Debug: Converted Impact: {impact}, Converted Usage: {usage}")
        
        if not name or not impact or not usage or not file:
            return "입력값이 부족합니다. 모든 항목을 채워주세요.", 400
        
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
 


