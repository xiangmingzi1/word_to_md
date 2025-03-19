from .config import SEGMENT_SEPARATOR


def write_markdown(sections, output_path):
    """将解析的内容转换为 Markdown"""
    md_output = []

    for section in sections:
        text = section["text"]
        titles = section["titles"]

        md_section = SEGMENT_SEPARATOR + "\n"
        md_section += "\n".join([f"{'#' * (i + 1)} {title}" for i, title in enumerate(titles)])
        md_section += f"\n{text.strip()}\n"
        md_section += SEGMENT_SEPARATOR + "\n"
        md_output.append(md_section)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_output))