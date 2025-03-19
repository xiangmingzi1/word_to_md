import argparse
import os
from word_to_md.doc_parser import parse_word_document
from word_to_md.text_processing import convert_to_latex_fraction, split_text_by_tokens
from word_to_md.markdown_writer import write_markdown


def main():
    parser = argparse.ArgumentParser(description="Convert Word document to Markdown")
    parser.add_argument("input", help="Input Word document filename (in input/) or full path")
    parser.add_argument("output", help="Output Markdown filename (in output/) or full path")
    parser.add_argument("--max-tokens", type=int, default=800,
                        help="Maximum number of tokens per segment (default: 800)")
    args = parser.parse_args()

    # Determine input and output paths
    input_dir = "input"
    output_dir = "output"

    # Ensure directories exist
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)

    # If input is a filename (not a full path), assume it's in input/
    if not os.path.isabs(args.input) and not args.input.startswith("input/"):
        input_path = os.path.join(input_dir, args.input)
    else:
        input_path = args.input

    # If output is a filename (not a full path), assume it's in output/
    if not os.path.isabs(args.output) and not args.output.startswith("output/"):
        output_path = os.path.join(output_dir, args.output)
    else:
        output_path = args.output

    # Ensure input file has .docx extension and output has .md extension
    if not input_path.endswith(".docx"):
        input_path += ".docx"
    if not output_path.endswith(".md"):
        output_path += ".md"

    # Check if input file exists
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    # 解析文档
    sections = parse_word_document(input_path)

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

    write_markdown(processed_sections, output_path)
    print(f"Conversion complete. Output saved to {output_path}")


if __name__ == "__main__":
    main()
