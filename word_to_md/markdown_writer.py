from .text_processing import split_text_by_tokens, convert_to_latex_fraction
from .config import SEGMENT_SEPARATOR

def convert_sections_to_markdown(sections):
    """将解析的 Word 内容转换为 Markdown"""
    md_output = []

    for section in sections:
        text = section["text"]
        titles = section["titles"]
        text = convert_to_latex_fraction(text)
        text_chunks = split_text_by_tokens(text)

        for chunk in text_chunks:
            md_section = SEGMENT_SEPARATOR + "\n"
            md_section += "\n".join([f"{'#' * (i+1)} {title}" for i, title in enumerate(titles)])
            md_section += f"\n{chunk.strip()}\n"
            md_section += SEGMENT_SEPARATOR + "\n"
            md_output.append(md_section)

    return "\n".join(md_output)
