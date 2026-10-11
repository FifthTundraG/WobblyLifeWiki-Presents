import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

info: dict[str, Any] = json.load(open("src/info.json", "r", encoding="utf-8"))  # noqa: SIM115

@dataclass
class GamePresent:
    x: int
    y: int
    z: int
    name: str
    image: str

    @staticmethod
    def parse_dump(file_path: str) -> list["GamePresent"]:
        presents: list[GamePresent] = []

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
    
                presents.append(GamePresent(
                    x=int(float(x)),
                    y=int(float(y)),
                    z=int(float(z)),
                    name=name.strip(),
                    image=texture_name.replace("_", " ") + ".png"
                ))

        presents.sort(
            key=lambda present: int(
                re.search(r"\d+", present.name).group()
            )
        )

        return presents


@dataclass
class WikiPresent(GamePresent):
    section: str
    location: str
    description: str
    reward: str

    @staticmethod
    def from_game_present(present: GamePresent) -> "WikiPresent":
        """Constructs a `WikiPresent` from a `GamePresent` by looking up additional information in `info.json`."""

        present_info = info["presents"][present.name]

        if present_info is None:
            raise ValueError(f"Present '{present.name}' not found in info.json")

        return WikiPresent(
            x=present.x,
            y=present.y,
            z=present.z,
            name=present.name,
            image=present.image,
            section=present_info["section"],
            location=present_info["location"],
            description=present_info["description"],
            reward=present_info["reward"]
        )

def get_presents_in_section(section: str) -> list[WikiPresent]:
    """Returns a list of `WikiPresent` objects that belong to the specified section."""
    
    return [
        WikiPresent.from_game_present(present)
        for present in GamePresent.parse_dump("presentsdump.txt")
        if info["presents"][present.name]["section"] == section
    ]

def init() -> None:
    """Generic initialization function for the different scripts in this project."""

    Path("build").mkdir(parents=True, exist_ok=True)