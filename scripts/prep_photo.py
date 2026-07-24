import sys
import cv2
import io
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path, output_path="source-prepped.png"):
    with open(input_path, "rb") as f:
        input_data = f.read()
    no_bg_bytes = remove(input_data)

    img_pil = Image.open(io.BytesIO(no_bg_bytes)).convert("RGBA")
    np_img = np.array(img_pil)
    rgb = np_img[:, :, :3]
    alpha = np_img[:, :, 3]

    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced_gray = clahe.apply(gray)

    white_bg = np.ones_like(enhanced_gray) * 255
    alpha_factor = alpha / 255.0
    final_gray = (enhanced_gray * alpha_factor + white_bg * (1 - alpha_factor)).astype(np.uint8)

    cv2.imwrite(output_path, final_gray)
    print(f"Prepped photo saved to {output_path}")

if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(src)