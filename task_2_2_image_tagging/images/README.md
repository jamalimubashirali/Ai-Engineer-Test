# Test Images for Task 2.2 — AI Image Auto-Tagging System

Place **5 advertising images** in this folder before running the tagger.

## Accepted Formats

| Format | Extension        |
| ------ | ---------------- |
| JPEG   | `.jpg` / `.jpeg` |
| PNG    | `.png`           |
| WebP   | `.webp`          |

Any other format (`.gif`, `.bmp`, `.tiff`, etc.) will be skipped with an error
entry logged to `tags_output.json` — the script will not crash.

## Suggested Test Images

Download any 5 royalty-free advertising-style images from:

- https://unsplash.com (search: "product", "lifestyle", "fashion", "fitness")
- https://www.pexels.com
- https://pixabay.com

Save them in this folder as:

```
images/
  image_01.jpg
  image_02.jpg
  image_03.jpg
  image_04.jpg
  image_05.jpg
```

## Running the Script

```bash
# Default: reads ./images, writes tags_output.json
python image_tagger.py

# Custom folder and output path
python image_tagger.py --folder ./images --output tags_output.json
```

## Expected Output Format

```json
{
  "results": [
    {
      "filename": "image_01.jpg",
      "alt_text": "A runner in urban clothing sprinting down a city street at dawn.",
      "tags": [
        "running",
        "urban",
        "athletic",
        "lifestyle",
        "motion",
        "city",
        "fitness"
      ],
      "brand_safety_score": 9,
      "use_cases": [
        "Instagram Story for athletic footwear brand",
        "Banner ad for urban fitness app",
        "TikTok background for sportswear launch"
      ]
    }
  ]
}
```
