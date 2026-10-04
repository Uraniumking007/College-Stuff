# Virtual House Smash — Friend Test Instructions

CIPAT / AVR demo: spawn outside one smash room, grip the door open, grab the bat, smash props + TV (sound + haptic code path).

**Repo:** https://github.com/Uraniumking007/College-Stuff  
**Project folder:** `BE/Sem 7/avr/VirtualHouseSmash`  
**Play scene:** `Assets/Scenes/CIPAT_SmashHouse.unity`

---

## 1. Prerequisites

1. Install [Unity Hub](https://unity.com/download)
2. Install editor **Unity 6000.6.4f1** (or closest **Unity 6** LTS)  
   - Hub → Installs → Install Editor → Unity 6  
   - If Unity asks to upgrade the project, accept only if you must; prefer matching `6000.6.x`
3. Optional modules: Android Build Support (only needed for Galaxy headset later — skip for Editor test)

---

## 2. Get the project

```bash
git clone https://github.com/Uraniumking007/College-Stuff.git
```

Or pull if you already have it:

```bash
cd College-Stuff
git pull origin main
```

Open in Hub:

**Add** → select  
`College-Stuff/BE/Sem 7/avr/VirtualHouseSmash`  
→ Open

First open can take several minutes (package resolve / import).

---

## 3. Open the demo scene

1. Project window → `Assets/Scenes/CIPAT_SmashHouse`
2. Double-click to open
3. Hierarchy should show roughly:
   - **CIPAT_SmashRoom** (single room — not a multi-room House Interior)
     - walls / floor / roof (colliding)
     - **Door** (grip to open once)
     - coffee table + orange **Bat** + smashable vases/plant/containers
     - sofa, **MediaConsole**, smashable **TvScreen**
   - **XR Origin (XR Rig)** — spawn **outside** the room, facing the door
   - **XR Device Simulator**
   - **XR Interaction Manager**
   - **EventSystem**

---

## 4. Play Mode test

1. Press **Play** (▶)
2. Click the **Game** view so Device Simulator keys/mouse go there (required)
3. You spawn **outside** the room with the door in front
4. Open the door (Device Simulator):
   - move a hand onto the door (**Space** = right hand)
   - **G** = grip while the hand is on the door → door swings open **once** and stays open
5. Walk in. Room center: coffee table with orange bat + vases; also sofa + MediaConsole + smashable **TvScreen**
6. **Grip** the **Bat** from the table, swing into a **vase** or the **TvScreen**
7. Expected:
   - props / screen stay intact until you swing the **grabbed** bat
   - smashable disappears / disables (console stand stays)
   - break **sound** plays
   - small **debris** cubes spawn briefly
8. Soft taps may **not** break (speed threshold) — swing harder
9. Press **Play** again to stop; press Play once more to reset the scene

### Haptics note

Controller vibration often **does not** fire in Editor Device Simulator.  
Code path exists (`HapticUtil` → `SendHapticImpulse`) for real headset builds. Audio + break is the Editor proof.

---

## 5. If something’s wrong

| Problem | Fix |
|--------|-----|
| Stuck outside / door won’t open | Put hand on door (**Space**), hold **G** (grip). Door opens once only |
| Walk through walls | Re-run room bootstrap (`CipatSmashRoomBootstrap`) so colliders are present |
| Can’t find bat | Orange bat sits on the **coffee table center** inside the room |
| Pink materials | Stay on URP; let Unity finish importing; don’t open HDRP nested packages |
| Can’t grab bat | Click **Game** view; confirm Device Simulator + XR Interaction Manager + EventSystem are in the scene |
| Items break on Play / freefall smash | Grab bat first, then hit. Soft tap / ungrabbed bat should not break |
| No break | Grab the bat, then hit a nearby smashable (vase on table or **TvScreen**), not the sofa/console stand |
| Scripts missing / compile errors | Wait for import; Console → clear; reopen project with Unity 6 |
| Scene empty / wrong scene | Open `CIPAT_SmashHouse`, not `SampleScene` |

---

## 6. What to record for CIPAT (optional)

- 20–40s screen recording: outside → grip door → grab bat → smash vase/TV → sound
- Hierarchy screenshot (`CIPAT_SmashRoom`)
- `BreakableObject` inspector screenshot (audio + haptic fields)

More notes: `docs/cipat-demo-notes.md`

---

## Quick path (TL;DR)

1. Clone repo  
2. Hub → open `BE/Sem 7/avr/VirtualHouseSmash`  
3. Open `Assets/Scenes/CIPAT_SmashHouse`  
4. Play → outside → grip door (**Space** + **G**) → grab bat → smash vase/TV  
