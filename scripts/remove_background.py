from PIL import Image
import numpy as np
import os

def remove_black_background(input_path, output_path, tolerance=30):
    """
    移除图像的黑色背景，使其变为透明
    
    参数:
        input_path (str): 输入图像的路径
        output_path (str): 输出图像的路径
        tolerance (int): 黑色的容差值，值越大，越多的深色像素会被视为背景
    """
    # 打开图像
    img = Image.open(input_path).convert('RGBA')
    data = np.array(img)
    
    # 创建一个全透明的数组
    alpha = data[:, :, 3]
    
    # 识别黑色区域 (R,G,B 都很低的区域)
    # 转换为布尔掩码数组，True表示应该变透明的像素
    black_mask = (data[:, :, 0] < tolerance) & (data[:, :, 1] < tolerance) & (data[:, :, 2] < tolerance)
    
    # 将黑色区域的alpha值设为0（完全透明）
    alpha[black_mask] = 0
    
    # 保存结果
    result = Image.fromarray(data)
    result.save(output_path)
    
    print(f"图像已处理并保存到 {output_path}")
    return result

if __name__ == "__main__":
    # 尝试不同的可能路径
    possible_paths = [
        "../logo-text.png",  # 从scripts目录
        "logo-text.png",     # 直接在当前目录
        os.path.join(os.path.dirname(os.path.dirname(__file__)), "logo-text.png")  # 从脚本文件位置
    ]
    
    input_file = None
    for path in possible_paths:
        if os.path.exists(path):
            input_file = path
            break
    
    if input_file:
        # 确定输出路径
        if input_file.startswith(".."):
            output_file = "../logo-text-transparent.png"
        else:
            output_file = "logo-text-transparent.png"
            
        print(f"找到输入文件: {input_file}")
        print(f"输出文件设置为: {output_file}")
        
        remove_black_background(input_file, output_file, tolerance=30)
    else:
        print("错误: 无法找到logo-text.png文件。请确保文件存在于正确的位置。") 