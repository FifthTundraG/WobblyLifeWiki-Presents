# WobblyLifeWiki-Presents
Creates the data for the Presents page on the Wobbly Life Wiki.

## Usage
You will need to install BepInEx 5 and place the built DLL file into the `BepInEx/plugins/` folder in your game instance. RubberBandGames also recently started destroying the BepInEx manager `GameObject`, which means you will also need to update your `BepInEx/config/BepInEx.cfg` file to say this:
```yaml
...
[Chainloader]
...
HideManagerGameObject = true
...
```