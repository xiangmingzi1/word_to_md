import re
from .config import TOKENIZER, MAX_TOKENS


def split_text_by_tokens(text, max_tokens=MAX_TOKENS):
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

        token_count = len(TOKENIZER.tokenize(line))

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


def convert_to_latex_fraction(text):
    """将上标/下标组合转换为 LaTeX 分数形式"""
    pattern = r'(\d+\.?\d*)\$?(\^\{[^\}]+\})\$?/\$?_(\{[^\}]+\})\$?'

    def replace_fraction(match):
        num = match.group(1)
        sup = match.group(2).replace('^{', '^{').replace('}', '}')
        sub = match.group(3).replace('{', '{').replace('}', '}')
        return f"{num}$\\frac{{{sup}}}{{{sub}}}$"

    return re.sub(pattern, replace_fraction, text)