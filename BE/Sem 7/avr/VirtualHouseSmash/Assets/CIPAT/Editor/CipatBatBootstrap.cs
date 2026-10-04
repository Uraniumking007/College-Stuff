using System;
using System.IO;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEditorInternal;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.XR.Interaction.Toolkit.Interactables;

namespace Cipat.Editor
{
    public static class CipatBatBootstrap
    {
        const string LogPrefix = "[CIPAT Bat]";
        const string SmashScene = "Assets/Scenes/CIPAT_SmashHouse.unity";
        const string PrefabDir = "Assets/CIPAT/Prefabs";
        const string PrefabPath = PrefabDir + "/Bat.prefab";
        const string MaterialDir = "Assets/CIPAT/Materials";
        const string MaterialPath = MaterialDir + "/BatHighlight.mat";
        const string WeaponTag = "Weapon";

        // Coffee table ~ (-13.02, 0.33, -6.89); thick bright bat so Device Simulator demos can see it
        const float TableTopY = 0.70f;
        static readonly Vector3 BatPosition = new Vector3(-13.0f, 1.0f, -6.7f);
        static readonly Quaternion BatRotation = Quaternion.Euler(0f, 25f, 90f);
        // Unit cylinder radius 0.5 → world radius 0.06; length ~0.9m
        static readonly Vector3 BatScale = new Vector3(0.12f, 0.45f, 0.12f);
        static readonly Color BatColor = new Color(1f, 0.35f, 0.05f, 1f);

        public static void Run()
        {
            try
            {
                Debug.Log($"{LogPrefix} Starting");
                EnsureWeaponTag();
                EnsureFolder(PrefabDir);
                EnsureFolder(MaterialDir);

                var prefab = BuildOrUpdateBatPrefab();
                PlaceBatInScene(prefab);

                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh();
                Debug.Log($"{LogPrefix} Complete — prefab={PrefabPath} scene instance at {BatPosition}");
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"{LogPrefix} FAILED: {ex}");
                EditorApplication.Exit(1);
            }
        }

        static GameObject BuildOrUpdateBatPrefab()
        {
            var root = GameObject.CreatePrimitive(PrimitiveType.Cylinder);
            root.name = "Bat";
            root.tag = WeaponTag;
            root.transform.localScale = BatScale;

            var renderer = root.GetComponent<MeshRenderer>();
            if (renderer != null)
                renderer.sharedMaterial = EnsureBatMaterial();

            // CreatePrimitive already adds CapsuleCollider matching the cylinder
            var capsule = root.GetComponent<CapsuleCollider>();
            if (capsule == null)
                capsule = root.AddComponent<CapsuleCollider>();
            capsule.direction = 1; // Y
            capsule.height = 2f;
            capsule.radius = 0.5f;
            capsule.center = Vector3.zero;

            var rb = root.GetComponent<Rigidbody>();
            if (rb == null)
                rb = root.AddComponent<Rigidbody>();
            rb.useGravity = false;
            rb.isKinematic = true;
            rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
            rb.interpolation = RigidbodyInterpolation.Interpolate;
            rb.mass = 1.2f;

            var grab = root.GetComponent<XRGrabInteractable>();
            if (grab == null)
                grab = root.AddComponent<XRGrabInteractable>();
            grab.movementType = XRBaseInteractable.MovementType.VelocityTracking;
            grab.throwOnDetach = true;

            if (root.GetComponent<Cipat.GrabPhysicsToggle>() == null)
                root.AddComponent<Cipat.GrabPhysicsToggle>();

            EnsureFolder(PrefabDir);
            var prefab = PrefabUtility.SaveAsPrefabAsset(root, PrefabPath);
            UnityEngine.Object.DestroyImmediate(root);
            if (prefab == null)
                throw new Exception($"Failed to save prefab at {PrefabPath}");

            Debug.Log($"{LogPrefix} Saved prefab {PrefabPath}");
            return prefab;
        }

        static Material EnsureBatMaterial()
        {
            var mat = AssetDatabase.LoadAssetAtPath<Material>(MaterialPath);
            if (mat == null)
            {
                var shader = Shader.Find("Universal Render Pipeline/Lit")
                             ?? Shader.Find("HDRP/Lit")
                             ?? Shader.Find("Standard");
                if (shader == null)
                    throw new Exception("No Lit/Standard shader found for bat material");
                mat = new Material(shader) { name = "BatHighlight" };
                AssetDatabase.CreateAsset(mat, MaterialPath);
            }

            if (mat.HasProperty("_BaseColor"))
                mat.SetColor("_BaseColor", BatColor);
            if (mat.HasProperty("_Color"))
                mat.SetColor("_Color", BatColor);
            if (mat.HasProperty("_EmissionColor"))
            {
                mat.EnableKeyword("_EMISSION");
                mat.SetColor("_EmissionColor", BatColor * 0.35f);
            }

            EditorUtility.SetDirty(mat);
            return mat;
        }

        static void PlaceBatInScene(GameObject prefab)
        {
            if (!File.Exists(Path.Combine(Directory.GetCurrentDirectory(), SmashScene)))
            {
                // Unity asset path check
            }
            if (AssetDatabase.LoadAssetAtPath<SceneAsset>(SmashScene) == null && !File.Exists(SmashScene))
                throw new Exception($"Scene missing: {SmashScene}");

            var scene = EditorSceneManager.OpenScene(SmashScene, OpenSceneMode.Single);

            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                if (root.name == "Bat" || root.name.StartsWith("Bat ", StringComparison.Ordinal))
                {
                    Debug.Log($"{LogPrefix} removing existing {root.name}");
                    UnityEngine.Object.DestroyImmediate(root);
                }
            }

            var instance = (GameObject)PrefabUtility.InstantiatePrefab(prefab);
            instance.name = "Bat";
            instance.tag = WeaponTag;
            instance.transform.SetPositionAndRotation(BatPosition, BatRotation);
            SeatOnTable(instance);
            Undo.RegisterCreatedObjectUndo(instance, "CIPAT add Bat");

            EditorSceneManager.MarkSceneDirty(scene);
            EditorSceneManager.SaveScene(scene);
            Debug.Log($"{LogPrefix} Placed Bat instance at {instance.transform.position}");
        }

        static void SeatOnTable(GameObject bat)
        {
            Physics.SyncTransforms();
            var col = bat.GetComponent<Collider>();
            if (col == null)
                return;

            // Rest collider bottom on tabletop + small clearance so the thick mesh stays above.
            const float clearance = 0.04f;
            float bottom = col.bounds.min.y;
            float delta = (TableTopY + clearance) - bottom;
            bat.transform.position += new Vector3(0f, delta, 0f);
            Physics.SyncTransforms();
            Debug.Log(
                $"{LogPrefix} Seated bat -> {bat.transform.position} (bottom={col.bounds.min.y:F3}, target={TableTopY + clearance:F2})");
        }

        static void EnsureWeaponTag()
        {
            var tags = InternalEditorUtility.tags;
            if (Array.IndexOf(tags, WeaponTag) >= 0)
            {
                Debug.Log($"{LogPrefix} tag '{WeaponTag}' already exists");
                return;
            }

            InternalEditorUtility.AddTag(WeaponTag);
            // Force TagManager dirty/save
            var tagManager = new SerializedObject(
                AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset")[0]);
            tagManager.Update();
            EditorUtility.SetDirty(tagManager.targetObject);
            AssetDatabase.SaveAssets();
            Debug.Log($"{LogPrefix} added tag '{WeaponTag}'");
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
    }
}
