import cv2
import numpy as np
from PIL import Image, ImageOps

def remove_background(input_path, output_path):
    print(f"处理 {input_path}...")
    
    # 读取图像
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # 如果图像没有Alpha通道，创建一个
    if img.shape[2] == 3:
        # 将BGR转换为BGRA
        img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    
    # 转换为灰度以便处理
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 使用自适应阈值分离前景和背景
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 240, 255, cv2.THRESH_BINARY_INV)
    
    # 形态学操作清理图像
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
    
    # 查找轮廓 - 专注于大的大脑区域
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 创建掩码
    mask = np.zeros(img.shape[:2], dtype=np.uint8)
    
    # 绘制轮廓
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # 只处理足够大的区域
            cv2.drawContours(mask, [contour], -1, 255, -1)
    
    # 扩展掩码区域以确保捕获完整的大脑图像
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # 应用掩码
    result = img.copy()
    result[mask == 0] = [0, 0, 0, 0]  # 将背景设为透明
    
    # 使用PIL进一步处理并保存
    pil_img = Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    
    # 保存结果
    pil_img.save(output_path, format="PNG")
    print(f"背景已移除，图像已保存为 {output_path}")

if __name__ == "__main__":
    input_file = "logo-brain.png"
    output_file = "logo-brain-transparent.png"
    remove_background(input_file, output_file) 