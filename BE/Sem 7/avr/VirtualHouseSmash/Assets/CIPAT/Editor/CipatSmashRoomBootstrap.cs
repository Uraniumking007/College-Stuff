using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Cipat.Editor
{
    /// <summary>
    /// Task 2: delete House Interior and scaffold a ~6x6 JC_LP smash-room shell.
    /// Door / sofa / console / TV placement is Task 3+.
    /// </summary>
    public static class CipatSmashRoomBootstrap
    {
        const string LogPrefix = "[CIPAT Room]";
        const string ScenePath = "Assets/Scenes/CIPAT_SmashHouse.unity";
        const string FloorPrefabPath = "Assets/JC_LP_House_Lite/Prefabs/SM_Buildings_Floor_01.prefab";
        const string WallPrefabPath = "Assets/JC_LP_House_Lite/Prefabs/SM_Buildings_Wall_Interior_15_T1.prefab";
        // Reserved for Task 3.
        const string DoorPrefabPath = "Assets/nappin/HouseInteriorPack/Prefabs/(Prb)Door.prefab";
        const string SofaPrefabPath = "Assets/nappin/HouseInteriorPack/Prefabs/(Prb)Sofa.prefab";
        const string ConsolePrefabPath = "Assets/nappin/HouseInteriorPack/Prefabs/(Prb)MediaConsole.prefab";

        const string RoomRootName = "CIPAT_SmashRoom";

        // RoomOrigin = southwest corner of the 6x6 floor AABB (world).
        // Near the existing coffee-table cluster (~-13, y, ~-7) so smashables stay reachable.
        static readonly Vector3 RoomOrigin = new Vector3(-13f, 0f, -8f);
        const float TileSize = 3f;
        const float RoomSize = 6f;
        const float WallHeight = 3f;
        const float DoorGap = 1.2f;

        public static void Run()
        {
            try
            {
                Debug.Log($"{LogPrefix} Starting");
                // Keep Task-3 path constants referenced.
                Debug.Log($"{LogPrefix} Task3 paths reserved: door={DoorPrefabPath} sofa={SofaPrefabPath} console={ConsolePrefabPath}");

                var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

                var preserved = CollectAndDetachPreserved();
                DeleteHouseInterior();
                DeleteOrphanHouseLights();

                var room = RebuildRoomRoot();
                BuildFloor(room);
                BuildWalls(room);
                BuildRoof(room);

                foreach (var go in preserved)
                {
                    if (go != null)
                        Debug.Log($"{LogPrefix} Preserved: {go.name} @ {go.transform.position}");
                }

                EditorSceneManager.MarkSceneDirty(scene);
                EditorSceneManager.SaveScene(scene);
                AssetDatabase.SaveAssets();
                Debug.Log($"{LogPrefix} Complete — {RoomRootName} SW origin {RoomOrigin}");
                EditorApplication.Exit(0);
            }
            catch (Exception ex)
            {
                Debug.LogError($"{LogPrefix} FAILED: {ex}");
                EditorApplication.Exit(1);
            }
        }

        static List<GameObject> CollectAndDetachPreserved()
        {
            var list = new List<GameObject>();

            foreach (var b in UnityEngine.Object.FindObjectsByType<Cipat.BreakableObject>(
                         FindObjectsInactive.Include, FindObjectsSortMode.None))
            {
                if (b == null) continue;
                var go = SmashableRoot(b.transform);
                if (!list.Contains(go))
                    list.Add(go);
            }

            foreach (var t in UnityEngine.Object.FindObjectsByType<Transform>(
                         FindObjectsInactive.Include, FindObjectsSortMode.None))
            {
                if (t == null) continue;
                if (t.name != "(Prb)CoffeTable") continue;
                if (!list.Contains(t.gameObject))
                    list.Add(t.gameObject);
            }

            foreach (var go in list)
            {
                if (go == null) continue;
                var pos = go.transform.position;
                var rot = go.transform.rotation;
                var scale = go.transform.localScale;
                go.transform.SetParent(null, true);
                go.transform.SetPositionAndRotation(pos, rot);
                go.transform.localScale = scale;
            }

            Debug.Log($"{LogPrefix} Detached {list.Count} preserved object(s)");
            return list;
        }

        static GameObject SmashableRoot(Transform t)
        {
            // Walk up until parent is House Interior / room / scene root.
            while (t.parent != null)
            {
                var pn = t.parent.name;
                if (pn == "House Interior" || pn.StartsWith("House Interior", StringComparison.Ordinal)
                    || pn == RoomRootName)
                    break;
                t = t.parent;
            }
            return t.gameObject;
        }

        static void DeleteHouseInterior()
        {
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                if (root == null) continue;
                if (root.name == "House Interior" || root.name.StartsWith("House Interior", StringComparison.Ordinal))
                {
                    Debug.Log($"{LogPrefix} Destroying {root.name}");
                    UnityEngine.Object.DestroyImmediate(root);
                }
            }
        }

        static void DeleteOrphanHouseLights()
        {
            // Snapshot — DestroyImmediate mutates hierarchy.
            var lights = new List<GameObject>();
            foreach (var t in UnityEngine.Object.FindObjectsByType<Transform>(
                         FindObjectsInactive.Include, FindObjectsSortMode.None))
            {
                if (t == null) continue;
                if (t.name != "Light_1" && t.name != "Light_2" && t.name != "Light_3")
                    continue;
                if (t.root != null && t.root.name == RoomRootName)
                    continue;
                lights.Add(t.gameObject);
            }

            foreach (var go in lights)
            {
                if (go == null) continue;
                Debug.Log($"{LogPrefix} Destroying orphan light {go.name}");
                UnityEngine.Object.DestroyImmediate(go);
            }
        }

        static GameObject RebuildRoomRoot()
        {
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                if (root != null && root.name == RoomRootName)
                {
                    Debug.Log($"{LogPrefix} Rebuilding existing {RoomRootName}");
                    UnityEngine.Object.DestroyImmediate(root);
                }
            }

            var room = new GameObject(RoomRootName);
            room.transform.position = RoomOrigin;
            return room;
        }

        static void BuildFloor(GameObject room)
        {
            var prefab = LoadPrefab(FloorPrefabPath);
            for (int ix = 0; ix < 2; ix++)
            for (int iz = 0; iz < 2; iz++)
            {
                var min = RoomOrigin + new Vector3(ix * TileSize, 0f, iz * TileSize);
                PlaceFloorTile(prefab, room.transform, $"Floor_{ix}_{iz}", min, RoomOrigin.y);
            }
        }

        static void BuildRoof(GameObject room)
        {
            var prefab = LoadPrefab(FloorPrefabPath);
            float y = RoomOrigin.y + WallHeight;
            for (int ix = 0; ix < 2; ix++)
            for (int iz = 0; iz < 2; iz++)
            {
                var min = RoomOrigin + new Vector3(ix * TileSize, 0f, iz * TileSize);
                PlaceFloorTile(prefab, room.transform, $"Roof_{ix}_{iz}", min, y);
            }
        }

        static void PlaceFloorTile(GameObject prefab, Transform parent, string name, Vector3 xzMin, float yMin)
        {
            var go = PrefabUtility.InstantiatePrefab(prefab, parent) as GameObject;
            if (go == null) throw new Exception($"Instantiate failed: {name}");
            go.name = name;
            go.transform.rotation = Quaternion.identity;
            SnapAabbMin(go, new Vector3(xzMin.x, yMin, xzMin.z), snapX: true, snapY: true, snapZ: true);
            EnsureSolidCollider(go);
        }

        static void BuildWalls(GameObject room)
        {
            var prefab = LoadPrefab(WallPrefabPath);

            // Wall collider is thin on local Z. Rotate so local Z aligns with world outward.
            // West edge (outward -X): yaw 90 → local Z → world +X; we snap inner face to edge.
            PlaceWallRun(prefab, room.transform, "Wall_West",
                along: Vector3.forward,
                edgeStart: RoomOrigin,
                length: RoomSize,
                gapCenter: -1f,
                outward: Vector3.left,
                yaw: 90f);

            PlaceWallRun(prefab, room.transform, "Wall_East",
                along: Vector3.forward,
                edgeStart: RoomOrigin + new Vector3(RoomSize, 0f, 0f),
                length: RoomSize,
                gapCenter: -1f,
                outward: Vector3.right,
                yaw: -90f);

            PlaceWallRun(prefab, room.transform, "Wall_North",
                along: Vector3.right,
                edgeStart: RoomOrigin + new Vector3(0f, 0f, RoomSize),
                length: RoomSize,
                gapCenter: -1f,
                outward: Vector3.forward,
                yaw: 180f);

            // South = door wall: centered 1.2 m gap.
            PlaceWallRun(prefab, room.transform, "Wall_South",
                along: Vector3.right,
                edgeStart: RoomOrigin,
                length: RoomSize,
                gapCenter: RoomSize * 0.5f,
                outward: Vector3.back,
                yaw: 0f);
        }

        static void PlaceWallRun(
            GameObject prefab,
            Transform parent,
            string prefix,
            Vector3 along,
            Vector3 edgeStart,
            float length,
            float gapCenter,
            Vector3 outward,
            float yaw)
        {
            along = along.normalized;
            outward = outward.normalized;
            var intervals = new List<(float a, float b)>();
            if (gapCenter < 0f)
            {
                intervals.Add((0f, length));
            }
            else
            {
                float gap0 = Mathf.Clamp(gapCenter - DoorGap * 0.5f, 0f, length);
                float gap1 = Mathf.Clamp(gapCenter + DoorGap * 0.5f, 0f, length);
                if (gap0 > 0.01f) intervals.Add((0f, gap0));
                if (gap1 < length - 0.01f) intervals.Add((gap1, length));
            }

            int i = 0;
            foreach (var (a, b) in intervals)
            {
                float span = b - a;
                float cursor = a;
                while (cursor < b - 0.01f)
                {
                    float seg = Mathf.Min(TileSize, b - cursor);
                    // Full 3 m tile. Stubs (~2.4 m) overhang away from the door gap.
                    float placeAlongMin;
                    if (seg < TileSize - 0.01f)
                    {
                        bool beforeGap = gapCenter >= 0f && b <= gapCenter + 0.01f;
                        placeAlongMin = beforeGap ? (b - TileSize) : a;
                    }
                    else
                    {
                        placeAlongMin = cursor;
                    }

                    var go = PrefabUtility.InstantiatePrefab(prefab, parent) as GameObject;
                    if (go == null) throw new Exception($"Instantiate failed: {prefix}_{i}");
                    go.name = $"{prefix}_{i}";
                    go.transform.rotation = Quaternion.Euler(0f, yaw, 0f);

                    SnapWall(go, along, outward, edgeStart, placeAlongMin);
                    EnsureSolidCollider(go);
                    i++;
                    cursor += seg;
                }
            }
        }

        /// <summary>
        /// Snap wall so: along-min = edgeStart+along*alongMin, y-min = RoomOrigin.y,
        /// inner face (min along outward) sits on the room edge.
        /// </summary>
        static void SnapWall(GameObject go, Vector3 along, Vector3 outward, Vector3 edgeStart, float alongMin)
        {
            var col = go.GetComponentInChildren<Collider>();
            if (col == null) throw new Exception($"No collider on {go.name}");

            Physics.SyncTransforms();
            var b = col.bounds;

            float curAlongMin = ProjectMin(b, along);
            float tgtAlongMin = Vector3.Dot(edgeStart, along) + alongMin;

            float curInner = ProjectMin(b, outward); // inner face = smaller outward coord
            float tgtInner = Vector3.Dot(edgeStart, outward);

            float curYMin = b.min.y;
            float tgtYMin = RoomOrigin.y;

            go.transform.position +=
                along * (tgtAlongMin - curAlongMin)
                + outward * (tgtInner - curInner)
                + Vector3.up * (tgtYMin - curYMin);

            Physics.SyncTransforms();
            b = col.bounds;
            Debug.Log($"{LogPrefix} {go.name} AABB min={b.min} max={b.max}");
        }

        static float ProjectMin(Bounds b, Vector3 axis)
        {
            axis = axis.normalized;
            var c = b.center;
            var e = b.extents;
            float min = float.PositiveInfinity;
            for (int ix = -1; ix <= 1; ix += 2)
            for (int iy = -1; iy <= 1; iy += 2)
            for (int iz = -1; iz <= 1; iz += 2)
            {
                var p = c + new Vector3(e.x * ix, e.y * iy, e.z * iz);
                min = Mathf.Min(min, Vector3.Dot(p, axis));
            }
            return min;
        }

        static void SnapAabbMin(GameObject go, Vector3 targetMin, bool snapX, bool snapY, bool snapZ)
        {
            var col = go.GetComponentInChildren<Collider>();
            if (col == null) throw new Exception($"No collider on {go.name}");
            Physics.SyncTransforms();
            var b = col.bounds;
            var delta = Vector3.zero;
            if (snapX) delta.x = targetMin.x - b.min.x;
            if (snapY) delta.y = targetMin.y - b.min.y;
            if (snapZ) delta.z = targetMin.z - b.min.z;
            go.transform.position += delta;
            Physics.SyncTransforms();
            b = col.bounds;
            Debug.Log($"{LogPrefix} {go.name} AABB min={b.min} max={b.max}");
        }

        static void EnsureSolidCollider(GameObject go)
        {
            var cols = go.GetComponentsInChildren<Collider>(true);
            if (cols == null || cols.Length == 0)
                throw new Exception($"No collider on shell piece {go.name}");
            foreach (var c in cols)
            {
                c.enabled = true;
                c.isTrigger = false;
            }
        }

        static GameObject LoadPrefab(string path)
        {
            var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            if (prefab == null)
                throw new Exception($"Missing prefab: {path}");
            return prefab;
        }
    }
}
