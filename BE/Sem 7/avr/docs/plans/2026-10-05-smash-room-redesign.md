# Smash Room Redesign Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Replace the multi-room house in `CIPAT_SmashHouse` with one JC_LP smash room: spawn outside, grip door open, enter, smash table props + TV screen; walls/floor/roof collide.

**Architecture:** Editor bootstrap deletes `House Interior`, assembles a ~6×6 m room from JC_LP floor/wall prefabs (existing BoxColliders), places door/sofa/MediaConsole/TV screen/table cluster, and moves XR Origin outside facing the door. New `DoorSwingOnSelect` one-shots a 90° open on XR select. TV screen is a primitive with existing `BreakableObject`. Keep bat grab-only smash rules and XR Manager/EventSystem.

**Tech Stack:** Unity 6000.6.4f1 URP, XRIT 3.6.1, OpenXR, XR Device Simulator, existing Cipat scripts/bootstraps.

**Design doc:** `docs/plans/2026-10-05-smash-room-redesign-design.md`

**Unity batch binary:** `/Applications/Unity/Hub/Editor/6000.6.4f1/Unity.app/Contents/MacOS/Unity`  
**Project:** `BE/Sem 7/avr/VirtualHouseSmash`

---

### Task 1: Add `DoorSwingOnSelect`

**Files:**
- Create: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/DoorSwingOnSelect.cs`
- Create: matching `.meta` via Unity import (do not hand-author guid)

**Step 1: Implement one-shot swing on select**

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.XR.Interaction.Toolkit.Interactables;

namespace Cipat
{
    [RequireComponent(typeof(XRGrabInteractable))]
    public class DoorSwingOnSelect : MonoBehaviour
    {
        [SerializeField] Transform hinge;
        [SerializeField] Vector3 localAxis = Vector3.up;
        [SerializeField] float openAngle = 90f;
        [SerializeField] float duration = 0.35f;

        XRGrabInteractable grab;
        bool opened;
        bool animating;
        Quaternion startRot;
        Quaternion endRot;
        float t;

        void Awake()
        {
            grab = GetComponent<XRGrabInteractable>();
            if (hinge == null) hinge = transform;
            // Door should not fly into hand — kinematic + no movement tracking.
            grab.movementType = XRBaseInteractable.MovementType.Instantaneous;
            grab.throwOnDetach = false;
            var rb = GetComponent<Rigidbody>();
            if (rb != null)
            {
                rb.isKinematic = true;
                rb.useGravity = false;
            }
        }

        void OnEnable() => grab.selectEntered.AddListener(OnSelectEntered);
        void OnDisable() => grab.selectEntered.RemoveListener(OnSelectEntered);

        void OnSelectEntered(SelectEnterEventArgs _)
        {
            if (opened || animating) return;
            startRot = hinge.localRotation;
            endRot = startRot * Quaternion.AngleAxis(openAngle, localAxis.normalized);
            t = 0f;
            animating = true;
            // Drop select so the hand doesn't keep owning the door.
            for (int i = grab.interactorsSelecting.Count - 1; i >= 0; i--)
                grab.interactionManager.SelectExit(grab.interactorsSelecting[i], grab);
        }

        void Update()
        {
            if (!animating) return;
            t += Time.deltaTime / Mathf.Max(0.01f, duration);
            hinge.localRotation = Quaternion.Slerp(startRot, endRot, Mathf.Clamp01(t));
            if (t >= 1f)
            {
                hinge.localRotation = endRot;
                animating = false;
                opened = true;
            }
        }
    }
}
```

Tune later if hinge child should be `door_body` while grab sits on the same GO.

**Step 2: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/DoorSwingOnSelect.cs" \
        "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/DoorSwingOnSelect.cs.meta"
git commit -m "$(cat <<'MSG'
feat(avr): add one-shot XR door swing on select
MSG
)"
```

---

### Task 2: Scaffold `CipatSmashRoomBootstrap` (delete house + room shell)

**Files:**
- Create: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatSmashRoomBootstrap.cs`

**Step 1: Constants + Run entry**

Match other bootstraps: `public static void Run()`, `EditorApplication.Exit(0/1)`, `LogPrefix = "[CIPAT Room]"`.

Paths:
- Scene: `Assets/Scenes/CIPAT_SmashHouse.unity`
- Floor: `Assets/JC_LP_House_Lite/Prefabs/SM_Buildings_Floor_01.prefab`
- Wall: `Assets/JC_LP_House_Lite/Prefabs/SM_Buildings_Wall_Interior_15_T1.prefab`
- Door: `Assets/nappin/HouseInteriorPack/Prefabs/(Prb)Door.prefab`
- Sofa: `Assets/nappin/HouseInteriorPack/Prefabs/(Prb)Sofa.prefab`
- Console: `Assets/nappin/HouseInteriorPack/Prefabs/(Prb)MediaConsole.prefab`

Room origin (world): e.g. `(-13, 0, -8)` so coffee-table cluster can stay near current coords after reposition — pick one parent origin and place everything relative to it. Document chosen origin in a comment.

**Step 2: Delete house content**

```csharp
static void DeleteHouseInterior()
{
    foreach (var root in SceneManager.GetActiveScene().GetRootGameObjects())
    {
        if (root.name == "House Interior" || root.name.StartsWith("House Interior"))
            Object.DestroyImmediate(root);
    }
    // Also destroy leftover house lights if named Light_1/2/3 and not under CIPAT_SmashRoom
}
```

Do **not** delete: `XR Origin (XR Rig)`, `XR Device Simulator`, `XR Interaction Manager`, `EventSystem`, `Bat`, smashables you will reparent/move, `StaticLightingSky` (optional keep).

If smashables are children of the house hierarchy, **collect references first** (by `BreakableObject` / names) before deleting, then reparent under `CIPAT_SmashRoom` or leave as roots after move.

**Step 3: Build shell**

Parent `CIPAT_SmashRoom`:
- Floor: 2×2 grid of floor prefabs (each tile collider size ~3×3; place using **collider bounds**, not raw pivot — JC_LP pivots are offset)
- Walls: four sides; south wall leave a ~1.2 m door gap (two wall segments with a hole, or three pieces)
- Roof: floor tiles at y ≈ 3 m, or scaled wall pieces

Ensure every shell piece has an enabled non-trigger collider (prefabs already do).

**Step 4: Batch compile check**

```bash
UNITY=.../Unity
"$UNITY" -batchmode -nographics -quit \
  -projectPath ".../VirtualHouseSmash" \
  -executeMethod Cipat.Editor.CipatSmashRoomBootstrap.Run \
  -logFile /tmp/cipat-smash-room.log
```

First Run may only delete+shell if later placement not ready — prefer finishing Tasks 3–4 in same bootstrap before relying on Play.

**Step 5: Commit scaffold when shell builds without compile errors** (placement can be same commit if small).

```bash
git commit -m "$(cat <<'MSG'
feat(avr): bootstrap smash room shell from JC_LP tiles
MSG
)"
```

---

### Task 3: Place door, sofa, MediaConsole, TV screen

**Files:**
- Modify: `CipatSmashRoomBootstrap.cs`
- Prefabs as above
- TV screen created at runtime in bootstrap (primitive cube), not a checked-in mesh

**Step 1: Door**

Instantiate `(Prb)Door` in south wall opening. On `door_body` (or root if simpler):
- Add `Rigidbody` kinematic if missing
- Add `XRGrabInteractable` if missing
- Add `DoorSwingOnSelect`; set `hinge` to the rotating transform (`door_body`)

**Step 2: Sofa + MediaConsole**

Place sofa near table (side wall). Place MediaConsole against opposite/back wall.

**Step 3: TV screen**

```csharp
var screen = GameObject.CreatePrimitive(PrimitiveType.Cube);
screen.name = "TvScreen";
screen.transform.SetParent(console.transform, false);
screen.transform.localPosition = new Vector3(0f, 1.1f, -0.05f); // tune
screen.transform.localScale = new Vector3(1.2f, 0.7f, 0.05f);
var br = screen.AddComponent<Cipat.BreakableObject>();
// Assign breakSound via AssetDatabase if an existing CIPAT audio clip path is known
```

Bright unlit/URP material optional (reuse bat highlight pattern or default).

**Step 4: Commit**

```bash
git commit -m "$(cat <<'MSG'
feat(avr): place door, sofa, console, and breakable TV screen
MSG
)"
```

---

### Task 4: Reposition table cluster, bat, XR Origin; wire spawn facing door

**Files:**
- Modify: `CipatSmashRoomBootstrap.cs`
- Modify: scene `CIPAT_SmashHouse.unity` (via batch)
- Possibly call existing seating helpers or duplicate SyncTransforms seating for smashables + bat

**Step 1: Table + smashables + bat**

Move coffee table to room center. Re-seat smashables on tabletop (`TableTopY` from collider bottom + `Physics.SyncTransforms`). Re-run bat seat logic (or invoke shared numbers: bottom on tabletop + clearance).

**Step 2: XR Origin**

Place origin **2–3 m outside** south door, Y on floor, rotation facing door (+Z or yaw toward room center). Keep Device Simulator at identity root (as now).

**Step 3: Idempotency**

If `CIPAT_SmashRoom` already exists, destroy/rebuild OR early-out with log — prefer destroy child rebuild for repeatable batch.

**Step 4: Run Unity batch end-to-end; verify scene YAML**

Confirm present:
- `CIPAT_SmashRoom`
- `TvScreen`
- `(Prb)Door` / DoorSwing
- No `House Interior`
- XR Origin position outside

**Step 5: Commit**

```bash
git add \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatSmashRoomBootstrap.cs" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity" \
  # + any new mats/scripts metas
git commit -m "$(cat <<'MSG'
feat(avr): assemble single smash room and outside spawn
MSG
)"
```

---

### Task 5: Update friend instructions + demo notes

**Files:**
- Modify: `BE/Sem 7/avr/instructions.md`
- Modify: `BE/Sem 7/avr/docs/cipat-demo-notes.md`

**Step 1: Document new flow**

- Spawn outside room → grip door (G while hand on door) → enters
- Room contents: table/bat/vases, sofa, MediaConsole + smashable screen
- Walls collide
- Troubleshooting: “stuck outside” → grip door; “walk through walls” → re-run room bootstrap

**Step 2: Commit**

```bash
git commit -m "$(cat <<'MSG'
docs(avr): document smash room entry and TV screen
MSG
)"
```

---

### Task 6: End-to-end Play Mode verification + push

**Checklist**

1. Play → outside, door visible, no multi-room house
2. Walk into wall → blocked
3. Space+mouse to door, hold G → door swings open once
4. Enter → table/bat/sofa/console/screen
5. Grab bat → smash vase + smash screen
6. Soft tap / no grab → no break

**Push when green**

```bash
git push origin main
```

---

## Out of scope

- Physics hinge drag door
- Cracked TV material art
- Keeping nappin house shell
- Lighting bake
- Galaxy/Android build

## Execution note

Prefer subagent-driven (implementer → spec review → quality review per task) same as Play Mode fix plan. Unity batch must use Hub editor binary; check `Temp/UnityLockfile` before batch.
