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
        name = request.form["이름을 알려주세요!"]
        impact = request.form["어떤 인상을 주고 싶으신가요 ?"]
        usage = request.form["사용처가 어디일까요 ?"]
        file = request.files["손글씨체를 보여주세요!"]
        
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
    app.run(debug=True)
# cd "C:\Users\namkh\OneDrive\바탕 화면\python\.vs" 하고 python made_sign.py
# 아우 ㅗㅈ나힘드렌

