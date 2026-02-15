# Kindle Quote Cover Generator

A Python tool designed to generate beautiful, readable quote images optimized for use as Kindle covers. It can process bulk quotes from CSV files or generate single images on the fly.

Note: The kindle needs to be rooted with KOReader installed to be able to change wallpapers.
It's a very easy and quick process, one only needs to follow instructions for the most part. Read more at [Kindle Modding](https://kindlemodding.org/).

## Features

- **Bulk Generation**: Process multiple CSV files from the `data/` directory.
- **Ad-hoc Generation**: Create single quote images via an interactive CLI.
- **Smart Formatting**: Automatically adjusts font size and wraps text to fit the screen (800x600).
- **Kindle Optimization**:
  - High-contrast black text on white background.
  - **Rotation Utility**: Includes a tool to rotate all generated images by 180 degrees.
- **Custom Fonts**: Supports custom `.ttf` fonts in `fonts/ttf/` or falls back to system fonts (DejaVu, Liberation, Ubuntu).

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/atb00ker/kindle-lockscreen-quote-generator.git
   cd kindle-lockscreen-quote-generator
   ```

1. **Set up a virtual environment (recommended):**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

1. **Install dependencies:**
   ```bash
   pip install .
   ```

## Usage

Run the main script to access the interactive menu:

```bash
python src/main.py
```

### Menu Options

1.  **Generate images from folder (CSV files)**:
    - Reads all `.csv` files in the `data/` directory.
    - Generates images in `output/`.
    - **CSV Format**:
      - Place your `.csv` files in `data/`.
      - Each quote on a new line.
      - Format: `"Quote Text", Speaker Name`
      - If the quote contains commas or newlines, enclose it in double quotes.
      - Speaker is optional.

2.  **Rotate images**:
    - Rotates all images in the `output/` directory by 180 degrees.
    - Overwrites the original files.

3.  **Generate ad-hoc quote image**:
    - Prompts you to enter a quote and speaker manually via the command line.

## Directory Structure

- `src/`: Source code.
  - `main.py`: Entry point.
  - `generate/`: Generation logic.
  - `rotate.py`: Rotation utility.
- `data/`: Place your input CSV files here.
- `output/`: Generated images will appear here.
- `fonts/`: Custom fonts directory (place `.ttf` files in `fonts/ttf/`).

## Customization

You can add custom fonts by placing `.ttf` files in `fonts/ttf/`. The generator picks a random font from the available list for each quote. Some pre-configured fonts include:

- Agbalumo
- Condiment
- Courgette
- Pacifico
- ShadowsIntoLight
- And more...
