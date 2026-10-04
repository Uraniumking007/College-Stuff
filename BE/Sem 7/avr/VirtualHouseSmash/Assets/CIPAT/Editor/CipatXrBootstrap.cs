using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Cipat.Editor
{
    public static class CipatXrBootstrap
    {
        const string LogPrefix = "[CIPAT XR]";
        const string SourceScene = "Assets/nappin/HouseInteriorPack/HouseInteriorPack.unity";
        const string SmashScene = "Assets/Scenes/CIPAT_SmashHouse.unity";
        const string XrOriginPrefab =
            "Assets/Samples/XR Interaction Toolkit/3.6.1/Starter Assets/Prefabs/XR Origin (XR Rig).prefab";
        const string DeviceSimPrefab =
            "Assets/Samples/XR Interaction Toolkit/3.6.1/XR Device Simulator/XR Device Simulator.prefab";
        // Living room near CoffeTable (-13.02, 0.33, -6.89) / CornerSofa
        static readonly Vector3 XrOriginPosition = new Vector3(-12.5f, 0.02f, -5.0f);
        static readonly Quaternion XrOriginRotation = Quaternion.Euler(0f, 200f, 0f);

        public static void Run()
        {
            try
            {
                Debug.Log($"{LogPrefix} Starting bootstrap");
                EnableOpenXrStandalone();
                ImportXritSamples();
                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh();
                Debug.Log($"{LogPrefix} Bootstrap complete");
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"{LogPrefix} FAILED: {ex}");
                EditorApplication.Exit(1);
            }
        }

        public static void SetupSmashHouseScene()
        {
            try
            {
                Debug.Log($"{LogPrefix} SetupSmashHouseScene start");
                EnsureSmashSceneCopy();
                AssetDatabase.Refresh();

                var scene = EditorSceneManager.OpenScene(SmashScene, OpenSceneMode.Single);
                var origin = EnsurePrefabInstance(XrOriginPrefab, "XR Origin (XR Rig)", XrOriginPosition, XrOriginRotation);
                EnsurePrefabInstance(DeviceSimPrefab, "XR Device Simulator", Vector3.zero, Quaternion.identity);
                DisableConflictingCameras(origin);
                EditorSceneManager.MarkSceneDirty(scene);
                EditorSceneManager.SaveScene(scene);
                AssetDatabase.SaveAssets();
                Debug.Log($"{LogPrefix} SetupSmashHouseScene complete at {XrOriginPosition}");
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"{LogPrefix} SetupSmashHouseScene FAILED: {ex}");
                EditorApplication.Exit(1);
            }
        }

        static void EnsureSmashSceneCopy()
        {
            EnsureFolder("Assets/Scenes");
            if (File.Exists(SmashScene))
            {
                Debug.Log($"{LogPrefix} smash scene already exists");
                return;
            }
            if (!File.Exists(SourceScene))
                throw new Exception($"Source scene missing: {SourceScene}");
            if (!AssetDatabase.CopyAsset(SourceScene, SmashScene))
                throw new Exception($"Failed to copy {SourceScene} -> {SmashScene}");
            Debug.Log($"{LogPrefix} copied smash scene -> {SmashScene}");
        }

        static GameObject EnsurePrefabInstance(string prefabPath, string objectName, Vector3 position, Quaternion rotation)
        {
            var existing = FindRootByName(objectName);
            if (existing != null)
            {
                Debug.Log($"{LogPrefix} already present: {objectName}");
                return existing;
            }

            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(prefabPath);
            if (prefab == null)
                throw new Exception($"Prefab missing: {prefabPath}");

            var instance = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
            instance.name = objectName;
            instance.transform.SetPositionAndRotation(position, rotation);
            Undo.RegisterCreatedObjectUndo(instance, $"CIPAT add {objectName}");
            Debug.Log($"{LogPrefix} instantiated {objectName} at {position}");
            return instance;
        }

        static GameObject FindRootByName(string objectName)
        {
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                if (root.name == objectName || root.name.StartsWith(objectName, StringComparison.Ordinal))
                    return root;
            }
            return null;
        }

        static void DisableConflictingCameras(GameObject xrOrigin)
        {
            var cameras = UnityEngine.Object.FindObjectsByType<Camera>(FindObjectsInactive.Include, FindObjectsSortMode.None);
            int disabled = 0;
            foreach (var cam in cameras)
            {
                if (xrOrigin != null && cam.transform.IsChildOf(xrOrigin.transform))
                    continue;
                if (cam.CompareTag("MainCamera") || cam.gameObject.name is "Main Camera" or "Camera")
                {
                    if (cam.gameObject.activeSelf)
                    {
                        cam.gameObject.SetActive(false);
                        disabled++;
                        Debug.Log($"{LogPrefix} disabled camera {cam.gameObject.name}");
                    }
                }
            }
            Debug.Log($"{LogPrefix} disabled {disabled} conflicting cameras");
        }

        static void EnableOpenXrStandalone()
        {
            var generalSettingsType = FindType("Unity.XR.Management.XRGeneralSettingsPerBuildTarget, Unity.XR.Management.Editor")
                ?? FindType("UnityEditor.XR.Management.XRGeneralSettingsPerBuildTarget, Unity.XR.Management.Editor");
            var managerSettingsType = FindType("UnityEngine.XR.Management.XRManagerSettings, Unity.XR.Management");
            var generalSettingsRuntimeType = FindType("UnityEngine.XR.Management.XRGeneralSettings, Unity.XR.Management");
            var openXrLoaderType = FindType("UnityEngine.XR.OpenXR.OpenXRLoader, Unity.XR.OpenXR");

            if (generalSettingsType == null || managerSettingsType == null || generalSettingsRuntimeType == null || openXrLoaderType == null)
                throw new Exception($"Missing XR types gs={generalSettingsType} ms={managerSettingsType} runtime={generalSettingsRuntimeType} loader={openXrLoaderType}");

            EnsureFolder("Assets/XR");
            EnsureFolder("Assets/XR/Settings");
            EnsureFolder("Assets/XR/Loaders");

            var perBuildTarget = LoadOrCreateAsset(generalSettingsType, "Assets/XR/XRGeneralSettingsPerBuildTarget.asset");
            var manager = LoadOrCreateAsset(managerSettingsType, "Assets/XR/Settings/Standalone XR Manager Settings.asset");
            var general = LoadOrCreateAsset(generalSettingsRuntimeType, "Assets/XR/Settings/Standalone XR General Settings.asset");
            var loader = LoadOrCreateAsset(openXrLoaderType, "Assets/XR/Loaders/Open XR Loader.asset");

            SetMember(general, "m_LoaderManagerInstance", manager);
            SetMember(general, "Manager", manager);
            AssignBuildTarget(perBuildTarget, BuildTargetGroup.Standalone, general);

            var metadataStore = FindType("UnityEditor.XR.Management.Metadata.XRPackageMetadataStore, Unity.XR.Management.Editor");
            bool assigned = false;
            if (metadataStore != null)
            {
                var assign = metadataStore.GetMethod("AssignLoader", BindingFlags.Public | BindingFlags.Static);
                if (assign != null)
                {
                    try
                    {
                        assigned = (bool)assign.Invoke(null, new object[] { manager, openXrLoaderType.FullName, BuildTargetGroup.Standalone });
                        Debug.Log($"{LogPrefix} AssignLoader returned {assigned}");
                    }
                    catch (Exception e)
                    {
                        Debug.LogWarning($"{LogPrefix} AssignLoader failed: {e.InnerException ?? e}");
                    }
                }
            }

            if (!assigned)
            {
                var loaders = new List<UnityEngine.Object> { loader };
                SetMember(manager, "m_Loaders", loaders);
                TryCall(manager, "TrySetLoaders", new object[] { loaders });
                TryCall(manager, "TryAddLoader", new object[] { loader });
                EditorUtility.SetDirty(manager);
            }

            EditorUtility.SetDirty(general);
            EditorUtility.SetDirty(perBuildTarget);
            EditorUtility.SetDirty(loader);
            EditorBuildSettings.AddConfigObject("com.unity.xr.management.loader_settings", perBuildTarget, true);

            AssetDatabase.SaveAssets();
            Debug.Log($"{LogPrefix} OpenXR loader wired for Standalone");
        }

        static void ImportXritSamples()
        {
            var packageInfoType = FindType("UnityEditor.PackageManager.PackageInfo, UnityEditor.CoreModule")
                ?? FindType("UnityEditor.PackageManager.PackageInfo, UnityEditor");
            if (packageInfoType == null)
                throw new Exception("PackageInfo type not found");

            var getAll = packageInfoType.GetMethod("GetAllRegisteredPackages", BindingFlags.Public | BindingFlags.Static)
                ?? packageInfoType.GetMethod("GetAll", BindingFlags.Public | BindingFlags.Static);
            object[] packages;
            if (getAll != null)
            {
                packages = ((Array)getAll.Invoke(null, null)).Cast<object>().ToArray();
            }
            else
            {
                throw new Exception("No GetAllRegisteredPackages");
            }

            object xrit = null;
            foreach (var pkg in packages)
            {
                var name = (string)pkg.GetType().GetProperty("name").GetValue(pkg);
                if (name == "com.unity.xr.interaction.toolkit")
                {
                    xrit = pkg;
                    break;
                }
            }
            if (xrit == null)
                throw new Exception("XR Interaction Toolkit package not registered yet");

            var version = (string)xrit.GetType().GetProperty("version").GetValue(xrit);
            var resolvedPath = (string)xrit.GetType().GetProperty("resolvedPath").GetValue(xrit);
            Debug.Log($"{LogPrefix} XRIT {version} at {resolvedPath}");

            string[] sampleNames = { "Starter Assets", "XR Device Simulator", "XR Interaction Simulator" };
            var samplesRoot = Path.Combine(resolvedPath, "Samples~");
            if (!Directory.Exists(samplesRoot))
                throw new Exception($"Samples~ missing at {samplesRoot}");

            foreach (var sampleName in sampleNames)
            {
                var src = Path.Combine(samplesRoot, sampleName);
                if (!Directory.Exists(src))
                {
                    Debug.LogWarning($"{LogPrefix} sample folder missing: {sampleName}");
                    continue;
                }

                var destRel = $"Assets/Samples/XR Interaction Toolkit/{version}/{sampleName}";
                var destAbs = Path.Combine(Directory.GetCurrentDirectory(), destRel);
                if (Directory.Exists(destAbs))
                {
                    Debug.Log($"{LogPrefix} sample already present: {destRel}");
                    continue;
                }

                Directory.CreateDirectory(Path.GetDirectoryName(destAbs)!);
                CopyDirectory(src, destAbs);
                Debug.Log($"{LogPrefix} imported sample -> {destRel}");
            }

            AssetDatabase.Refresh();
        }

        static void AssignBuildTarget(UnityEngine.Object perBuildTarget, BuildTargetGroup group, UnityEngine.Object general)
        {
            var so = new SerializedObject(perBuildTarget);
            var keys = so.FindProperty("m_Keys");
            var values = so.FindProperty("m_Values");
            if (keys != null && values != null)
            {
                int idx = -1;
                for (int i = 0; i < keys.arraySize; i++)
                {
                    if (keys.GetArrayElementAtIndex(i).intValue == (int)group)
                    {
                        idx = i;
                        break;
                    }
                }
                if (idx < 0)
                {
                    idx = keys.arraySize;
                    keys.arraySize++;
                    values.arraySize++;
                    keys.GetArrayElementAtIndex(idx).intValue = (int)group;
                }
                values.GetArrayElementAtIndex(idx).objectReferenceValue = general;
                so.ApplyModifiedPropertiesWithoutUndo();
                return;
            }

            var method = perBuildTarget.GetType().GetMethod("SetSettingsForBuildTarget", BindingFlags.Public | BindingFlags.Instance | BindingFlags.Static);
            if (method != null)
            {
                if (method.IsStatic)
                    method.Invoke(null, new object[] { group, general });
                else
                    method.Invoke(perBuildTarget, new object[] { group, general });
                return;
            }

            Debug.LogWarning($"{LogPrefix} Could not find SetSettingsForBuildTarget; relying on AssignLoader / manual fields");
        }

        static UnityEngine.Object LoadOrCreateAsset(Type type, string path)
        {
            var existing = AssetDatabase.LoadAssetAtPath(path, type);
            if (existing != null)
                return existing;
            EnsureFolder(Path.GetDirectoryName(path)!.Replace('\\', '/'));
            var asset = ScriptableObject.CreateInstance(type);
            AssetDatabase.CreateAsset(asset, path);
            return asset;
        }

        static void EnsureFolder(string assetPath)
        {
            assetPath = assetPath.Replace('\\', '/');
            if (AssetDatabase.IsValidFolder(assetPath))
                return;
            var parts = assetPath.Split('/');
            var cur = parts[0];
            for (int i = 1; i < parts.Length; i++)
            {
                var next = cur + "/" + parts[i];
                if (!AssetDatabase.IsValidFolder(next))
                    AssetDatabase.CreateFolder(cur, parts[i]);
                cur = next;
            }
        }

        static void SetMember(object obj, string name, object value)
        {
            var t = obj.GetType();
            var f = t.GetField(name, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            if (f != null)
            {
                f.SetValue(obj, value);
                return;
            }
            var p = t.GetProperty(name, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            if (p != null && p.CanWrite)
            {
                p.SetValue(obj, value);
            }
        }

        static void TryCall(object obj, string method, object[] args)
        {
            var m = obj.GetType().GetMethod(method, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
            if (m == null) return;
            try { m.Invoke(obj, args); } catch { /* ignore */ }
        }

        static Type FindType(string asmQualified)
        {
            var t = Type.GetType(asmQualified);
            if (t != null) return t;
            var comma = asmQualified.IndexOf(',');
            var name = comma > 0 ? asmQualified.Substring(0, comma).Trim() : asmQualified;
            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                t = asm.GetType(name);
                if (t != null) return t;
            }
            return null;
        }

        static void CopyDirectory(string src, string dest)
        {
            Directory.CreateDirectory(dest);
            foreach (var file in Directory.GetFiles(src))
            {
                var name = Path.GetFileName(file);
                if (name == ".DS_Store") continue;
                File.Copy(file, Path.Combine(dest, name), true);
            }
            foreach (var dir in Directory.GetDirectories(src))
            {
                CopyDirectory(dir, Path.Combine(dest, Path.GetFileName(dir)));
            }
        }
    }
}
