# Converts a presents dump file into a markers group for usage in a MediaWiki DataMaps map

import json
from typing import Any

from .common import GamePresent

OUTPUT_FILE: str = "presents.json"

def game_present_to_datamap_marker(present: GamePresent) -> dict[str, Any]:
    return {
        "name": present.name,
        "x": present.x,
        "y": present.y,
        "image": present.image
    }


def main() -> None:
    game_presents = GamePresent.parse_dump("presentsdump.txt")

    data = {"presents": [game_present_to_datamap_marker(present) for present in game_presents]}

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Exported {len(data['presents'])} presents to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()