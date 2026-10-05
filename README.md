# WobblyLifeWiki-Presents
Creates the data for the Presents page on the Wobbly Life Wiki.

## Usage
You will need to install BepInEx 5 and place the built DLL file into the `BepInEx/plugins/` folder in your game instance. The game will also attempt to destroy the BepInEx manager `GameObject` on load, which means you will also need to update your `BepInEx/config/BepInEx.cfg` file to say this:
```yaml
...
[Chainloader]
...
HideManagerGameObject = true
...
```

Load into any save and press `P`. You should see a file called `presentsdump.txt` in your `BepInEx/plugins/` directory. This file will have a list of present names, GUIDs, and locations.

### DataMap markers
Use the Python script at `scripts/to_datamap.py` to create a markers group for usage in [DataMaps](https://support.wiki.gg/wiki/DataMaps):

```bash
python3 scripts/to_datamap.py path/to/your/presentsdump.txt
```

This will output a file titled `presents.json` in the directory the `to_datamap.py` script is run from. The array in this file can then be copy/pasted into a group under the `"markers"` object in MediaWiki.