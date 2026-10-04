# CIPAT Demo Notes — Virtual House Smash

- Environment: nappin HouseInteriorPack (imported via `virtual_house_cipat.unitypackage`)
- Play scene: `VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity`
- Interaction: XRIT 3.6 grab bat (`Weapon` tag) + physics collision break **only while bat is selected**
- Scene wiring: XR Origin + XR Device Simulator + XR Interaction Manager + EventSystem (`XRUIInputModule`)
- Auditory: `AudioSource.PlayClipAtPoint` on break (`Assets/CIPAT/Audio/*.wav`)
- Haptic: `XRBaseInputInteractor.SendHapticImpulse` via `Cipat.HapticUtil`
- Bat: starts **kinematic on coffee table** (`GrabPhysicsToggle`); not pre-parented into hand
- Smashables (seated on coffee table, collider bottoms ≈ y=0.70): vase1–3, smallPlant, Container1–2
- Demo path: Unity Editor + XR Device Simulator (click **Game** view for input focus)
- Later: Android OpenXR build for Galaxy XR headset

## Acceptance checklist

1. Open `CIPAT_SmashHouse`, press Play — props must **not** auto-break
2. Click Game view; Device Simulator moves headset + controllers
3. Grab bat from the table
4. Swing into a vase → prop disables/hides
5. Break sound plays
6. Debris appears briefly
7. Soft tap below threshold does not break
8. Already-broken prop does not retrigger

## Note on haptics in Editor

Device Simulator often will not physically vibrate. The haptic call still runs in code for headset builds / writeup evidence.
