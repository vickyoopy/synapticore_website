from PIL import Image, ImageFilter
import numpy as np
import os

def process_logo(input_file='logo.png', output_file='logo-brain.png'):
    try:
        # 检查文件是否存在
        if not os.path.exists(input_file):
            print(f"错误: 找不到输入文件 {input_file}")
            return False
            
        # 打开原始 logo 图像
        img = Image.open(input_file)
        
        # 将图像转换为 RGBA 模式（如果不是）以支持透明度
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        
        # 获取图像尺寸
        width, height = img.size
        
        # 获取图像数据为 numpy 数组
        data = np.array(img)
        
        # 创建一个透明图层的副本
        result_data = np.zeros_like(data)
        
        # 分离通道
        r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
        
        # 保留原始 alpha 通道以备后用
        original_alpha = a.copy()
        
        # 基于色调和亮度计算一个更好的掩码
        # 创建一个色彩丰富度指标 (max(r,g,b) - min(r,g,b))
        color_range = np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b)
        
        # 创建一个亮度指标
        brightness = (r.astype(float) + g.astype(float) + b.astype(float)) / 3
        
        # 定义可能的主要图形区域
        # 假设背景是暗色的，文字是亮色的或特定颜色
        # 我们希望保留中等亮度的彩色元素
        
        # 背景掩码 (暗色区域)
        background_mask = (brightness < 60) & (color_range < 30)
        
        # 文字掩码 (亮色区域，通常是白色或浅色)
        text_mask = (brightness > 180) | ((r > 180) & (g > 180) & (b > 180))
        
        # 创建要保留的区域掩码
        # 只保留既不是背景也不是文字的部分，并且原始 alpha 不为零
        keep_mask = ~(background_mask | text_mask) & (original_alpha > 0)
        
        # 应用掩码到结果数据
        result_data[keep_mask] = data[keep_mask]
        
        # 设置透明度
        # 将保留区域的 alpha 通道设为原始值
        result_data[:,:,3] = np.where(keep_mask, original_alpha, 0)
        
        # 创建新图像
        result_img = Image.fromarray(result_data)
        
        # 应用轻微的模糊以平滑边缘
        result_img = result_img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        # 保存处理后的图像
        result_img.save(output_file)
        
        print(f"处理完成! 背景和文字已被移除，新文件已保存为 {output_file}")
        return True
        
    except Exception as e:
        print(f"处理图像时出错: {e}")
        return False

if __name__ == "__main__":
    process_logo() 