#!/usr/bin/env python3
"""
Quote Image Generator
Generates beautiful quote images from CSV files containing quotes and speakers.
"""

import os
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import textwrap
from helpers import find_project_root


class QuoteImageGenerator:
    """Generate images from quotes with customizable styling."""

    # Fonts provided by user
    FONTS = [
        "Agbalumo-Regular",
        "Condiment-Regular",
        "Courgette-Regular",
        "EmilysCandy-Regular",
        "FreckleFace-Regular",
        "GamjaFlower-Regular",
        "IrishGrover-Regular",
        "Knewave-Regular",
        "Pacifico-Regular",
        "ShadowsIntoLight-Regular",
    ]

    # Standard fonts for speaker
    SPEAKER_FONTS = ["DejaVuSans"]

    # Common font paths on Linux systems
    @staticmethod
    def _get_font_paths():
        """Get font paths, with project fonts directory based on pyproject.toml location."""
        project_root = find_project_root()
        paths = []

        if project_root:
            # Project fonts directory relative to project root
            project_fonts = project_root / "fonts" / "ttf"
            paths.append(str(project_fonts))

        # System font paths
        paths.extend(
            [
                "/usr/share/fonts/truetype/dejavu",
                "/usr/share/fonts/truetype/liberation",
                "/usr/share/fonts/truetype/ubuntu",
            ]
        )

        return paths

    def __init__(self, width=800, height=600, bg_color="white", text_color="black"):
        """
        Initialize the quote image generator.

        Args:
            width: Image width in pixels
            height: Image height in pixels
            bg_color: Background color
            text_color: Text color
        """
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.text_color = text_color
        self.font_paths = self._get_font_paths()
        self.available_fonts = self._find_available_fonts()
        self.speaker_font_path = self._find_normal_font()

    def _find_available_fonts(self):
        """Find available font files on the system."""
        available = []

        for font_path in self.font_paths:
            if os.path.exists(font_path):
                for font_name in self.FONTS:
                    # Try different file extensions
                    for ext in [".ttf", ".TTF"]:
                        font_file = os.path.join(font_path, font_name + ext)
                        if os.path.exists(font_file):
                            available.append(font_file)
                            break

        # Fallback to default font if no fonts found
        if not available:
            print("Warning: No fancy fonts found, using default font")
            available = [None]  # Will use default PIL font
        else:
            print(f"Found {len(available)} fancy fonts")

        return available

    def _find_normal_font(self):
        """Find a normal font for the speaker."""
        for font_path in self.font_paths:
            if os.path.exists(font_path):
                for font_name in self.SPEAKER_FONTS:
                    # Try different file extensions
                    for ext in [".ttf", ".TTF"]:
                        font_file = os.path.join(font_path, font_name + ext)
                        if os.path.exists(font_file):
                            return font_file
        return None

    def _get_random_font(self, size):
        """Get a random font from available fonts."""
        font_path = random.choice(self.available_fonts)

        if font_path is None:
            # Use default font
            return ImageFont.load_default()

        try:
            return ImageFont.truetype(font_path, size)
        except Exception as e:
            print(f"Error loading font {font_path}: {e}")
            return ImageFont.load_default()

    def _get_speaker_font(self, size):
        """Get the normal font for speaker."""
        if self.speaker_font_path:
            try:
                return ImageFont.truetype(self.speaker_font_path, size)
            except Exception as e:
                print(f"Error loading speaker font: {e}")

        return ImageFont.load_default()

    def _wrap_text(self, text, font, max_width):
        """
        Wrap text to fit within max_width.

        Args:
            text: Text to wrap
            font: PIL font object
            max_width: Maximum width in pixels

        Returns:
            List of wrapped lines
        """
        lines = []
        paragraphs = text.split("\n")

        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append("")
                continue

            # Estimate characters per line
            avg_char_width = font.getbbox("x")[2]
            chars_per_line = max(10, int(max_width / avg_char_width))

            # Wrap the paragraph
            wrapped = textwrap.wrap(paragraph, width=chars_per_line)

            # Adjust if still too wide
            final_wrapped = []
            for line in wrapped:
                while font.getbbox(line)[2] > max_width and len(line) > 10:
                    # Reduce and re-wrap
                    chars_per_line = int(chars_per_line * 0.9)
                    wrapped = textwrap.wrap(paragraph, width=chars_per_line)
                    break
                final_wrapped.append(line)

            lines.extend(final_wrapped if final_wrapped else wrapped)

        return lines

    def _calculate_font_size(self, text, speaker, draw, max_width, max_height):
        """
        Calculate optimal font size to fit text within dimensions.

        Args:
            text: Quote text
            speaker: Speaker name
            draw: ImageDraw object
            max_width: Maximum width for text
            max_height: Maximum height for text

        Returns:
            Tuple of (quote_font, speaker_font, wrapped_lines)
        """
        # Start with a large font size and decrease until it fits
        quote_font_size = 120
        min_font_size = 20

        while quote_font_size >= min_font_size:
            quote_font = self._get_random_font(quote_font_size)
            # Smaller, normal font for speaker
            speaker_font = self._get_speaker_font(max(14, int(quote_font_size * 0.4)))

            # Wrap the text
            lines = self._wrap_text(text, quote_font, max_width)

            # Calculate total height
            line_height = quote_font.getbbox("Ay")[3] * 1.3  # Add line spacing
            total_text_height = len(lines) * line_height

            # Add speaker height if present
            if speaker and speaker.strip() and speaker.upper() != "NULL":
                speaker_height = speaker_font.getbbox(speaker)[3]
                total_text_height += speaker_height * 2  # Add spacing

            # Check if it fits
            if total_text_height <= max_height:
                return quote_font, speaker_font, lines

            # Reduce font size
            quote_font_size -= 2

        # Fallback to minimum size
        quote_font = self._get_random_font(min_font_size)
        speaker_font = self._get_speaker_font(max(12, int(min_font_size * 0.4)))
        lines = self._wrap_text(text, quote_font, max_width)

        return quote_font, speaker_font, lines

    def generate_image(self, quote, speaker=None, output_path=None):
        """
        Generate an image for a quote.

        Args:
            quote: Quote text
            speaker: Speaker name (optional)
            output_path: Path to save the image (optional)

        Returns:
            PIL Image object
        """
        # Create image
        img = Image.new("RGB", (self.width, self.height), self.bg_color)
        draw = ImageDraw.Draw(img)

        # Calculate margins (2% on each side for min white space)
        margin_x = int(self.width * 0.02)
        margin_y = int(self.height * 0.05)
        max_width = self.width - (2 * margin_x)
        max_height = self.height - (2 * margin_y)

        # Add quotes to the text if author is present
        has_speaker = speaker and speaker.strip() and speaker.upper() != "NULL"
        if has_speaker and not quote.startswith('"'):
            quote = f'"{quote}"'

        # Get fonts and wrapped text
        quote_font, speaker_font, lines = self._calculate_font_size(
            quote, speaker, draw, max_width, max_height
        )

        # Calculate text block height
        line_height = quote_font.getbbox("Ay")[3] * 1.3
        text_height = len(lines) * line_height

        # Add speaker height if present
        show_speaker = speaker and speaker.strip() and speaker.upper() != "NULL"
        if show_speaker:
            speaker_height = speaker_font.getbbox(speaker)[3]
            text_height += speaker_height * 2

        # Start y position (centered vertically)
        y = (self.height - text_height) / 2

        # Draw quote text (centered)
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=quote_font)
            text_width = bbox[2] - bbox[0]
            x = (self.width - text_width) / 2
            draw.text((x, y), line, fill=self.text_color, font=quote_font)
            y += line_height

        # Draw speaker (centered, below quote)
        if show_speaker:
            y += speaker_height * 0.5  # Add spacing
            speaker_text = f"— {speaker}"
            bbox = draw.textbbox((0, 0), speaker_text, font=speaker_font)
            speaker_width = bbox[2] - bbox[0]
            x = (self.width - speaker_width) / 2
            draw.text((x, y), speaker_text, fill=self.text_color, font=speaker_font)

        # Save image if path provided
        if output_path:
            img.save(output_path)
            print(f"Saved: {output_path}")

        return img

    def process_csv(self, csv_path, output_dir="output"):
        """
        Process a CSV file and generate images for all quotes.

        Args:
            csv_path: Path to CSV file
            output_dir: Directory to save images

        Returns:
            Number of images generated
        """
        # Create output directory
        Path(output_dir).mkdir(exist_ok=True)

        # Read CSV and generate images
        count = 0
        csv_filename = Path(csv_path).stem

        with open(csv_path, "r", encoding="utf-8") as f:
            # Read the entire file content
            content = f.read()

        # Parse CSV manually to handle multi-line quotes
        lines = content.split("\n")
        current_quote = ""
        current_speaker = ""
        in_quote = False
        header_skipped = False

        for line in lines:
            if not header_skipped:
                header_skipped = True
                continue

            if not line.strip():
                # Empty line - process current quote if any
                if current_quote.strip():
                    count += 1
                    output_path = os.path.join(
                        output_dir, f"{csv_filename}_quote_{count:03d}.png"
                    )
                    self.generate_image(
                        current_quote.strip(), current_speaker, output_path
                    )
                    current_quote = ""
                    current_speaker = ""
                    in_quote = False
                continue

            # Check if line starts with a quote
            if line.startswith('"'):
                in_quote = True
                line = line[1:]  # Remove leading quote

            if in_quote:
                # Check if quote ends in this line
                if '",' in line or line.endswith('"'):
                    # Quote ends
                    if '",' in line:
                        quote_part, speaker_part = line.rsplit('",', 1)
                        current_quote += (
                            "\n" + quote_part if current_quote else quote_part
                        )
                        current_speaker = speaker_part.strip()
                    else:
                        current_quote += (
                            "\n" + line[:-1] if current_quote else line[:-1]
                        )

                    # Generate image
                    count += 1
                    output_path = os.path.join(
                        output_dir, f"{csv_filename}_quote_{count:03d}.png"
                    )
                    self.generate_image(
                        current_quote.strip(), current_speaker, output_path
                    )
                    current_quote = ""
                    current_speaker = ""
                    in_quote = False
                else:
                    # Quote continues
                    current_quote += "\n" + line if current_quote else line
            else:
                # Single line quote
                if "," in line:
                    parts = line.rsplit(",", 1)
                    quote = parts[0].strip()
                    speaker = parts[1].strip() if len(parts) > 1 else ""

                    if quote:
                        count += 1
                        output_path = os.path.join(
                            output_dir, f"{csv_filename}_quote_{count:03d}.png"
                        )
                        self.generate_image(quote, speaker, output_path)

        # Process last quote if any
        if current_quote.strip():
            count += 1
            output_path = os.path.join(
                output_dir, f"{csv_filename}_quote_{count:03d}.png"
            )
            self.generate_image(current_quote.strip(), current_speaker, output_path)

        print(f"Generated {count} images from {csv_path}")
        return count
