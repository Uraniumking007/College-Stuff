using System;
using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditorInternal;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Cipat.Editor
{
    public static class CipatBreakableBootstrap
    {
        const string LogPrefix = "[CIPAT Breakable]";
        const string SmashScene = "Assets/Scenes/CIPAT_SmashHouse.unity";
        const string BreakableTag = "Breakable";
        const string DebrisPath = "Assets/CIPAT/Prefabs/DebrisChunk.prefab";
        const string GlassClipPath = "Assets/CIPAT/Audio/glass_break.wav";
        const string CeramicClipPath = "Assets/CIPAT/Audio/ceramic_thud.wav";
        const string WoodClipPath = "Assets/CIPAT/Audio/wood_thud.wav";

        // Prefer living-area-friendly small props from the nappin pack.
        static readonly string[] PreferNames =
        {
            "(Prb)LaunchTable_vase1",
            "(Prb)LaunchTable_vase2",
            "(Prb)LaunchTable_vase3",
            "(Prb)CoffeTable_smallPlant",
            "(Prb)Container1",
            "(Prb)Container2",
            "(Prb)Lamp",
        };

        static readonly string[] ExcludeHints =
        {
            "fridge", "sofa", "wardrobe", "wall", "floor", "ceiling", "door",
            "bed", "stove", "sink", "toilet", "island", "desk", "dresser",
            "media", "storage", "coat", "shelf", "mirror", "shoe", "vent",
            "light", "drawer", "chair", "pillow", "kitchen", "origin", "simulator",
            "bat", "launchtable", // bare LaunchTable (furniture), not vase
        };

        public static void Run()
        {
            try
            {
                Debug.Log($"{LogPrefix} Starting");
                EnsureBreakableTag();

                if (AssetDatabase.LoadAssetAtPath<SceneAsset>(SmashScene) == null)
                    throw new Exception($"Scene missing: {SmashScene}");

                var debris = AssetDatabase.LoadAssetAtPath<GameObject>(DebrisPath);
                if (debris == null)
                    throw new Exception($"Debris prefab missing: {DebrisPath}");

                var glass = AssetDatabase.LoadAssetAtPath<AudioClip>(GlassClipPath);
                var ceramic = AssetDatabase.LoadAssetAtPath<AudioClip>(CeramicClipPath);
                var wood = AssetDatabase.LoadAssetAtPath<AudioClip>(WoodClipPath);
                if (glass == null || ceramic == null || wood == null)
                    throw new Exception("One or more break audio clips missing under Assets/CIPAT/Audio");

                var scene = EditorSceneManager.OpenScene(SmashScene, OpenSceneMode.Single);
                var wired = new List<string>();

                foreach (var preferred in PreferNames)
                {
                    if (wired.Count >= 6)
                        break;

                    var go = FindByExactName(preferred);
                    if (go == null)
                    {
                        Debug.Log($"{LogPrefix} skip missing {preferred}");
                        continue;
                    }

                    if (go.GetComponentInChildren<BreakableObject>(true) != null)
                    {
                        Debug.Log($"{LogPrefix} already wired: {go.name}");
                        wired.Add(go.name + " (existing)");
                        continue;
                    }

                    if (IsExcluded(go.name))
                    {
                        Debug.Log($"{LogPrefix} excluded by name: {go.name}");
                        continue;
                    }

                    Wire(go, debris, glass, ceramic, wood);
                    wired.Add(Describe(go));
                }

                // Fallback scan if preferred list under-delivered.
                if (wired.Count < 4)
                {
                    foreach (var go in FindCandidates())
                    {
                        if (wired.Count >= 6)
                            break;
                        if (go.GetComponentInChildren<BreakableObject>(true) != null)
                            continue;
                        if (IsExcluded(go.name))
                            continue;
                        Wire(go, debris, glass, ceramic, wood);
                        wired.Add(Describe(go));
                    }
                }

                if (wired.Count < 4)
                    throw new Exception($"Only wired {wired.Count} smashables; need at least 4");

                EditorSceneManager.MarkSceneDirty(scene);
                EditorSceneManager.SaveScene(scene);
                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh();

                Debug.Log($"{LogPrefix} Complete — wired {wired.Count}:\n - " + string.Join("\n - ", wired));
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"{LogPrefix} FAILED: {ex}");
                EditorApplication.Exit(1);
            }
        }

        static void Wire(GameObject go, GameObject debris, AudioClip glass, AudioClip ceramic, AudioClip wood)
        {
            // Prefab instances must be unpacked so we can add Rigidbody / BreakableObject.
            if (PrefabUtility.IsPartOfPrefabInstance(go))
            {
                PrefabUtility.UnpackPrefabInstance(
                    PrefabUtility.GetOutermostPrefabInstanceRoot(go),
                    PrefabUnpackMode.Completely,
                    InteractionMode.AutomatedAction);
            }

            ClearStaticRecursive(go);

            var rb = go.GetComponent<Rigidbody>();
            if (rb == null)
                rb = go.AddComponent<Rigidbody>();
            rb.useGravity = true;
            rb.isKinematic = false;
            rb.interpolation = RigidbodyInterpolation.Interpolate;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousSpeculative;
            rb.mass = MassFor(go.name);

            EnsureNonTriggerCollider(go);

            // Strip duplicate child BoxColliders so root collider bounds stay clean.
            foreach (var c in go.GetComponentsInChildren<Collider>(true))
            {
                if (c.gameObject == go) continue;
                if (c is BoxCollider)
                    UnityEngine.Object.DestroyImmediate(c);
            }

            if (!string.IsNullOrEmpty(BreakableTag) && Array.IndexOf(InternalEditorUtility.tags, BreakableTag) >= 0)
                go.tag = BreakableTag;

            var br = go.GetComponent<BreakableObject>();
            if (br == null)
                br = go.AddComponent<BreakableObject>();

            var so = new SerializedObject(br);
            so.FindProperty("debrisPrefab").objectReferenceValue = debris;

            var profile = ProfileFor(go.name);
            so.FindProperty("breakSound").objectReferenceValue =
                profile.kind == "glass" ? glass : profile.kind == "ceramic" ? ceramic : wood;
            so.FindProperty("hapticAmplitude").floatValue = profile.amp;
            so.FindProperty("hapticDuration").floatValue = profile.duration;
            so.FindProperty("breakSpeedThreshold").floatValue = profile.threshold;
            so.ApplyModifiedPropertiesWithoutUndo();

            EditorUtility.SetDirty(go);
            Debug.Log($"{LogPrefix} wired {go.name} sound={profile.kind} mass={rb.mass} thr={profile.threshold}");
        }

        static void EnsureNonTriggerCollider(GameObject go)
        {
            var cols = go.GetComponentsInChildren<Collider>(true);
            bool hasSolid = cols.Any(c => c != null && !c.isTrigger);
            if (hasSolid)
            {
                // Prefer a solid collider on the root so RequireComponent(Collider) is satisfied.
                if (go.GetComponent<Collider>() == null)
                {
                    var box = go.AddComponent<BoxCollider>();
                    FitBoxToRenderers(go, box);
                }
                return;
            }

            var added = go.AddComponent<BoxCollider>();
            FitBoxToRenderers(go, added);
        }

        static void FitBoxToRenderers(GameObject go, BoxCollider box)
        {
            var renderers = go.GetComponentsInChildren<Renderer>(true);
            if (renderers.Length == 0)
            {
                box.center = Vector3.zero;
                box.size = Vector3.one * 0.2f;
                return;
            }

            var bounds = renderers[0].bounds;
            for (int i = 1; i < renderers.Length; i++)
                bounds.Encapsulate(renderers[i].bounds);

            var t = go.transform;
            var localCenter = t.InverseTransformPoint(bounds.center);
            var localSize = t.InverseTransformVector(bounds.size);
            box.center = localCenter;
            box.size = new Vector3(Mathf.Abs(localSize.x), Mathf.Abs(localSize.y), Mathf.Abs(localSize.z));
            if (box.size.sqrMagnitude < 1e-6f)
                box.size = Vector3.one * 0.2f;
        }

        static void ClearStaticRecursive(GameObject go)
        {
            GameObjectUtility.SetStaticEditorFlags(go, 0);
            foreach (Transform child in go.transform)
                ClearStaticRecursive(child.gameObject);
        }

        static float MassFor(string name)
        {
            var n = name.ToLowerInvariant();
            if (n.Contains("vase") || n.Contains("plant")) return 0.4f;
            if (n.Contains("lamp")) return 0.8f;
            return 0.6f; // containers
        }

        struct Profile
        {
            public string kind;
            public float amp;
            public float duration;
            public float threshold;
        }

        static Profile ProfileFor(string name)
        {
            var n = name.ToLowerInvariant();
            if (n.Contains("vase") || n.Contains("glass"))
                return new Profile { kind = "glass", amp = 0.7f, duration = 0.08f, threshold = 1.2f };
            if (n.Contains("plant") || n.Contains("ceramic"))
                return new Profile { kind = "ceramic", amp = 0.7f, duration = 0.08f, threshold = 1.3f };
            // wood / container / lamp base
            return new Profile { kind = "wood", amp = 0.4f, duration = 0.12f, threshold = 1.7f };
        }

        static string Describe(GameObject go)
        {
            var br = go.GetComponent<BreakableObject>();
            var so = new SerializedObject(br);
            var clip = so.FindProperty("breakSound").objectReferenceValue as AudioClip;
            return $"{go.name} [{(clip != null ? clip.name : "?")}] @ {go.transform.position}";
        }

        static GameObject FindByExactName(string name)
        {
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                var t = FindTransform(root.transform, name);
                if (t != null)
                    return t.gameObject;
            }
            return null;
        }

        static Transform FindTransform(Transform parent, string name)
        {
            if (parent.name == name)
                return parent;
            for (int i = 0; i < parent.childCount; i++)
            {
                var found = FindTransform(parent.GetChild(i), name);
                if (found != null)
                    return found;
            }
            return null;
        }

        static IEnumerable<GameObject> FindCandidates()
        {
            var keys = new[] { "vase", "lamp", "container", "smallplant", "plant" };
            var list = new List<GameObject>();
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
                Collect(root.transform, keys, list);
            return list;
        }

        static void Collect(Transform t, string[] keys, List<GameObject> list)
        {
            var lower = t.name.ToLowerInvariant();
            if (keys.Any(k => lower.Contains(k)) && !IsExcluded(t.name))
                list.Add(t.gameObject);
            for (int i = 0; i < t.childCount; i++)
                Collect(t.GetChild(i), keys, list);
        }

        static bool IsExcluded(string name)
        {
            var n = name.ToLowerInvariant().Replace("(prb)", "").Replace(" ", "");
            // Allow LaunchTable_vase* / CoffeTable_smallPlant; block bare LaunchTable / CoffeTable.
            if (n == "launchtable" || n == "coffetable")
                return true;
            foreach (var h in ExcludeHints)
            {
                if (h == "launchtable")
                    continue; // handled above
                if (h == "light" && n.Contains("lamp"))
                    continue;
                if (n.Contains(h) && !n.Contains("vase") && !n.Contains("container") && !n.Contains("plant") && !n.Contains("lamp"))
                    return true;
            }
            return false;
        }

        static void EnsureBreakableTag()
        {
            var tags = InternalEditorUtility.tags;
            if (Array.IndexOf(tags, BreakableTag) >= 0)
            {
                Debug.Log($"{LogPrefix} tag '{BreakableTag}' already exists");
                return;
            }

            InternalEditorUtility.AddTag(BreakableTag);
            var tagManager = new SerializedObject(
                AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset")[0]);
            tagManager.Update();
            EditorUtility.SetDirty(tagManager.targetObject);
            AssetDatabase.SaveAssets();
            Debug.Log($"{LogPrefix} added tag '{BreakableTag}'");
        }
    }
}
