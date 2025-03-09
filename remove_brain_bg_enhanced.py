import cv2
import numpy as np
from PIL import Image, ImageFilter

def remove_background_enhanced(input_path, output_path):
    print(f"处理 {input_path}...")
    
    # 读取图像
    img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
    
    # 转换为RGB格式以便处理
    if img.shape[2] == 3:
        # 已经是BGR格式
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        # 如果有Alpha通道，先转换为BGRA再转RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
    
    # 转换为HSV颜色空间，这对分离颜色更有效
    img_hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    
    # 创建更精细的黑色掩码 - 针对暗色背景
    # 调整这些阈值可以获得更好的结果
    lower_black = np.array([0, 0, 0])
    upper_black = np.array([180, 255, 50])  # 增加亮度阈值以包含深灰色
    
    # 创建掩码
    mask = cv2.inRange(img_hsv, lower_black, upper_black)
    
    # 使用形态学操作清理噪点
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    
    # 应用高斯模糊使边缘更平滑
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    
    # 反转掩码 - 我们想要保留非黑色部分
    mask_inv = cv2.bitwise_not(mask)
    
    # 转换为PIL Image进行处理
    img_pil = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    mask_pil = Image.fromarray(mask_inv)
    
    # 创建一个新的透明图像
    img_rgba = img_pil.convert("RGBA")
    
    # 获取数据
    data = img_rgba.getdata()
    new_data = []
    
    # 遍历像素，调整透明度
    for i, item in enumerate(data):
        # 从掩码获取透明度值（0-255）
        alpha = mask_inv.flatten()[i]
        
        # 保留原始RGB，但使用掩码作为透明度值
        if alpha < 10:  # 完全透明的阈值
            new_data.append((255, 255, 255, 0))  # 完全透明
        else:
            # 应用渐变透明度
            new_data.append((item[0], item[1], item[2], alpha))
    
    # 更新图像数据
    img_rgba.putdata(new_data)
    
    # 进一步改进边缘 - 使用模糊滤镜
    img_rgba = img_rgba.filter(ImageFilter.SMOOTH)
    
    # 保存结果
    img_rgba.save(output_path, format="PNG")
    print(f"背景已移除，图像已保存为 {output_path}")
    print("使用了增强的透明度处理以改善边缘质量")

if __name__ == "__main__":
    input_file = "logo-brain.png"
    output_file = "logo-brain-transparent.png"
    remove_background_enhanced(input_file, output_file) 