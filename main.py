import argparse
from word_to_md.doc_parser import parse_word_document
from word_to_md.text_processing import convert_to_latex_fraction, split_text_by_tokens
from word_to_md.markdown_writer import write_markdown


def main():
    parser = argparse.ArgumentParser(description="Convert Word document to Markdown")
    parser.add_argument("input", help="Input Word document path (.docx)")
    parser.add_argument("output", help="Output Markdown file path (.md)")
    parser.add_argument("--max-tokens", type=int, default=800,
                        help="Maximum number of tokens per segment (default: 800)")
    args = parser.parse_args()

    # 解析文档
    sections = parse_word_document(args.input)

    # 处理文本并写入 Markdown
    processed_sections = []
    for section in sections:
        text = convert_to_latex_fraction(section["text"])
        text_chunks = split_text_by_tokens(text, max_tokens=args.max_tokens)
        for chunk in text_chunks:
            processed_sections.append({
                "titles": section["titles"],
                "text": chunk
            })

    write_markdown(processed_sections, args.output)
    print(f"Conversion complete. Output saved to {args.output}")


if __name__ == "__main__":
    main()