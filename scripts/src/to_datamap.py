# Converts a presents dump file into a markers group for usage in a MediaWiki DataMaps map

import json
import re
import sys


def parse_presents(file_path):
    presents = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            match = re.search(
                r"Name:(.*?);GUID:[^;]+;Position:"
                r"\s*(-?\d+(?:\.\d+)?),"
                r"\s*(-?\d+(?:\.\d+)?),"
                r"\s*(-?\d+(?:\.\d+)?);Texture:(.*)",
                line,
            )

            if not match:
                continue

            name, x, y, z, texture_name = match.groups()

            presents.append({
                "x": int(float(x)),
                "y": int(float(z)),
                "name": name.strip(),
                "image": texture_name.replace("_", " ") + ".png"
            })

    presents.sort(
        key=lambda present: int(
            re.search(r"\d+", present["name"]).group()
        )
    )

    return {"presents": presents}

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python3 to_datamap.py <input_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    data = parse_presents(input_file)

    with open("presents.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print(f"Exported {len(data['presents'])} presents to presents.json")


if __name__ == "__main__":
    main()