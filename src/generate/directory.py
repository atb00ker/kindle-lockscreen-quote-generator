#!/usr/bin/env python3
"""
Generate Folder Script
Generates images from all CSV files in the data directory.
"""

from generate.helpers import QuoteImageGenerator, find_project_root


def generate_from_folder():
    """Generates images from all CSV files in the data directory."""
    print("Generating images from folder...")

    # Initialize generator
    generator = QuoteImageGenerator(
        width=800, height=600, bg_color="white", text_color="black"
    )

    # Get project root and construct paths relative to it
    project_root = find_project_root()
    if not project_root:
        print("Error: Could not find project root (pyproject.toml)")
        return

    data_dir = project_root / "data"
    output_dir = project_root / "output"

    if not data_dir.exists():
        print(f"Error: Data directory not found at {data_dir}")
        return

    csv_files = [f for f in data_dir.iterdir() if f.suffix == ".csv"]

    if not csv_files:
        print(f"No CSV files found in {data_dir}")
        return

    total_images = 0
    for csv_file in csv_files:
        print(f"Processing {csv_file.name}...")
        count = generator.process_csv(str(csv_file), output_dir=str(output_dir))
        total_images += count

    print(f"\n✅ Total images generated: {total_images}")
    print(f"📁 Images saved in: {output_dir}")


if __name__ == "__main__":
    generate_from_folder()
