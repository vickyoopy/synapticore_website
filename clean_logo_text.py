import cv2
import numpy as np
from PIL import Image, ImageOps

def extract_text_from_logo(input_path, output_path):
    print(f"Processing {input_path}...")
    
    # 读取图像
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # 如果图像有透明通道，保留它；否则创建一个
    if img.shape[2] == 4:
        # 已经有Alpha通道
        pass
    else:
        # 将BGR转换为BGRA
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 转换为灰度以便处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 应用自适应阈值来更好地检测文字
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                  cv2.THRESH_BINARY_INV, 11, 2)
    
    # 查找轮廓 - 专注于文字形状
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 创建掩码
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # 过滤并绘制文字轮廓
    min_area = 50  # 最小区域阈值，用于过滤噪声
    max_area = img.shape[0] * img.shape[1] * 0.4  # 最大区域阈值，避免选择过大的区域（如背景）
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            # 计算轮廓的宽高比，文字通常更高
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / float(h)
            
            # 文字的轮廓通常有特定的宽高比范围
            if 0.1 < aspect_ratio < 5:
                # 更可能是文字
                cv2.drawContours(mask, [contour], -1, 255, -1)
    
    # 扩展掩码区域以确保捕获完整文字
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=3)
    
    # 应用掩码
    result = img.copy()
    result[mask == 0] = [0, 0, 0, 0]  # 将非文字区域设为透明
    
    # 使用PIL进一步处理并保存
    pil_img = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    
    # 保存结果
    pil_img.save(output_path, format="PNG")
    print(f"文字图像已保存为 {output_path}")

if __name__ == "__main__":
    input_file = "logo.png"
    output_file = "logo-text.png"
    extract_text_from_logo(input_file, output_file) 