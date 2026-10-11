using BepInEx;
using BepInEx.Logging;
using UnityEngine;
using UnityEngine.AddressableAssets;
using UnityEngine.ResourceManagement.AsyncOperations;
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
            StartCoroutine(DumpPresents());
        }
    }

    private System.Collections.IEnumerator DumpPresents()
    {
        Logger.LogInfo("Starting present location dump...");

        WizardTentManager wizardTentManager = FindObjectOfType<WizardTentManager>();

        if (wizardTentManager == null)
        {
            Logger.LogError("Could not find WizardTentManager!");
            yield break;
        }

        presents.Clear();

        WizardPresent[] wizardPresents = wizardTentManager.GetWizardPresentData().GetWizardPresents();

        foreach (WizardPresent present in wizardPresents)
        {
            yield return StartCoroutine(AddPresent(present));
        }

        string filePath = Path.Combine(Paths.PluginPath, "presentsdump.txt");

        using (StreamWriter sw = new StreamWriter(filePath, false))
        {
            foreach (PluginPresent present in presents)
            {
                sw.WriteLine(present);
            }
        }

        Logger.LogInfo($"Dumped {presents.Count} presents to {filePath}");
    }

    private static System.Collections.IEnumerator AddPresent(WizardPresent present)
    {
        AsyncOperationHandle<Texture> handle = Addressables.LoadAssetAsync<Texture>(present.presentTextureReference);
        yield return handle;

        string textureName = "Tile000"; // default texture name in case of failure, see https://wobblylife.wiki.gg/wiki/File:Tile000.png
        if (handle.Status == AsyncOperationStatus.Succeeded)
        {
            Texture texture = handle.Result;

            textureName = texture.name;

            Addressables.Release(handle);
        }
        else
        {
            Logger.LogError($"Failed to load present texture for {present.displayName}.");

            Addressables.Release(handle);
        }

        presents.Add(new PluginPresent(present.displayName,present.presentGuidStr,present.PresentAdjustedPosition,textureName));
    }
}

// i would make this a record but C# gets mad at me and i don't wanna make a workaround
public class PluginPresent
{
    public string Name { get; }
    public string GuidStr { get; }
    public Vector3 Position { get; }
    public string TextureName { get; }

    public PluginPresent(string name, string guidStr, Vector3 position, string textureName)
    {
        Name = name;
        GuidStr = guidStr;
        Position = position;
        TextureName = textureName;
    }

    public override string ToString()
    {
        return $"Name:{Name};GUID:{GuidStr};Position:{Position.x:F2},{Position.y:F2},{Position.z:F2};Texture:{TextureName}";
    }
}