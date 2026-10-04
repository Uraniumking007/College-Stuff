# CIPAT Demo Notes — Smash Room

- Environment: single **CIPAT_SmashRoom** (JC_LP floor/walls/roof + colliders); nappin house shell removed from play scene
- Play scene: `VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity`
- Entry: XR Origin spawns **outside** → grip door (**Space**=right hand, **G**=grip on door) → one-shot swing open → enter
- Room contents: coffee table + orange bat + seated smashables; sofa; MediaConsole + smashable **TvScreen**; colliding walls/floor/roof
- Interaction: XRIT 3.6 grab bat (`Weapon` tag) + physics collision break **only while bat is selected**
- Scene wiring: XR Origin + XR Device Simulator + XR Interaction Manager + EventSystem (`XRUIInputModule`)
- Auditory: `AudioSource.PlayClipAtPoint` on break (`Assets/CIPAT/Audio/*.wav`)
- Haptic: `XRBaseInputInteractor.SendHapticImpulse` via `Cipat.HapticUtil`
- Bat: starts **kinematic on coffee table center** (`GrabPhysicsToggle`); bright orange for Device Simulator; not pre-parented into hand
- Smashables: vase1–3, smallPlant, Container1–2 (table); **TvScreen** (console stand stays when screen breaks)
- Door: `(Prb)Door` + `DoorSwingOnSelect` — opens ~90° once on select, stays open
- Demo path: Unity Editor + XR Device Simulator (click **Game** view for input focus)
- Later: Android OpenXR build for Galaxy XR headset

## Acceptance checklist

1. Open `CIPAT_SmashHouse`, press Play — spawn **outside**; door visible; **no** multi-room House Interior
2. Walk into wall → blocked (re-run room bootstrap if not)
3. Click Game view; Device Simulator moves headset + controllers
4. Hand on door → hold **G** (grip) → door swings open once and stays open
5. Enter → table/bat/vases, sofa, MediaConsole + **TvScreen** present
6. Grab bat from table center → swing vase → prop disables/hides + sound + brief debris
7. Grab bat → smash **TvScreen** → screen disables; console remains
8. Soft tap / ungrabbed bat → no break
9. Already-broken prop does not retrigger

## Troubleshooting (quick)

| Symptom | Do this |
|--------|---------|
| Stuck outside | Grip door: hand on door + **G** |
| Walk through walls | Re-run `CipatSmashRoomBootstrap` |
| Can’t find bat | Orange bat on coffee table **center** |

## Note on haptics in Editor

Device Simulator often will not physically vibrate. The haptic call still runs in code for headset builds / writeup evidence.
