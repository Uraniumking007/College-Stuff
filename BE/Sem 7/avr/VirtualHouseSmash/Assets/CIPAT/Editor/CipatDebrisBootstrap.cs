using System;
using UnityEditor;
using UnityEngine;

namespace Cipat.Editor
{
    public static class CipatDebrisBootstrap
    {
        const string LogPrefix = "[CIPAT Debris]";
        const string PrefabDir = "Assets/CIPAT/Prefabs";
        const string PrefabPath = PrefabDir + "/DebrisChunk.prefab";
        static readonly Vector3 ChunkScale = new Vector3(0.05f, 0.05f, 0.05f);

        public static void Run()
        {
            try
            {
                Debug.Log($"{LogPrefix} Starting");
                EnsureFolder(PrefabDir);

                var root = GameObject.CreatePrimitive(PrimitiveType.Cube);
                root.name = "DebrisChunk";
                root.transform.localScale = ChunkScale;

                var rb = root.GetComponent<Rigidbody>();
                if (rb == null)
                    rb = root.AddComponent<Rigidbody>();
                rb.useGravity = true;
                rb.isKinematic = false;
                rb.collisionDetectionMode = CollisionDetectionMode.Discrete;
                rb.interpolation = RigidbodyInterpolation.Interpolate;
                rb.mass = 0.05f;

                // Keep BoxCollider from CreatePrimitive
                var prefab = PrefabUtility.SaveAsPrefabAsset(root, PrefabPath);
                UnityEngine.Object.DestroyImmediate(root);
                if (prefab == null)
                    throw new Exception($"Failed to save prefab at {PrefabPath}");

                AssetDatabase.SaveAssets();
                AssetDatabase.Refresh();
                Debug.Log($"{LogPrefix} Complete — prefab={PrefabPath} scale={ChunkScale}");
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"{LogPrefix} FAILED: {ex}");
                EditorApplication.Exit(1);
            }
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
