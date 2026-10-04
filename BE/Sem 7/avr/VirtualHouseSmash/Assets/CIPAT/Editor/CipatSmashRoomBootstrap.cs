using System;
using System.Collections.Generic;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.XR.Interaction.Toolkit.Interactables;

namespace Cipat.Editor
{
    /// <summary>
    /// Delete House Interior, scaffold a ~6x6 JC_LP smash-room shell,
    /// place door / sofa / MediaConsole + TV, reseat table/smashables/bat,
    /// and spawn XR Origin outside the south door facing into the room.
    /// </summary>
    public static class CipatSmashRoomBootstrap
    {
        const string LogPrefix = "[CIPAT Room]";
        const string ScenePath = "Assets/Scenes/CIPAT_SmashHouse.unity";
        const string FloorPrefabPath = "Assets/JC_LP_House_Lite/Prefabs/SM_Buildings_Floor_01.prefab";
        const string WallPrefabPath = "Assets/JC_LP_House_Lite/Prefabs/SM_Buildings_Wall_Interior_15_T1.prefab";
        const string DoorPrefabPath = "Assets/nappin/HouseInteriorPack/Prefabs/(Prb)Door.prefab";
        const string SofaPrefabPath = "Assets/nappin/HouseInteriorPack/Prefabs/(Prb)Sofa.prefab";
        const string ConsolePrefabPath = "Assets/nappin/HouseInteriorPack/Prefabs/(Prb)MediaConsole.prefab";
        const string GlassBreakPath = "Assets/CIPAT/Audio/glass_break.wav";

        const string RoomRootName = "CIPAT_SmashRoom";

        // RoomOrigin = southwest corner of the 6x6 floor AABB (world).
        // Near the existing coffee-table cluster (~-13, y, ~-7) so smashables stay reachable.
        static readonly Vector3 RoomOrigin = new Vector3(-13f, 0f, -8f);
        const float TileSize = 3f;
        const float RoomSize = 6f;
        const float WallHeight = 3f;
        const float DoorGap = 1.2f;

        // Interior layout targets (world).
        static readonly Vector3 RoomCenter = new Vector3(-10f, 0f, -5f);
        static readonly Vector3 TableXz = new Vector3(-10f, 0f, -5f);
        static readonly Vector3 XrSpawnPos = new Vector3(-10f, 0.02f, -10.5f);
        static readonly Quaternion BatRotation = Quaternion.Euler(0f, 25f, 90f);
        const float BatClearance = 0.04f;

        // Scatter offsets around table center (same pattern as CipatMoveBreakablesBootstrap).
        static readonly Vector3[] SmashOffsets =
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
                Debug.Log($"{LogPrefix} Starting");

                var scene = EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single);

                var preserved = CollectAndDetachPreserved();
                DeleteHouseInterior();
                DeleteOrphanHouseLights();
                DeleteOrphanTask3Props();

                var room = RebuildRoomRoot();
                BuildFloor(room);
                BuildWalls(room);
                BuildRoof(room);

                PlaceDoor(room);
                PlaceSofa(room);
                PlaceMediaConsoleAndTv(room);

                PlaceTableCluster(room, preserved);
                PlaceXrOriginSpawn();

                foreach (var go in preserved)
                {
                    if (go != null)
                        Debug.Log($"{LogPrefix} Preserved: {go.name} @ {go.transform.position}");
                }

                DisableConflictingCameras();

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
                // TvScreen is recreated each bootstrap — do not preserve orphans.
                if (b.gameObject.name == "TvScreen" || b.transform.root.name == "TvScreen")
                    continue;
                var go = SmashableRoot(b.transform);
                if (go.name == "TvScreen") continue;
                if (!list.Contains(go))
                    list.Add(go);
            }

            foreach (var t in UnityEngine.Object.FindObjectsByType<Transform>(
                         FindObjectsInactive.Include, FindObjectsSortMode.None))
            {
                if (t == null) continue;
                if (t.name != "(Prb)CoffeTable" && t.name != "Bat") continue;
                // Bat: only the hierarchy root named Bat (skip nested meshes if any).
                if (t.name == "Bat")
                {
                    var root = SmashableRoot(t);
                    if (root.name != "Bat") continue;
                    if (!list.Contains(root))
                        list.Add(root);
                    continue;
                }
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

        static void DeleteOrphanTask3Props()
        {
            var names = new HashSet<string> { "(Prb)Door", "(Prb)Sofa", "(Prb)MediaConsole", "TvScreen" };
            var doomed = new List<GameObject>();
            foreach (var t in UnityEngine.Object.FindObjectsByType<Transform>(
                         FindObjectsInactive.Include, FindObjectsSortMode.None))
            {
                if (t == null) continue;
                if (!names.Contains(t.name)) continue;
                if (t.parent != null && t.parent.name == RoomRootName) continue;
                if (t.root != null && t.root.name == RoomRootName) continue;
                doomed.Add(t.gameObject);
            }

            foreach (var go in doomed)
            {
                if (go == null) continue;
                Debug.Log($"{LogPrefix} Destroying orphan Task3 prop {go.name}");
                UnityEngine.Object.DestroyImmediate(go);
            }
        }

        static void DisableConflictingCameras()
        {
            GameObject xrOrigin = null;
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                if (root != null && root.name.StartsWith("XR Origin", StringComparison.Ordinal))
                {
                    xrOrigin = root;
                    break;
                }
            }

            var cameras = UnityEngine.Object.FindObjectsByType<Camera>(
                FindObjectsInactive.Include, FindObjectsSortMode.None);
            int disabled = 0;
            foreach (var cam in cameras)
            {
                if (cam == null) continue;
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

        static void PlaceTableCluster(GameObject room, List<GameObject> preserved)
        {
            GameObject table = null;
            GameObject bat = null;
            var smashables = new List<GameObject>();

            foreach (var go in preserved)
            {
                if (go == null) continue;
                if (go.name == "(Prb)CoffeTable")
                {
                    table = go;
                    continue;
                }
                if (go.name == "Bat")
                {
                    bat = go;
                    continue;
                }
                if (go.GetComponentInChildren<Cipat.BreakableObject>(true) != null
                    && go.name != "TvScreen")
                    smashables.Add(go);
            }

            // Also hunt loose Bat if not preserved (fresh scene / renamed parent).
            if (bat == null)
            {
                foreach (var t in UnityEngine.Object.FindObjectsByType<Transform>(
                             FindObjectsInactive.Include, FindObjectsSortMode.None))
                {
                    if (t != null && t.name == "Bat" && (t.parent == null || t.parent.name == RoomRootName))
                    {
                        bat = t.gameObject;
                        break;
                    }
                }
            }

            if (table == null)
                throw new Exception("(Prb)CoffeTable not found — cannot reseat smashables");

            // 1) Table to room center, upright, seated on floor.
            table.transform.SetParent(null, true);
            table.transform.rotation = Quaternion.identity;
            table.transform.position = new Vector3(TableXz.x, table.transform.position.y, TableXz.z);
            Physics.SyncTransforms();
            var tableCol = table.GetComponentInChildren<Collider>();
            if (tableCol == null) throw new Exception("No collider on (Prb)CoffeTable");
            float floorY = RoomOrigin.y;
            float deltaY = floorY - tableCol.bounds.min.y;
            table.transform.position += new Vector3(0f, deltaY, 0f);
            Physics.SyncTransforms();
            float tableTopY = tableCol.bounds.max.y;
            Debug.Log($"{LogPrefix} Table @ {table.transform.position} topY={tableTopY:F3}");

            // 2) Smashables on tabletop.
            smashables.Sort((a, b) => string.CompareOrdinal(a.name, b.name));
            for (int i = 0; i < smashables.Count; i++)
            {
                var go = smashables[i];
                go.transform.SetParent(null, true);
                var offset = SmashOffsets[i % SmashOffsets.Length];
                go.transform.position = new Vector3(
                    TableXz.x + offset.x,
                    go.transform.position.y,
                    TableXz.z + offset.z);

                foreach (var c in go.GetComponentsInChildren<Collider>(true))
                {
                    if (c.gameObject == go) continue;
                    if (c is BoxCollider)
                        UnityEngine.Object.DestroyImmediate(c);
                }

                Physics.SyncTransforms();
                var col = go.GetComponent<Collider>() ?? go.GetComponentInChildren<Collider>();
                float bottom = col != null ? col.bounds.min.y : go.transform.position.y;
                go.transform.position += new Vector3(0f, tableTopY - bottom, 0f);
                Physics.SyncTransforms();
                float seated = col != null ? col.bounds.min.y : go.transform.position.y;
                Debug.Log($"{LogPrefix} Smashable {go.name} @ {go.transform.position} bottom={seated:F3} topY={tableTopY:F3}");
            }

            // 3) Bat on table with clearance.
            if (bat != null)
            {
                bat.transform.SetParent(null, true);
                bat.transform.SetPositionAndRotation(
                    new Vector3(TableXz.x + 0.05f, bat.transform.position.y, TableXz.z - 0.05f),
                    BatRotation);
                Physics.SyncTransforms();
                var batCol = bat.GetComponent<Collider>() ?? bat.GetComponentInChildren<Collider>();
                if (batCol != null)
                {
                    float bottom = batCol.bounds.min.y;
                    bat.transform.position += new Vector3(0f, (tableTopY + BatClearance) - bottom, 0f);
                    Physics.SyncTransforms();
                    Debug.Log($"{LogPrefix} Bat @ {bat.transform.position} bottom={batCol.bounds.min.y:F3} target={tableTopY + BatClearance:F3}");
                }
                else
                {
                    Debug.LogWarning($"{LogPrefix} Bat has no collider — left at {bat.transform.position}");
                }
            }
            else
            {
                Debug.LogWarning($"{LogPrefix} Bat not found — skip bat reseat");
            }

            // 4) Reparent under room (world-position preserve).
            table.transform.SetParent(room.transform, true);
            foreach (var go in smashables)
            {
                if (go != null) go.transform.SetParent(room.transform, true);
            }
            if (bat != null) bat.transform.SetParent(room.transform, true);

            Debug.Log($"{LogPrefix} Table cluster reparented under {RoomRootName} (smashables={smashables.Count})");
        }

        static void PlaceXrOriginSpawn()
        {
            GameObject xr = null;
            foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
            {
                if (root != null && root.name.StartsWith("XR Origin", StringComparison.Ordinal))
                {
                    xr = root;
                    break;
                }
            }

            if (xr == null)
            {
                Debug.LogWarning($"{LogPrefix} XR Origin not found — skip spawn placement");
                return;
            }

            // Face into the room (+Z toward RoomCenter from south of the door).
            var look = RoomCenter - new Vector3(XrSpawnPos.x, RoomCenter.y, XrSpawnPos.z);
            if (look.sqrMagnitude < 1e-6f) look = Vector3.forward;
            var rot = Quaternion.LookRotation(look.normalized, Vector3.up);

            xr.transform.SetPositionAndRotation(XrSpawnPos, rot);
            Debug.Log($"{LogPrefix} XR Origin @ {xr.transform.position} yaw={xr.transform.eulerAngles.y:F1}");
        }

        static void PlaceDoor(GameObject room)
        {
            var prefab = LoadPrefab(DoorPrefabPath);
            var door = PrefabUtility.InstantiatePrefab(prefab, room.transform) as GameObject;
            if (door == null) throw new Exception("Instantiate door failed");
            door.name = "(Prb)Door";

            // South-wall gap center; face into room (+Z). Prefab width is local Z → yaw 90 so it spans X.
            door.transform.SetPositionAndRotation(
                new Vector3(-10f, RoomOrigin.y, RoomOrigin.z),
                Quaternion.Euler(0f, 90f, 0f));
            Physics.SyncTransforms();
            var b = EncapsulateColliders(door);
            door.transform.position += new Vector3(
                -10f - b.center.x,
                RoomOrigin.y - b.min.y,
                RoomOrigin.z - b.center.z);
            Physics.SyncTransforms();
            b = EncapsulateColliders(door);
            Debug.Log($"{LogPrefix} Door AABB min={b.min} max={b.max}");

            var body = FindDeep(door.transform, "door_body");
            if (body == null) throw new Exception("door_body missing on (Prb)Door");

            var rb = body.GetComponent<Rigidbody>();
            if (rb == null) rb = body.gameObject.AddComponent<Rigidbody>();
            rb.isKinematic = true;
            rb.useGravity = false;

            var grab = body.GetComponent<XRGrabInteractable>();
            if (grab == null) grab = body.gameObject.AddComponent<XRGrabInteractable>();
            grab.movementType = XRBaseInteractable.MovementType.Instantaneous;
            grab.throwOnDetach = false;
            var grabSo = new SerializedObject(grab);
            var trackPos = grabSo.FindProperty("m_TrackPosition");
            if (trackPos != null) trackPos.boolValue = false;
            var trackRot = grabSo.FindProperty("m_TrackRotation");
            if (trackRot != null) trackRot.boolValue = false;
            grabSo.ApplyModifiedPropertiesWithoutUndo();

            var swing = body.GetComponent<Cipat.DoorSwingOnSelect>();
            if (swing == null) swing = body.gameObject.AddComponent<Cipat.DoorSwingOnSelect>();
            var so = new SerializedObject(swing);
            so.FindProperty("hinge").objectReferenceValue = body;
            so.ApplyModifiedPropertiesWithoutUndo();

            EditorUtility.SetDirty(door);
            Debug.Log($"{LogPrefix} Placed door @ {door.transform.position} rotY={door.transform.eulerAngles.y}");
        }

        static void PlaceSofa(GameObject room)
        {
            var prefab = LoadPrefab(SofaPrefabPath);
            var sofa = PrefabUtility.InstantiatePrefab(prefab, room.transform) as GameObject;
            if (sofa == null) throw new Exception("Instantiate sofa failed");
            sofa.name = "(Prb)Sofa";

            // West wall, near table cluster, leave walk path from south door.
            // Long axis local Z (~3 m) along room depth; identity yaw faces +X into room.
            sofa.transform.SetPositionAndRotation(
                new Vector3(-12.2f, RoomOrigin.y, -5.2f),
                Quaternion.identity);
            SnapAabbMin(sofa, new Vector3(-12.2f, RoomOrigin.y, -5.2f), snapX: false, snapY: true, snapZ: false);

            EditorUtility.SetDirty(sofa);
            Debug.Log($"{LogPrefix} Placed sofa @ {sofa.transform.position}");
        }

        static void PlaceMediaConsoleAndTv(GameObject room)
        {
            var prefab = LoadPrefab(ConsolePrefabPath);
            var console = PrefabUtility.InstantiatePrefab(prefab, room.transform) as GameObject;
            if (console == null) throw new Exception("Instantiate MediaConsole failed");
            console.name = "(Prb)MediaConsole";

            // North wall (z≈-2). Long axis local Z → yaw -90 spans X; -localX (TV side) faces into room (-Z).
            console.transform.SetPositionAndRotation(
                new Vector3(-10f, RoomOrigin.y, -2.35f),
                Quaternion.Euler(0f, -90f, 0f));
            SnapAabbMin(console, new Vector3(-10f, RoomOrigin.y, -2.35f), snapX: false, snapY: true, snapZ: false);

            var bakedTv = FindDeep(console.transform, "mediaConsole_TV");
            if (bakedTv != null)
                bakedTv.gameObject.SetActive(false);

            var screen = GameObject.CreatePrimitive(PrimitiveType.Cube);
            screen.name = "TvScreen";
            screen.transform.SetParent(console.transform, false);
            screen.transform.localPosition = new Vector3(0f, 1.1f, -0.05f);
            screen.transform.localScale = new Vector3(1.2f, 0.7f, 0.05f);

            var br = screen.AddComponent<Cipat.BreakableObject>();
            var clip = AssetDatabase.LoadAssetAtPath<AudioClip>(GlassBreakPath);
            if (clip == null) throw new Exception($"Missing audio: {GlassBreakPath}");
            var so = new SerializedObject(br);
            so.FindProperty("breakSound").objectReferenceValue = clip;
            so.ApplyModifiedPropertiesWithoutUndo();

            EditorUtility.SetDirty(console);
            Debug.Log($"{LogPrefix} Placed MediaConsole @ {console.transform.position} + TvScreen");
        }

        static Bounds EncapsulateColliders(GameObject go)
        {
            var cols = go.GetComponentsInChildren<Collider>(true);
            if (cols == null || cols.Length == 0)
                throw new Exception($"No collider on {go.name}");
            var b = cols[0].bounds;
            for (int i = 1; i < cols.Length; i++)
                b.Encapsulate(cols[i].bounds);
            return b;
        }

        static Transform FindDeep(Transform root, string name)
        {
            if (root.name == name) return root;
            for (int i = 0; i < root.childCount; i++)
            {
                var found = FindDeep(root.GetChild(i), name);
                if (found != null) return found;
            }
            return null;
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
