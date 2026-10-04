# Galaxy VR Smash Room — Design (CIPAT / AVR)

**Date:** 2026-10-04  
**Course:** BE Sem 7 AVR / CIPAT demo  
**Constraint:** ~under 1 day, beginner Unity, no headset yet  

## Goal

Interactive VR living-room scene: grab a bat, smash appliances/props, get **auditory** + **haptic** feedback. Demo in Unity Editor with XR Device Simulator; same project later targets OpenXR / Android XR for Galaxy XR.

## Non-goals (YAGNI)

- Real-time mesh fracturing
- Multiplayer / networking
- Fancy furniture kits or photoreal room
- Full Galaxy store packaging on day 1
- WebXR or 360-video as primary deliverable

## Approach

**Unity + XR Interaction Toolkit (XRIT) + OpenXR + XR Device Simulator.**

Why: matches “VR environment” wording, real grab/swing interaction, clear audio + haptic code path, works without a headset for the first demo recording.

## Architecture

### Stack

1. Unity 6 LTS (or Unity 2022.3 LTS if already installed)
2. XR Plugin Management + OpenXR
3. XR Interaction Toolkit
4. XR Device Simulator (Editor play mode)

### Scene

- Floor, 4 walls, ceiling (static colliders)
- Table / shelf with **4–6** breakable props (vase, mug, box/TV stand-in, lamp, plates)
- Bat prefab (grab interactable)
- XR Origin (XRIT) + Device Simulator

### Smash loop

1. Player grips bat (`XRGrabInteractable`)
2. Bat collider hits object tagged `Breakable` with velocity above threshold
3. Play impact `AudioClip` at contact point
4. `SendHapticImpulse(amplitude, duration)` on the grabbing controller
5. Spawn a few debris cubes; disable/destroy breakable
6. Optional: score +1 (nice-to-have only)

## Components

### Prefabs

| Prefab | Notes |
|--------|--------|
| `XR_Origin_Setup` | XR Origin + simulator |
| `Bat` | Grab + Rigidbody + Collider, tag `Weapon` |
| `Breakable_*` | Rigidbody + Collider + `BreakableObject` |
| `Debris_Chunk` | Tiny RB cube, despawn ~3s |
| `Room` | Static geometry only |

### Scripts

**`BreakableObject.cs`** (must-have)

- Fields: `breakSound`, `hapticAmplitude`, `hapticDuration`, `debrisPrefab`, `debrisCount`, `breakSpeedThreshold`
- `OnCollisionEnter`: validate weapon + speed → audio → haptic → debris → break once (`broken` flag)

**`HapticUtil.cs`** (tiny helper)

- Null-safe `SendHapticImpulse` on `XRBaseController` / controller from interactor

### Feedback presets

| Material feel | Audio | Haptic |
|---------------|-------|--------|
| Glass / ceramic | Short bright crack | ~0.7 amp, ~0.08 s |
| Wood / plastic | Dull thud | ~0.4 amp, ~0.12 s |

Editor simulator may not physically vibrate; keep the call for headset builds and CIPAT writeup.

## Day plan (~6–8 hours)

1. **0–1.5 h** — Install Unity Hub + editor; create 3D (URP or Built-in) project under `BE/Sem 7/avr/`
2. **1.5–2.5 h** — XR Plugin Management, OpenXR, XRIT, Device Simulator; verify grab in Play Mode
3. **2.5–3.5 h** — Greybox room + table + 4–6 props + bat
4. **3.5–5 h** — `BreakableObject` + audio clips + haptic impulse + debris
5. **5–6 h** — Tune thresholds; record screen demo; screenshots of hierarchy + code
6. **Buffer** — Reset scene (R / button) if time; else document manual Play restart

## Risks & mitigations

| Risk | Mitigation |
|------|------------|
| XR packages fail / version mismatch | Stick to XRIT samples; Built-in pipeline if URP slows you |
| No haptic in Editor | Expected; code path + headset note in writeup; audio is the visible proof |
| Physics jitter / multi-break | Velocity threshold + `broken` flag |
| No Galaxy headset | Editor recording for CIPAT; Android XR / OpenXR build later |

## Galaxy / Android XR later (not day-1)

1. Switch build target to Android
2. Enable OpenXR / Android XR provider as docs require for the device you get
3. Controller profiles + permission/manifest as needed
4. Sideload or device run; verify `SendHapticImpulse` on hardware

## CIPAT evidence checklist

- [ ] Scene hierarchy screenshot (room, bat, breakables, XR Origin)
- [ ] `BreakableObject` collision + haptic snippet
- [ ] Screen recording: grab → swing → smash → sound
- [ ] Short writeup: environment, auditory feedback, haptic feedback, future Galaxy build

## Success criteria

Demo shows a player-controlled bat destroying at least 3 objects with distinct impact sound and a haptic call on hit, runnable in Editor without a headset.
