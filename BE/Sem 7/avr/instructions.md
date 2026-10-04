# Virtual House Smash — Friend Test Instructions

CIPAT / AVR demo: smash props in a VR house with sound + haptic code path.

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
   - house / furniture
   - **XR Origin (XR Rig)**
   - **XR Device Simulator**
   - **XR Interaction Manager**
   - **EventSystem**
   - **Bat** on the coffee table (not already in hand — grab it)
   - smashables seated on the coffee table (vases, plant, containers)

---

## 4. Play Mode test

1. Press **Play** (▶)
2. Click the **Game** view so Device Simulator keys/mouse go there (required)
3. Use **XR Device Simulator** (keyboard/mouse — see Game view overlay / docs):
   - move headset / hands to the coffee table
   - **grip** to grab the **Bat** (starts on the table, not in-hand)
   - swing into a **vase / plant / container**
4. Expected:
   - props stay intact until you swing the **grabbed** bat
   - prop disappears / disables
   - break **sound** plays
   - small **debris** cubes spawn briefly
5. Soft taps may **not** break (speed threshold) — swing harder
6. Press **Play** again to stop; press Play once more to reset the scene

### Haptics note

Controller vibration often **does not** fire in Editor Device Simulator.  
Code path exists (`HapticUtil` → `SendHapticImpulse`) for real headset builds. Audio + break is the Editor proof.

---

## 5. If something’s wrong

| Problem | Fix |
|--------|-----|
| Pink materials | Stay on URP; let Unity finish importing; don’t open HDRP nested packages |
| Can’t grab bat | Click **Game** view; confirm Device Simulator + XR Interaction Manager + EventSystem are in the scene |
| Items break on Play / freefall smash | Should be fixed (grab-only break + seated props). If props still fall through table, re-run move bootstrap / raise `TableTopY` |
| No break | Grab the bat first, then hit a nearby smashable (coffee table), not the sofa/fridge |
| Scripts missing / compile errors | Wait for import; Console → clear; reopen project with Unity 6 |
| Scene empty / wrong scene | Open `CIPAT_SmashHouse`, not `SampleScene` |

---

## 6. What to record for CIPAT (optional)

- 20–40s screen recording: grab → smash → sound
- Hierarchy screenshot
- `BreakableObject` inspector screenshot (audio + haptic fields)

More notes: `docs/cipat-demo-notes.md`

---

## Quick path (TL;DR)

1. Clone repo  
2. Hub → open `BE/Sem 7/avr/VirtualHouseSmash`  
3. Open `Assets/Scenes/CIPAT_SmashHouse`  
4. Play → grip bat → smash vase  
