import os
import cv2
import numpy as np
from flask import Flask, request, render_template, send_from_directory
from PIL import Image
import pytesseract

app = Flask(__name__, static_folder="static")
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

def extract_handwriting(image_path):
    """손글씨만 추출하는 함수"""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)

    # 노이즈 제거 및 컨투어 검출
    kernel = np.ones((3,3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=2)

    return binary

def generate_signature(name, impact, usage, handwriting_image):
    """손글씨 스타일을 분석하여 서명을 생성하는 함수"""
    handwriting_style = extract_handwriting(handwriting_image)

    # 빈 캔버스 생성
    height, width = handwriting_style.shape
    blank_canvas = np.ones((height, width), dtype=np.uint8) * 255

    # 사용자 입력을 손글씨 스타일로 변환
    signature_text = f"{name}\n{impact}\n{usage}"
    y_offset = 50

    for line in signature_text.split("\n"):
        cv2.putText(blank_canvas, line, (50, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        y_offset += 50

    return blank_canvas

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        impact = request.form.get("impact", "").strip()
        usage = request.form.get("usage", "").strip()
        file = request.files.get("file")

        if not name or not impact or not usage or not file:
            return "입력값이 부족합니다. 모든 항목을 채워주세요.", 400
        
        # 이미지 저장
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 손글씨 스타일 추출 및 서명 생성
        processed_image = generate_signature(name, impact, usage, file_path)
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
 
