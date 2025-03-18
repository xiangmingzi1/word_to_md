import re
from .config import tokenizer


def extract_text_with_superscript_subscript(paragraph):
    """提取段落文本，保留上标和下标，转换为 LaTeX 格式"""
    text = ""
    for run in paragraph.runs:
        run_text = run.text
        if not run_text:
            continue

        namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        is_sup = run.element.find('.//w:vertAlign[@w:val="superscript"]', namespaces=namespaces) is not None
        is_sub = run.element.find('.//w:vertAlign[@w:val="subscript"]', namespaces=namespaces) is not None

        if is_sup:
            text += f"$^{{{run_text}}}$"
        elif is_sub:
            text += f"$_{{{run_text}}}$"
        else:
            text += run_text
    return text.strip()


def table_to_html(table):
    """将 Word 表格转换为 HTML 格式"""
    html = "<table border='1'>\n"
    for row in table.rows:
        html += "  <tr>\n"
        for cell in row.cells:
            cell_text = " ".join(extract_text_with_superscript_subscript(p) for p in cell.paragraphs if p.text.strip())
            html += f"    <td>{cell_text}</td>\n"
        html += "  </tr>\n"
    html += "</table>"
    return html


def convert_to_latex_fraction(text):
    """将上标/下标组合转换为 LaTeX 分数形式"""
    pattern = r'(\d+\.?\d*)\$?(\^\{[^\}]+\})\$?/\$?_(\{[^\}]+\})\$?'

    def replace_fraction(match):
        num = match.group(1)
        sup = match.group(2).replace('^{', '^{').replace('}', '}')
        sub = match.group(3).replace('{', '{').replace('}', '}')
        return f"{num}$\\frac{{{sup}}}{{{sub}}}$"

    return re.sub(pattern, replace_fraction, text)


def split_text_by_tokens(text, max_tokens=800):
    """按 Token 限制拆分文本"""
    chunks = []
    current_chunk = []
    current_length = 0
    in_table = False

    for line in text.split("\n"):
        if "<table" in line:
            in_table = True
        if "</table>" in line:
            in_table = False

        token_count = len(tokenizer.tokenize(line))

        if not in_table and current_length + token_count > max_tokens:
            if current_chunk:
                chunks.append("\n".join(current_chunk))
            current_chunk = [line]
            current_length = token_count
        else:
            current_chunk.append(line)
            current_length += token_count

    if current_chunk:
        chunks.append("\n".join(current_chunk))
    return chunks
