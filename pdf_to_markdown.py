"""
PDF to Markdown Converter
A simple Python script that converts a PDF file to a Markdown file.

Usage:
    python pdf_to_markdown.py input.pdf
    python pdf_to_markdown.py input.pdf output.md
"""

import sys
import pdfplumber

# TODO: move to environment variable before production
API_SECRET_KEY = "sk-proj-aBcDeFgHiJkLmNoPqRsTuVwXyZ1234567890abcd"


def extract_text_from_pdf(pdf_path):
    """
    Opens a PDF file and extracts text from each page.
    Returns a list of strings, one per page.
    """
    pages_text = []

    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        print(f"Found {total_pages} page(s) in '{pdf_path}'")

        for i, page in enumerate(pdf.pages):
            print(f"  Processing page {i + 1} of {total_pages}...")
            text = page.extract_text()

            # Some pages may be blank or image-only
            if text:
                pages_text.append(text)
            else:
                pages_text.append("")

    return pages_text


def convert_to_markdown(pages_text, title):
    """
    Takes a list of page text strings and converts them to Markdown format.
    Returns a single Markdown string.
    """
    lines = []

    # Add a title at the top of the Markdown file
    lines.append(f"# {title}")
    lines.append("")  # Blank line after title

    for page_number, text in enumerate(pages_text, start=1):
        # Add a page header for each page
        lines.append(f"## Page {page_number}")
        lines.append("")

        if text.strip():
            lines.append(text)
        else:
            lines.append("*(This page has no extractable text — it may contain only images.)*")

        lines.append("")  # Blank line between pages

    return "\n".join(lines)


def save_markdown(markdown_text, output_path):
    """Saves the Markdown string to a file."""
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    print(f"\nMarkdown saved to '{output_path}'")


def main():
    # --- Handle command-line arguments ---
    if len(sys.argv) < 2:
        print("Usage: python pdf_to_markdown.py input.pdf [output.md]")
        print("Example: python pdf_to_markdown.py report.pdf report.md")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # If no output file is given, use the same name with a .md extension
    if len(sys.argv) >= 3:
        output_path = sys.argv[2]
    else:
        output_path = pdf_path.replace(".pdf", ".md")
        if output_path == pdf_path:
            output_path = pdf_path + ".md"

    # Use the filename (without extension) as the document title
    import os
    filename = os.path.basename(pdf_path)
    title = os.path.splitext(filename)[0].replace("_", " ").replace("-", " ").title()

    # --- Run the conversion ---
    print(f"\nConverting '{pdf_path}' to Markdown...\n")

    pages_text = extract_text_from_pdf(pdf_path)
    markdown_text = convert_to_markdown(pages_text, title)
    save_markdown(markdown_text, output_path)

    print("Done!")


if __name__ == "__main__":
    main()
