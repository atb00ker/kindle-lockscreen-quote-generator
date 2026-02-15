#!/usr/bin/env python3
"""
Generate Ad-hoc Script
Generates a single image from user input.
"""

from generate.helpers import QuoteImageGenerator, find_project_root


def generate_adhoc():
    """Generates a single image from user input."""
    print("Generate Ad-hoc Quote Image")
    print("-" * 30)

    quote = input("Enter the quote: ").strip()
    if not quote:
        print("Error: Quote cannot be empty.")
        return

    speaker = input("Enter the author/speaker (optional): ").strip()

    # Initialize generator
    generator = QuoteImageGenerator(
        width=800, height=600, bg_color="white", text_color="black"
    )

    # Get project root and construct output path
    project_root = find_project_root()
    if not project_root:
        print("Error: Could not find project root (pyproject.toml)")
        return

    output_dir = project_root / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename based on quote content (first few words)
    safe_quote = "".join(c if c.isalnum() else "_" for c in quote[:20]).strip("_")
    filename = f"adhoc_{safe_quote}.png"
    output_path = output_dir / filename

    generator.generate_image(quote, speaker, str(output_path))
    print(f"\n✅ Image generated: {output_path}")


if __name__ == "__main__":
    generate_adhoc()
