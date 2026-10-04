using BepInEx;
using BepInEx.Logging;
using UnityEngine;
using System;
using System.Collections.Generic;
using System.IO;

namespace WobbyLifeWiki_Presents;

[BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
public class Plugin : BaseUnityPlugin
{
    internal static new ManualLogSource Logger;

    internal static List<PluginPresent> presents = new List<PluginPresent>();

    private void Awake()
    {
        // Plugin startup logic
        Logger = base.Logger;
        Logger.LogInfo($"Plugin {MyPluginInfo.PLUGIN_GUID} is loaded!");
    }

    private void Update()
    {
        if (Input.GetKeyDown(KeyCode.P))
        {
            Logger.LogInfo("Starting present location dump...");
            WizardTentManager wizardTentManager = FindObjectOfType<WizardTentManager>();

            // populate presents list
            Action<WizardPresent> action = new Action<WizardPresent>(AddPresent);
            Array.ForEach(wizardTentManager.GetWizardPresentData().GetWizardPresents(), action);

            // dump presents list to a file
            string filePath = Path.Combine(Paths.PluginPath, "presentsdump.txt");
            using (StreamWriter sw = new StreamWriter(filePath, false)) {
                foreach (PluginPresent present in presents)
                {
                    sw.WriteLine(present);
                };
            }

            Logger.LogInfo("Finished present location dump!");
        }
    }

    private static void AddPresent(WizardPresent present)
    {
        presents.Add(new PluginPresent(present.displayName, present.presentGuidStr, present.presentPosition));
    }
}

// i would make this a record but C# gets mad at me and i don't wanna make a workaround
public class PluginPresent
{
    public string Name { get; }
    public string GuidStr { get; }
    public Vector3 Position { get; }

    public PluginPresent(string name, string guidStr, Vector3 position)
    {
        Name = name;
        GuidStr = guidStr;
        Position = position;
    }

    public override string ToString()
    {
        return $"Name: {Name}, GUID: {GuidStr}, Position: {Position.x:F2}, {Position.y:F2}, {Position.z:F2}";
    }
}