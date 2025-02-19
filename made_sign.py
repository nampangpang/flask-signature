from flask import Flask, request, render_template, send_from_directory
import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from PIL import Image
import pytesseract

app = Flask(__name__, static_folder="static")
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extract_handwriting(image_path):
    """Extracts handwriting style from an image using OpenCV."""
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY_INV)
    return binary

def generate_signature(name, impact, usage, handwriting_image):
    """Generates a digital signature based on the user's handwriting."""
    handwriting_style = extract_handwriting(handwriting_image)
    signature_text = f"{name}\n{impact}\n{usage}"
    
    blank_canvas = np.ones((200, 600), dtype=np.uint8) * 255
    y_offset = 50
    
    for line in signature_text.split("\n"):
        cv2.putText(blank_canvas, line, (50, y_offset), cv2.FONT_HERSHEY_SCRIPT_COMPLEX, 1, (0, 0, 0), 2)
        y_offset += 50
    
    return blank_canvas

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        name = request.form.get("name", "")  # 기본값 "" 설정
        impact = request.form.get("impact", "")
        usage = request.form.get("usage", "")
        file = request.files.get("file")  # 파일은 request.files에서 가져와야 함
        
        if not name or not impact or not usage or not file:
            return "입력값이 부족합니다. 모든 항목을 채워주세요.", 400
            
        if file:
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)
            signature = generate_signature(name, impact, usage, file_path)
            output_path = os.path.join(UPLOAD_FOLDER, "signature.png")
            cv2.imwrite(output_path, signature)
            return render_template("result.html", image_url=f"/uploads/signature.png")
    
    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render에서 자동 할당한 포트 사용
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
 
