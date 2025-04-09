import os
import fitz  # PyMuPDF

# 递归搜索文件夹中的PDF文件，并记录文件夹结构
def search_pdf_files(folder_path):
    pdf_files = []
    folder_structure = {}

    def _search_pdf_files(current_path, current_structure):
        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)
            if os.path.isdir(item_path):
                current_structure[item] = {}
                _search_pdf_files(item_path, current_structure[item])
            elif item.lower().endswith('.pdf'):
                # 去掉文件名后缀
                name_without_extension = os.path.splitext(item)[0]
                pdf_files.append((item_path, name_without_extension, current_structure))
                current_structure[name_without_extension] = None

    _search_pdf_files(folder_path, folder_structure)
    return pdf_files, folder_structure

# 合并PDF文件并设置书签
def merge_pdfs_with_bookmarks(pdf_files, folder_structure, output_file):
    doc = fitz.open()  # 创建一个新的PDF文档
    toc = []  # 用于存储目录结构
    current_page = 0  # 当前页码

    def _add_toc_entry(toc, name, level, page):
        toc.append([level, name, page])

    def _add_bookmarks(current_structure, parent_level=1, parent_page=0):
        nonlocal current_page
        for name, children in current_structure.items():
            if children is None:  # 如果是PDF文件
                pdf_path, file_name, folder_structure = pdf_files.pop(0)
                pdf_to_add = fitz.open(pdf_path)
                doc.insert_pdf(pdf_to_add)
                pdf_to_add.close()
                page_count = doc.page_count - current_page
                _add_toc_entry(toc, file_name, parent_level, current_page + 1)
                current_page += page_count
            else:  # 如果是文件夹
                _add_toc_entry(toc, name, parent_level, current_page + 1)
                _add_bookmarks(children, parent_level + 1, current_page + 1)

    _add_bookmarks(folder_structure)
    doc.set_toc(toc)  # 设置目录
    doc.save(output_file)
    doc.close()

# 主函数
def main():
    #folder_path = input("请输入要搜索的文件夹路径：")  # 替换为你的文件夹路径
    folder_path = "E:\\25汇编文件"
    output_file = os.path.join(folder_path, "merged_with_bookmarks.pdf")  # 输出文件路径
    # 搜索PDF文件和文件夹结构
    pdf_files, folder_structure = search_pdf_files(folder_path)
    if not pdf_files:
        print("未找到PDF文件。")
        return

    # 合并PDF文件并设置书签
    merge_pdfs_with_bookmarks(pdf_files, folder_structure, output_file)
    print(f"PDF文件已合并并设置书签，保存为：{output_file}")

if __name__ == "__main__":
    main()