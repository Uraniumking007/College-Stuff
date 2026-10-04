# Smash Room Redesign — Design (CIPAT / AVR)

**Date:** 2026-10-05  
**Course:** BE Sem 7 AVR / CIPAT demo  
**Scene:** `VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity`  
**Constraint:** Keep current bat grab + break loop; Editor + XR Device Simulator first

## Goal

Replace the full multi-room house with **one enclosed smash room**: spawn outside, grip a door open, enter, smash table props and a TV screen. Walls/floor/roof have collisions.

## Decisions (locked)

| Topic | Choice |
|-------|--------|
| Room shell | JC_LP `SM_Buildings_Floor_01` + `SM_Buildings_Wall_Interior_15_T1` (+ roof from scaled floor/wall) |
| Old house | **Delete** `House Interior` from smash scene |
| TV | `(Prb)MediaConsole` stand + **cube/quad screen** with `BreakableObject` |
| Screen smash | Disable mesh + break sound (+ optional debris); console stays |
| Door | `(Prb)Door`, **one-shot ~90° open on XR select**, stays open |
| Spawn | XR Origin **2–3 m outside door**, facing in |
| Keep | Bat (orange, seated), coffee table smashables, XR Origin / Device Simulator / Interaction Manager / EventSystem, grab-only break rules |

## Non-goals (YAGNI)

- Multi-room layout / keeping the nappin house shell
- Physics hinge drag-open door
- Real TV art / cracked-material swap
- Lighting bake polish / GI
- Android / Galaxy headset pass in this redesign
- New smashables beyond screen + existing table props

## Layout

```
  [XR Origin spawn / outdoor pad]
           |
        [Door]   ← grip/select → swing open once
           |
   +-------|--------+
   | sofa           |  MediaConsole + breakable screen (wall)
   |                |
   |   coffee table |  vases / plant / containers + orange bat
   |                |
   +----------------+
        roof above; JC_LP walls/floor with BoxColliders
```

Approx room: **~6×6 m** (two 3 m JC floor tiles per side, or scaled equivalent). Door on south wall. Table center. Sofa along one side. Console opposite sofa or on back wall.

## Architecture

### Stack (unchanged)

Unity 6000.6.4f1 · URP · XRIT 3.6.1 · OpenXR · XR Device Simulator · Active Input Handling = Both

### Scene graph (target)

- `CIPAT_SmashRoom` (empty parent)
  - `Floor`, `Wall_*`, `Roof` (JC_LP prefab instances, static colliders)
  - `(Prb)Door` + `DoorSwingOnSelect`
  - `(Prb)Sofa` (or CornerSofa)
  - `(Prb)MediaConsole`
  - `TvScreen` (primitive) + `BreakableObject`
  - Existing: `(Prb)CoffeTable`, smashables, `Bat`
- `XR Origin (XR Rig)` — outside, facing door
- `XR Device Simulator`, `XR Interaction Manager`, `EventSystem`

### Smash loop (unchanged rules)

1. Grip bat (`XRGrabInteractable` + `GrabPhysicsToggle`)
2. Bat tagged `Weapon` hits breakable while selected, speed ≥ threshold
3. Audio + haptic path + disable + debris

### Door loop (new)

1. Hand selects door body (`XRGrabInteractable` or select listener)
2. `DoorSwingOnSelect` rotates door ~90° around hinge once
3. Further selects ignored (already open)

## Components

| Asset / script | Role |
|----------------|------|
| `SM_Buildings_Floor_01` | Floor tiles (BoxCollider ~3×3) |
| `SM_Buildings_Wall_Interior_15_T1` | Walls (BoxCollider ~3×3×0.24) |
| Roof | Scaled floor or wall pieces |
| `(Prb)Door` | Visual + colliders; add select → swing |
| `DoorSwingOnSelect.cs` | One-shot open on select entered |
| `(Prb)MediaConsole` | Stand (`mediaConsole_TV` child may exist — prefer dedicated smash cube if mesh not isolatable) |
| `TvScreen` | Cube/quad + `BreakableObject` |
| `CipatSmashRoomBootstrap.cs` | Editor batch: delete house, assemble room, place props, wire door/TV, move spawn |

## Acceptance checklist

1. Play Mode: spawn outside; door visible; no full house
2. Cannot walk through walls / floor / roof
3. Grip door → opens once and stays open
4. Enter room → table, bat, smashables, sofa, console+screen present
5. Grab bat → smash vase (sound + disable + debris)
6. Grab bat → smash TV screen (sound + disable); console remains
7. Soft tap / ungrabbed bat → no break
8. XR Interaction Manager + EventSystem still present

## Risks / notes

- JC_LP wall collider center is offset (`center.x = -1.5`); bootstrap must place by **bounds**, not raw transform origin
- HDRP leftover packages under JC_LP must **not** be imported into this URP project
- Deleting house may leave stray lights — bootstrap should remove or disable house-only lights
- Door hinge axis: use door_body local Y; tune angle in inspector

## Implementation follow-up

Write bite-sized plan: `docs/plans/2026-10-05-smash-room-redesign.md`  
Execute via subagent-driven or inline tasks after plan approval.
