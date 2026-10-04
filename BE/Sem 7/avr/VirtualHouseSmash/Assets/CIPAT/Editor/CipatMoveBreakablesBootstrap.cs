using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;

namespace Cipat.Editor
{
    public static class CipatMoveBreakablesBootstrap
    {
        const string ScenePath = "Assets/Scenes/CIPAT_SmashHouse.unity";
        static readonly Vector3 Anchor = new Vector3(-13.0f, 0.95f, -6.7f);

        // Offsets around the bat/coffee table so props are reachable in demo.
        static readonly Vector3[] Offsets =
        {
            new Vector3(-0.35f, 0.00f,  0.15f),
            new Vector3( 0.25f, 0.00f,  0.20f),
            new Vector3(-0.15f, 0.00f, -0.25f),
            new Vector3( 0.30f, 0.00f, -0.15f),
            new Vector3(-0.40f, 0.00f, -0.05f),
            new Vector3( 0.10f, 0.00f,  0.35f),
            new Vector3( 0.45f, 0.00f,  0.05f),
        };

        public static void Run()
        {
            try
            {
                var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);
                var breakables = UnityEngine.Object.FindObjectsByType<Cipat.BreakableObject>(
                    FindObjectsInactive.Include, FindObjectsSortMode.None);

                if (breakables == null || breakables.Length == 0)
                    throw new Exception("No BreakableObject components found in scene.");

                // Stable order by name
                var list = new List<Cipat.BreakableObject>(breakables);
                list.Sort((a, b) => string.CompareOrdinal(a.gameObject.name, b.gameObject.name));

                for (int i = 0; i < list.Count; i++)
                {
                    var go = list[i].gameObject;
                    var offset = Offsets[i % Offsets.Length];
                    var pos = Anchor + offset;
                    go.transform.position = pos;
                    Debug.Log($"[CIPAT] Moved {go.name} -> {pos}");
                }

                EditorSceneManager.MarkSceneDirty(scene);
                EditorSceneManager.SaveScene(scene);
                AssetDatabase.SaveAssets();
                Debug.Log($"[CIPAT] Moved {list.Count} breakables near bat.");
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"[CIPAT] Move breakables failed: {ex}");
                EditorApplication.Exit(1);
            }
        }
    }
}
