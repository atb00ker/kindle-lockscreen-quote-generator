#!/usr/bin/env python3
"""
Image Rotation Script
Rotates all images in the output directory by 180 degrees.
This script scans the 'output' directory for image files, rotates them in place,
and overwrites the original files.
"""

import sys
from pathlib import Path
from PIL import Image

from helpers import find_project_root


def rotate_images(directory=None):
    """
    Rotates all image files in the specified directory by 180 degrees.

    Args:
        directory: The directory containing images to rotate.
                   If None, uses project_root/output.
    """
    if directory is None:
        project_root = find_project_root()
        if not project_root:
            print("Error: Could not find project root (pyproject.toml)")
            return
        directory = project_root / "output"
    else:
        directory = Path(directory)

    if not directory.exists():
        print(f"Error: Directory '{directory}' not found.")
        print(
            "Please run generate_quote_images.py first to generate the output directory."
        )
        return

    # Supported image extensions
    extensions = {".png", ".jpg", ".jpeg", ".bmp", ".tiff"}

    success_count = 0
    error_count = 0

    # Get all files in directory
    files = [f for f in directory.iterdir() if f.is_file()]

    if not files:
        print(f"No files found in '{directory}'.")
        return

    print(f"Found {len(files)} files in '{directory}'. Processing...")

    for file_path in files:
        ext = file_path.suffix.lower()

        if ext in extensions:
            try:
                # Open image
                with Image.open(file_path) as img:
                    # Rotate 180 degrees
                    rotated_img = img.rotate(180)
                    # Create a new filename or overwrite? Overwrite is simpler and standard for "turn images".
                    rotated_img.save(file_path)
                    print(f"✓ Rotated: {file_path.name}")
                    success_count += 1
            except Exception as e:
                print(f"✗ Error processing {file_path.name}: {e}")
                error_count += 1
        else:
            # Skip non-image files
            pass

    print("-" * 40)
    print(f"Processing complete.")
    print(f"✅ Successfully rotated: {success_count}")
    if error_count > 0:
        print(f"❌ Errors encountered: {error_count}")
    else:
        print("All images processed successfully!")


if __name__ == "__main__":
    rotate_images()
