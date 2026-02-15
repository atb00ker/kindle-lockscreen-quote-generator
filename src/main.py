#!/usr/bin/env python3
"""
Main Script
Entry point for the Quote Image Generator application.
"""

import sys
from generate import generate_from_folder, generate_adhoc
from rotate import rotate_images


def main():
    while True:
        print("\nQuote Image Generator")
        print("=====================")
        print("1. Generate images from folder (CSV files)")
        print("2. Rotate images")
        print("3. Generate ad-hoc quote image")
        print("4. Exit")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            generate_from_folder()
        elif choice == "2":
            rotate_images()
        elif choice == "3":
            generate_adhoc()
        elif choice == "4":
            print("Goodbye!")
            sys.exit(0)
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
