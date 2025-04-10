# input_pdf_path = input("请输入PDF文件路径：")
# output_pdf_path = input("请输入输出PDF文件路径：")
"""
input_pdf_path = 'D:\\360极速浏览器X下载\\2025汇编（带书签）.pdf'
output_pdf_path = 'D:\\360极速浏览器X下载\\2025汇编（带书签）2.pdf'
"""
import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from io import BytesIO
import fitz  # PyMuPDF

# 获取当前文件所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, 'resources')

# 注册字体
font_path = os.path.join(resources_dir, "仿宋_GB2312.ttf")
pdfmetrics.registerFont(TTFont('FangSong_GB2312', font_path))

# 注册楷体字体
kaiti_font_path = os.path.join(resources_dir, "楷体_GB2312.ttf")
pdfmetrics.registerFont(TTFont('KaiTi_GB2312', kaiti_font_path))

# 注册方正小标宋字体
xiaobiaosong_font_path = os.path.join(resources_dir, "FZXBSJW.TTF")
pdfmetrics.registerFont(TTFont('FZXiaoBiaoSong-B05S', xiaobiaosong_font_path))

def generate_toc_page(bookmarks, output_path):
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    p.setFont("FangSong_GB2312", 12)  # 默认使用仿宋字体

    y = A4[1] - 50  # 起始Y坐标
    x = 50          # 起始X坐标
    line_height = 20  # 行高
    page_width = A4[0]  # 页宽
    page_num_right_margin = 50  # 页码右边距

    # 标题
    p.setFont("FZXiaoBiaoSong-B05S", 18)  # 目录标题使用方正小标宋，大小为18号
    title_text = "目录"
    title_width = p.stringWidth(title_text, "FZXiaoBiaoSong-B05S", 18)
    # 计算居中位置
    center_x = (page_width - title_width) / 2
    p.drawString(center_x, y, title_text)
    y -= 32  # 调整下边距，适合更小的字体

    # 分割线
    p.line(x, y - 10, A4[0] - x, y - 10)
    y -= 30

    # 记录每个条目的链接信息（页码和链接区域）
    link_info = []
    current_page = 0  # 当前目录页码

    # 写入书签信息
    for i, bookmark in enumerate(bookmarks):
        title = bookmark["/Title"]
        page_num = bookmark["/Page"]
        real_page_num = bookmark["/RealPage"]  # 使用真实页码
        level = bookmark["/Level"]  # 获取书签级别
        is_leaf = bookmark["/IsLeaf"]  # 获取是否为叶子节点
        
        # 检查下一个标题的缩进是否更长
        has_child = False
        if i < len(bookmarks) - 1:  # 确保不是最后一个标题
            next_level = bookmarks[i + 1]["/Level"]
            if next_level > level:
                has_child = True
        
        # 根据是否有子标题和是否是叶子节点选择字体
        if has_child:
            # 如果有子标题，使用楷体且字体更大
            p.setFont("KaiTi_GB2312", 15)  # 楷体字号更大(15)
            current_font = "KaiTi_GB2312"
            current_font_size = 15
        elif is_leaf:
            p.setFont("FangSong_GB2312", 12)  # 叶子节点使用仿宋
            current_font = "FangSong_GB2312"
            current_font_size = 12
        else:
            p.setFont("FZXiaoBiaoSong-B05S", 12)  # 非叶子节点使用方正小标宋
            current_font = "FZXiaoBiaoSong-B05S"
            current_font_size = 12

        # 根据级别设置缩进
        indent = x + level * 20
        
        # 计算页码宽度和最大标题宽度
        page_num_width = p.stringWidth(str(real_page_num), "FangSong_GB2312", 12)  # 页码宽度计算使用一致的字体
        # 保留约93%的页面宽度给标题，7%给页码
        max_title_width = (page_width - indent - page_num_width - page_num_right_margin) * 0.93
        
        # 当前字体下的标题宽度
        title_width = p.stringWidth(title, current_font, current_font_size)
        
        # 目标页码
        target_page = real_page_num  # 目标页码(PDF内部页码)
        
        if title_width <= max_title_width:
            # 标题不需要换行，直接绘制
            p.drawString(indent, y, title)
            
            # 记录标题链接信息
            link_rect = (indent, y - 2, indent + title_width, y + current_font_size + 2)
            link_info.append({
                'page': current_page,
                'rect': link_rect, 
                'target_page': target_page
            })
            
            # 计算虚线的起始和结束位置
            dots_start_x = indent + title_width + 10  # 标题后留出一定空间
            dots_end_x = page_width - x - page_num_width - 20  # 页码前留出适当空间
            
            # 绘制虚线
            p.setDash([2, 2], 0)  # 设置虚线样式：2点划线，2点空白
            p.line(dots_start_x, y + 4, dots_end_x, y + 4)  # 设置在文字基线上方一点
            p.setDash([], 0)  # 恢复实线
            
            # 写入页码（右对齐）
            p.setFont("FangSong_GB2312", 12)  # 页码统一使用仿宋
            p.drawString(page_width - x - 20, y, str(real_page_num))
            
            # 记录页码链接信息
            page_num_x = page_width - x - 20
            page_num_width = p.stringWidth(str(real_page_num), "FangSong_GB2312", 12)
            page_num_rect = (page_num_x, y - 2, page_num_x + page_num_width, y + 10)
            link_info.append({
                'page': current_page,
                'rect': page_num_rect, 
                'target_page': target_page
            })
            
        else:
            # 标题需要换行处理
            words = list(title)  # 将中文字符分开
            current_line = ""
            current_width = 0
            first_line = True
            
            for char in words:
                char_width = p.stringWidth(char, current_font, current_font_size)
                
                if current_width + char_width <= max_title_width:
                    current_line += char
                    current_width += char_width
                else:
                    # 绘制当前行
                    p.drawString(indent, y, current_line)
                    
                    # 记录当前行链接信息
                    line_width = p.stringWidth(current_line, current_font, current_font_size)
                    line_rect = (indent, y - 2, indent + line_width, y + current_font_size + 2)
                    link_info.append({
                        'page': current_page,
                        'rect': line_rect, 
                        'target_page': target_page
                    })
                    
                    # 不再在第一行绘制页码
                    first_line = False
                    
                    # 准备下一行
                    y -= line_height
                    current_line = char
                    current_width = char_width
            
            # 绘制最后一行（如果有）
            if current_line:
                p.drawString(indent, y, current_line)
                
                # 记录最后一行链接信息
                last_line_width = p.stringWidth(current_line, current_font, current_font_size)
                last_line_rect = (indent, y - 2, indent + last_line_width, y + current_font_size + 2)
                link_info.append({
                    'page': current_page,
                    'rect': last_line_rect, 
                    'target_page': target_page
                })
                
                # 在最后一行绘制虚线和页码
                dots_start_x = indent + p.stringWidth(current_line, current_font, current_font_size) + 10
                dots_end_x = page_width - x - page_num_width - 20  # 页码前留出适当空间
                
                # 绘制虚线
                p.setDash([2, 2], 0)  # 设置虚线样式
                p.line(dots_start_x, y + 4, dots_end_x, y + 4)
                p.setDash([], 0)  # 恢复实线
                
                # 在最后一行末尾绘制页码，无论是否是第一行
                p.setFont("FangSong_GB2312", 12)  # 页码统一使用仿宋
                p.drawString(page_width - x - 20, y, str(real_page_num))
                
                # 记录页码链接信息
                page_num_x = page_width - x - 20
                page_num_width = p.stringWidth(str(real_page_num), "FangSong_GB2312", 12)
                page_num_rect = (page_num_x, y - 2, page_num_x + page_num_width, y + 10)
                link_info.append({
                    'page': current_page,
                    'rect': page_num_rect, 
                    'target_page': target_page
                })
        
        y -= line_height  # 下移到下一个条目

        # 如果超出一页，新建一页
        if y < 50:
            p.showPage()
            current_page += 1  # 增加页计数
            y = A4[1] - 50
            p.setFont("FZXiaoBiaoSong-B05S", 18)  # 使用方正小标宋，18号字体
            title_text = "目录（续）"
            title_width = p.stringWidth(title_text, "FZXiaoBiaoSong-B05S", 18)
            # 计算居中位置
            center_x = (page_width - title_width) / 2
            p.drawString(center_x, y, title_text)
            y -= 32  # 调整下边距，适合更小的字体

    p.save()
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
    
    return link_info  # 返回链接信息

def get_bookmarks(pdf_path):
    reader = PdfReader(pdf_path)
    bookmarks = reader.outline
    return bookmarks, reader

def get_real_page_number(reader, indirect_object):
    """从IndirectObject获取真实页码"""
    # 获取页面对象
    page_obj = reader.get_object(indirect_object.idnum)
    # 遍历PDF的页面，找到对应的页面对象
    for index, page in enumerate(reader.pages):
        if page == page_obj:
            return index + 1  # 索引从0开始，加1得到真实页码
    return None  # 如果未找到，返回None

def process_bookmarks(bookmarks, reader):
    processed_bookmarks = []
    
    # 预先识别哪些节点是非叶子节点
    non_leaf_nodes = set()
    
    def identify_non_leaf_nodes(bookmarks):
        for i, bookmark in enumerate(bookmarks):
            if isinstance(bookmark, dict) and bookmark.get('children'):
                # 如果有children属性，是非叶子节点
                if hasattr(bookmark, 'title'):
                    non_leaf_nodes.add(bookmark.title)
                # 递归处理子节点
                identify_non_leaf_nodes(bookmark.get('children', []))
            elif isinstance(bookmark, list):
                # 如果是列表，则父节点已经在上一级处理
                identify_non_leaf_nodes(bookmark)
    
    identify_non_leaf_nodes(bookmarks)
    
    def recursive_process(bookmarks, level):
        for bookmark in bookmarks:
            if isinstance(bookmark, dict):
                title = bookmark.title
                page_ref = bookmark.page
                real_page_num = get_real_page_number(reader, page_ref)
                
                # 判断是否是叶子节点
                is_leaf = title not in non_leaf_nodes
                
                processed_bookmarks.append({
                    "/Title": title,
                    "/Page": page_ref,
                    "/RealPage": real_page_num,  # 添加真实页码
                    "/Level": level,
                    "/IsLeaf": is_leaf  # 记录是否是叶子节点
                })
                
                # 处理子节点（如果有）
                if bookmark.get('children'):
                    recursive_process(bookmark.get('children', []), level + 1)
            elif isinstance(bookmark, list):
                recursive_process(bookmark, level + 1)

    recursive_process(bookmarks, 0)
    return processed_bookmarks

def insert_toc_to_pdf(input_pdf_path, output_pdf_path):
    bookmarks, reader = get_bookmarks(input_pdf_path)
    processed_bookmarks = process_bookmarks(bookmarks, reader)
    toc_page_path = "toc_page.pdf"
    
    # 生成目录并获取链接信息
    link_info = generate_toc_page(processed_bookmarks, toc_page_path)
    
    # 读取PDF文件
    reader = PdfReader(input_pdf_path)
    toc_reader = PdfReader(toc_page_path)
    writer = PdfWriter()

    # 添加目录页面
    toc_page_count = len(toc_reader.pages)
    print(f"目录页数量: {toc_page_count}")
    for page in toc_reader.pages:
        writer.add_page(page)

    # 添加内容页面
    print(f"原PDF页数: {len(reader.pages)}")
    for page in reader.pages:
        writer.add_page(page)
    
    # 直接从processed_bookmarks中重建书签
    print(f"处理后的书签数量: {len(processed_bookmarks)}")
    
    # 先添加目录书签
    print("添加目录书签")
    writer.add_outline_item("目录", 0)
    
    # 创建书签级别字典，用于存储每个级别的最后一个书签
    level_bookmarks = {}
    
    # 处理书签
    for bookmark in processed_bookmarks:
        title = bookmark["/Title"]
        page_num = bookmark["/RealPage"] + toc_page_count - 1  # 添加目录页偏移
        level = bookmark["/Level"]
        
        print(f"添加书签: {title}, 级别: {level}, 页码: {page_num}")
        
        # 找到此书签的父书签
        parent = None
        if level > 0 and level-1 in level_bookmarks:
            parent = level_bookmarks[level-1]
        
        # 添加书签
        try:
            new_bookmark = writer.add_outline_item(
                title,
                page_num,
                parent=parent
            )
            # 保存此级别的最后一个书签
            level_bookmarks[level] = new_bookmark
            # 清除更高级别的书签缓存（因为新书签可能是新的分支）
            for l in list(level_bookmarks.keys()):
                if l > level:
                    del level_bookmarks[l]
        except Exception as e:
            print(f"添加书签时出错: {e}")
    
    # 写入中间PDF（带书签但没有超链接）
    temp_output_path = "temp_output.pdf"
    print("写入临时PDF文件...")
    with open(temp_output_path, "wb") as f:
        writer.write(f)
    
    # 使用PyMuPDF添加超链接
    print("使用PyMuPDF添加超链接...")
    try:
        # 打开临时PDF
        doc = fitz.open(temp_output_path)
        
        # 添加链接
        successful_links = 0
        failed_links = 0
        
        for idx, link in enumerate(link_info):
            try:
                toc_page_index = link['page']
                rect = link['rect']
                target_page_index = link['target_page'] + toc_page_count - 1  # 调整目标页码
                
                # fitz使用的是PDF坐标系（左下角为原点）
                # 因此需要转换ReportLab坐标（左上角为原点）
                height = A4[1]  # 页面高度（点）
                
                # 创建fitz矩形对象
                fitz_rect = fitz.Rect(
                    rect[0],          # 左
                    height - rect[3], # 下
                    rect[2],          # 右
                    height - rect[1]  # 上
                )
                
                # 在目录页添加链接
                page = doc[toc_page_index]
                page.insert_link({
                    "kind": fitz.LINK_GOTO,
                    "from": fitz_rect,
                    "page": target_page_index
                })
                
                successful_links += 1
                if idx % 50 == 0 or idx == len(link_info) - 1:
                    print(f"添加链接进度: {idx+1}/{len(link_info)}")
                    
            except Exception as e:
                failed_links += 1
                if failed_links <= 5:
                    print(f"添加链接 {idx} 时出错: {e}")
                elif failed_links == 6:
                    print("更多错误被省略...")
        
        print(f"链接添加完成: 成功={successful_links}, 失败={failed_links}")
        
        # 添加测试链接
        try:
            print("添加测试链接到目录页顶部...")
            first_page = doc[0]
            test_rect = fitz.Rect(100, 100, 200, 120)  # 左上右下
            first_page.insert_link({
                "kind": fitz.LINK_GOTO,
                "from": test_rect,
                "page": toc_page_count  # 链接到内容第一页
            })
        except Exception as e:
            print(f"添加测试链接时出错: {e}")
        
        # 保存最终PDF
        print("保存最终PDF...")
        doc.save(output_pdf_path)
        doc.close()
        
        # 删除临时文件
        import os
        os.remove(temp_output_path)
        
    except Exception as e:
        print(f"PyMuPDF处理时出错: {e}")
        # 如果出错，使用临时文件作为输出
        import shutil
        shutil.copy(temp_output_path, output_pdf_path)

        print("由于错误，使用无超链接版本作为输出")
    
    print("PDF目录和原书签结构生成完成！")
    print(f"目录页面已保存为: {toc_page_path}")
    print(f"最终PDF保存为: {output_pdf_path}")

def add_contents_page(input_pdf_path, output_pdf_path=None):
    """
    为PDF添加目录页
    :param input_pdf_path: 输入PDF路径
    :param output_pdf_path: 输出PDF路径，如果为None则自动生成
    """
    if output_pdf_path is None:
        # 自动生成输出文件名
        base_name = os.path.splitext(input_pdf_path)[0]
        output_pdf_path = f"{base_name}(with content).pdf"
    
    insert_toc_to_pdf(input_pdf_path, output_pdf_path)
    return output_pdf_path

if __name__ == "__main__":
    input_pdf_path = 'E:\\25汇编文件\\merged_with_bookmarks.pdf'
    add_contents_page(input_pdf_path)