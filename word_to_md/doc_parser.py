from docx import Document
from docx.oxml.ns import qn
from .text_processing import extract_text_with_superscript_subscript, table_to_html


def get_outline_level(para):
    """获取段落的大纲级别"""
    try:
        return int(para._element.xpath('.//w:outlineLvl')[0].get(qn('w:val')))
    except:
        return None


def read_word_document(doc_path):
    """读取 Word 文档，解析标题、文本和表格"""
    doc = Document(doc_path)
    sections = []
    current_section = {"titles": [], "text": ""}
    title_stack = []

    elements = list(doc.element.body)
    for elem in elements:
        if elem.tag.endswith('p'):
            para = doc.paragraphs[[p._element for p in doc.paragraphs].index(elem)]
            text = extract_text_with_superscript_subscript(para)
            if not text:
                continue

            outline_level = get_outline_level(para)
            if para.style.name.startswith("Heading") or (outline_level is not None):
                level = outline_level + 1 if outline_level is not None else int(para.style.name.split()[-1])
                title_stack = title_stack[:level - 1]
                title_stack.append(text)
                if current_section["text"]:
                    sections.append(current_section)
                current_section = {"titles": title_stack.copy(), "text": ""}
            else:
                current_section["text"] += text + "\n"

        elif elem.tag.endswith('tbl'):
            table = doc.tables[[t._element for t in doc.tables].index(elem)]
            table_html = table_to_html(table)
            current_section["text"] += "\n" + table_html + "\n"

    if current_section["text"]:
        sections.append(current_section)
    return sections
