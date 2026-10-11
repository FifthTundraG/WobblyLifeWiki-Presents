# Converts a presents dump file into a markers group for usage in a MediaWiki DataMaps map

import json
from typing import Any

from .common import GamePresent, WikiPresent

OUTPUT_FILE: str = "presents.json"

def wiki_present_to_datamap_marker(present: WikiPresent) -> dict[str, Any]:
    descriptionList: list[str] = []

    if present.location:
        descriptionList.append(f"'''Location:''' {present.location}")

    if present.description:
        descriptionList.append(f"'''Description:''' {present.description}")

    if present.reward:
        descriptionList.append(f"'''Reward:''' {present.reward}")

    return {
        "name": present.name,
        "x": present.x,
        "y": present.y,
        "description": "\n".join(descriptionList),
        "image": present.image
    }


def main() -> None:
    game_presents = GamePresent.parse_dump("presentsdump.txt")
    wiki_presents = [WikiPresent.from_game_present(present) for present in game_presents]

    data = {"presents": [wiki_present_to_datamap_marker(present) for present in wiki_presents]}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Exported {len(data['presents'])} presents to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()