from PIL import Image, ImageDraw, ImageFont
import os

def create_s_favicon(output_path='favicon.png', size=128, bg_color=(18, 18, 18), 
                    s_color=(180, 180, 180), s_highlight=(230, 230, 230)):
    """
    创建一个风格化的S字母作为favicon
    
    参数:
        output_path (str): 输出文件路径
        size (int): favicon大小（像素）
        bg_color (tuple): 背景色 (R,G,B)
        s_color (tuple): S字母主色 (R,G,B)
        s_highlight (tuple): S字母高光色 (R,G,B)
    """
    print(f"创建 {size}x{size} 的S字母favicon...")
    
    # 创建透明背景的图像
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # 绘制略微透明的圆形背景
    padding = int(size * 0.08)  # 减小padding使圆形背景更大
    draw.ellipse([(padding, padding), (size-padding, size-padding)], 
                 fill=bg_color+(250,))  # 增加不透明度
    
    # 尝试加载自定义字体，如果失败则使用默认字体
    try:
        # 增大字体尺寸以使S更大更清晰
        font_size = int(size * 0.75)
        font = ImageFont.truetype("Arial Bold.ttf", font_size)
    except IOError:
        try:
            # macOS上Arial字体的路径
            font_size = int(size * 0.75)
            font = ImageFont.truetype("/Library/Fonts/Arial Bold.ttf", font_size)
        except IOError:
            try:
                # 使用系统的默认无衬线粗体字体
                font = ImageFont.truetype(None, font_size)
            except IOError:
                # 如果没有可用字体，使用默认字体
                font = ImageFont.load_default()
    
    # 计算文本的位置，使其更精确地居中
    text = "S"
    try:
        # PIL 9.0.0+的新方法
        bbox = font.getbbox(text)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except AttributeError:
        try:
            # PIL 8.0.0+的方法
            left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
            text_width = right - left
            text_height = bottom - top
        except AttributeError:
            # 回退到老方法（虽然已弃用但部分版本可能还支持）
            text_width, text_height = draw.textsize(text, font=font)
    
    # 精确计算中心位置，不添加垂直偏移
    position = ((size-text_width)/2, (size-text_height)/2)
    
    # 创建渐变效果的S字母
    # 首先绘制一个轻微偏移的浅色S作为高光
    highlight_offset = int(size * 0.02)  # 减小偏移量使效果更微妙
    
    # 添加轮廓效果以增强可见性
    outline_color = (240, 240, 240)
    for offset_x in range(-1, 2):
        for offset_y in range(-1, 2):
            if offset_x == 0 and offset_y == 0:
                continue
            draw.text((position[0]+offset_x, position[1]+offset_y), 
                  text, font=font, fill=outline_color)
    
    # 绘制高光效果
    draw.text((position[0]-highlight_offset, position[1]-highlight_offset), 
              text, font=font, fill=s_highlight)
    
    # 然后绘制主S字母
    draw.text(position, text, font=font, fill=s_color)
    
    # 保存图像
    img.save(output_path, format="PNG")
    print(f"favicon已保存至 {output_path}")
    return img

def create_favicon_set():
    """创建一套不同尺寸的favicon图标，只包含网站实际需要的尺寸"""
    # 创建favicon目录（如果不存在）
    favicon_dir = 'favicon'
    if not os.path.exists(favicon_dir):
        os.makedirs(favicon_dir)
    
    # 只保留网站实际需要的favicon尺寸
    sizes = [16, 32, 48, 192]
    
    # 生成主favicon.png (192px)
    main_favicon = create_s_favicon('favicon.png', 192)
    
    # 生成不同尺寸的favicon
    for size in sizes:
        output_path = os.path.join(favicon_dir, f'favicon-{size}x{size}.png')
        if size == 192:
            # 192px直接使用主favicon
            main_favicon.save(output_path, format="PNG")
            print(f"重用主favicon: {output_path}")
        else:
            # 其他尺寸重新生成，以获得更好的清晰度
            create_s_favicon(output_path, size)

if __name__ == "__main__":
    # 生成一套favicon
    create_favicon_set() 