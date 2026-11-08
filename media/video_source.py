"""Validate and select the video script without changing workshop slide notes."""

import json
from pathlib import Path

SCENES = {"team", "recipe", "flow", "board", "review", "brief", "split",
          "interface", "compare", "code", "score", "filter", "branch"}


def write_script(root, chapters):
    output = ["# Animated beginner-friendly video script",
              "\nThis script covers the original workshop topics with shorter visual teaching beats.",
              "The PowerPoint's long-form speaker notes are a separate teaching reference.\n"]
    for chapter in chapters:
        output.append(f"\n## {chapter['slide']:02}. {chapter['title']}\n")
        for beat in chapter["beats"]:
            output.append(f"\n### {beat['headline']}\n\nVisual: {beat['scene']}\n\n{beat['text']}\n")
    (Path(root) / "video-script.md").write_text("\n".join(output), encoding="utf-8")


def effective_chapters(manifest, root, storyboard=None):
    path = Path(storyboard) if storyboard else None
    if path is None and manifest.get("video", {}).get("style") == "animated":
        path = Path(root) / "storyboard.json"
    if path is None:
        return manifest["slides_data"]
    story = json.loads(path.read_text(encoding="utf-8"))
    chapters = story["chapters"]
    if len(chapters) != manifest["slides"] or story["fps"] != 24:
        raise ValueError("Animated story must cover every chapter at 24 fps.")
    result = []
    for index, (original, item) in enumerate(zip(manifest["slides_data"], chapters), 1):
        if item["slide"] != index or item["title"] != original["title"].replace("\n", " "):
            raise ValueError(f"Story chapter order/title differs at {index}.")
        if not 2 <= len(item["beats"]) <= 4:
            raise ValueError(f"Chapter {index} needs two to four teaching beats.")
        for beat in item["beats"]:
            if beat["scene"] not in SCENES or not beat["headline"] or not beat["labels"]:
                raise ValueError(f"Invalid visual teaching beat in chapter {index}.")
            if not 15 <= len(beat["text"].split()) <= 110:
                raise ValueError(f"Teaching beat is too short or dense in chapter {index}.")
        result.append({**original, **item, "narration": " ".join(beat["text"] for beat in item["beats"])})
    return result
