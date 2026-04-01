"""
image_tagger.py — Entry-point for Task 2.2 batch image processing.

Usage:
    python image_tagger.py
    python image_tagger.py --folder ./images --output tags_output.json
"""
import argparse
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from models import ImageTaggingOutput, ImageAnalysis
from services import analyze_image

_SUPPORTED_FORMATS = {".png", ".jpg", ".jpeg", ".webp"}


def process_folder(folder: str, output_file: str) -> None:
    folder_path = Path(folder)

    if not folder_path.exists() or not folder_path.is_dir():
        print(f"ERROR: '{folder}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    image_files = [
        f for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() in _SUPPORTED_FORMATS
    ]

    if not image_files:
        print(f"No supported images found in '{folder}'.", file=sys.stderr)
        sys.exit(0)

    results: list[ImageAnalysis] = []

    for img_path in image_files:
        print(f"Processing: {img_path.name} …")
        try:
            analysis = analyze_image(str(img_path))
            results.append(analysis)
            print(f"  [OK] Brand safety score: {analysis.brand_safety_score}/10")
        except (ValueError, RuntimeError) as err:
            print(f"  [X] Skipped — {err}")
            # Record a partial error entry so every image appears in the output.
            # brand_safety_score uses minimum valid value (1) per schema constraint (ge=1).
            results.append(ImageAnalysis(
                filename=img_path.name,
                alt_text="[ERROR — could not analyze image]",
                tags=["error"],
                brand_safety_score=1,
                use_cases=[f"ERROR: {err}"],
            ))

    # Validate the full batch through the wrapper model
    output = ImageTaggingOutput(results=results)

    with open(output_file, "w", encoding="utf-8") as f:
        # Use model_dump to get a plain dict from Pydantic, then serialize to JSON
        json.dump(output.model_dump(), f, indent=2)

    print(f"\nDone! Results saved to '{output_file}'.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch AI image tagger")
    parser.add_argument("--folder", default="images", help="Folder containing images")
    parser.add_argument("--output", default="tags_output.json", help="Output JSON file")
    args = parser.parse_args()

    os.makedirs(args.folder, exist_ok=True)
    process_folder(args.folder, args.output)


if __name__ == "__main__":
    main()
