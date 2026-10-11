from common import WikiPresent, get_presents_in_section, info

OUTPUT_FILE: str = "presents.wikitext"

ARTICLE_HEADER: str = "<noinclude>__NOTOC__{{Generated|link=https://github.com/FifthTundraG/WobblyLifeWiki-Presents|contact=FifthTundraG}}</noinclude>"

def output_row(present: WikiPresent) -> str:
    """Outputs a single row of the table for a given present."""

    return f"""|-
|{{{{Anchor|{present.name}}}}}[[File:{present.image}|120px]]
|{present.name.split(" ")[-1]}
|{present.location}
|{present.description}
|{present.reward}"""

def create_section(section: str) -> str:
    output = f"=== {section} ===\n"
    output += '''{| class="wikitable mw-collapsible"
|+
!Image
!#
!Location
!Description
!Reward'''

    section_members = get_presents_in_section(section)

    for present in section_members:
        output += "\n" + output_row(present)

    output += "\n|}"

    return output

def main() -> None:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(ARTICLE_HEADER)
        for section in info["sections"]:
            section_output = create_section(section)
            file.write(section_output + "\n\n")

    print(f"Exported presents page to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()