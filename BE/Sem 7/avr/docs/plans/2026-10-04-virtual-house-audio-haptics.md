# Virtual House Smash — Audio + Haptics Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Reuse the friend's `virtual_house_cipat.unitypackage` house art and add XR grab-bat smash gameplay with impact audio and controller haptic feedback for a CIPAT/AVR demo (Editor + Device Simulator first).

**Architecture:** Import the existing interior pack into a Unity URP project, drop XR Interaction Toolkit origin into a working copy of the house scene, add one grabable bat and a single `BreakableObject` behaviour on a few small props (vases/lamp/containers). On bat collision: play clip at point, `SendHapticImpulse` on the grabbing controller, spawn simple debris, disable the prop. No mesh fracture, no custom networking.

**Tech Stack:** Unity 6 LTS or 2022.3 LTS · URP (already in package settings) · XR Plugin Management + OpenXR · XR Interaction Toolkit + XR Device Simulator · Unity Input System (already in package)

**Base art (do not rebuild):** `virtual_house_cipat.unitypackage`  
**Primary scene source:** `Assets/nappin/HouseInteriorPack/HouseInteriorPack.unity`  
**Working scene to create:** `Assets/Scenes/CIPAT_SmashHouse.unity`  
**Design ref:** `docs/plans/2026-10-04-galaxy-vr-smash-room-design.md`

---

## Gap reminder (from package audit)

| Have | Need |
|------|------|
| House meshes/prefabs/scenes | XR Origin + Device Simulator |
| Static colliders on props | Rigidbody + break script on smashables |
| Input System actions asset | XRIT grab + bat prefab |
| — | Audio clips + `PlayClipAtPoint` |
| — | `SendHapticImpulse` path |
| — | Debris prefab |

---

### Task 1: Create Unity project and import house package

**Files:**
- Create: Unity project at `BE/Sem 7/avr/VirtualHouseSmash/`
- Import: `BE/Sem 7/avr/virtual_house_cipat.unitypackage`
- Verify: scenes under `Assets/nappin/HouseInteriorPack/`

**Step 1: Install editor if needed**

- Open Unity Hub → Install **Unity 6000.x LTS** or **2022.3 LTS**
- Modules: **Android Build Support** optional today; needed later for Galaxy

**Step 2: Create project**

- Hub → New Project → **3D (URP)** template
- Name: `VirtualHouseSmash`
- Location: `BE/Sem 7/avr/`

**Step 3: Import package**

- In Unity: `Assets → Import Package → Custom Package…`
- Select `BE/Sem 7/avr/virtual_house_cipat.unitypackage`
- Import **All**

**Step 4: Verify import**

- Project window shows `Assets/nappin/HouseInteriorPack/Prefabs` with vases, fridge, lamp, etc.
- Open `Assets/nappin/HouseInteriorPack/HouseInteriorPack.unity` — house visible in Scene view
- Console: fix only blocking pink-material/URP errors
- Ignore nested `.unitypackage` files inside `JC_LP_House_Lite` unless materials are broken

**Step 5: Add Unity gitignore, then commit scaffolding**

Create `BE/Sem 7/avr/VirtualHouseSmash/.gitignore` with at least:

```
/[Ll]ibrary/
/[Tt]emp/
/[Oo]bj/
/[Bb]uild/
/[Bb]uilds/
/[Ll]ogs/
/[Uu]ser[Ss]ettings/
*.csproj
*.unityproj
*.sln
*.pidb
*.suo
```

```bash
cd "/Users/bhaveshpatil/Documents/github/College-Stuff"
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets" \
        "BE/Sem 7/avr/VirtualHouseSmash/Packages" \
        "BE/Sem 7/avr/VirtualHouseSmash/ProjectSettings" \
        "BE/Sem 7/avr/VirtualHouseSmash/.gitignore" \
        "BE/Sem 7/avr/docs/plans"
git status
git commit -m "$(cat <<'EOF'
feat(avr): import virtual house Unity project for CIPAT smash demo

EOF
)"
```

Expected: commit contains Assets/Packages/ProjectSettings, **not** `Library/`.

---

### Task 2: Install XR packages and Device Simulator

**Files:**
- Modify via Package Manager: `Packages/manifest.json`
- Modify: `ProjectSettings/` XR and Player settings

**Step 1: Enable XR Plugin Management**

- `Edit → Project Settings → XR Plugin Management` → Install if prompted
- Desktop tab: enable **OpenXR**
- Android tab optional now: enable **OpenXR** for later Galaxy builds

**Step 2: Install XR Interaction Toolkit**

- `Window → Package Manager` → Unity Registry
- Install **XR Interaction Toolkit**
- `Edit → Project Settings → Player → Active Input Handling` = **Input System Package** or **Both**

**Step 3: Import XRIT samples**

- Package Manager → XR Interaction Toolkit → Samples → Import:
  - **Starter Assets**
  - **XR Device Simulator**

**Step 4: OpenXR interaction profiles**

- `Project Settings → XR Plug-in Management → OpenXR`
- Add common controller profiles for later device testing (e.g. Meta Quest Touch / Oculus Touch)
- Editor play uses Device Simulator

**Step 5: Smoke-check and commit**

- No red errors about missing XR Interaction assemblies

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Packages/manifest.json" \
        "BE/Sem 7/avr/VirtualHouseSmash/Packages/packages-lock.json" \
        "BE/Sem 7/avr/VirtualHouseSmash/ProjectSettings"
git commit -m "feat(avr): add OpenXR and XR Interaction Toolkit"
```

---

### Task 3: Add XR Origin + Device Simulator to house scene

**Files:**
- Create: `Assets/Scenes/CIPAT_SmashHouse.unity` (duplicate of house scene)
- Modify that scene with XR Origin + Device Simulator prefabs from XRIT samples

**Step 1: Duplicate playable scene**

- Open `Assets/nappin/HouseInteriorPack/HouseInteriorPack.unity`
- `File → Save As` → `Assets/Scenes/CIPAT_SmashHouse.unity`
- Work only in the copy

**Step 2: Disable conflicting Main Camera**

- If a lone `Main Camera` will fight XR Origin's camera, disable it

**Step 3: Place XR Origin**

- Drag **XR Origin (XR Rig)** / **XR Origin (Action-based)** from XRIT Starter Assets into the scene
- Put feet on floor in living room / near coffee table
- Face smashable props

**Step 4: Place Device Simulator**

- Drag **XR Device Simulator** prefab into the scene
- Leave enabled for Editor Play Mode

**Step 5: Play Mode sanity check**

- Press Play
- Confirm simulator can move headset/hands
- Stop Play

**Step 6: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity"
git commit -m "feat(avr): add XR Origin and Device Simulator to smash house scene"
```

---

### Task 4: Create bat weapon prefab

**Files:**
- Create: `Assets/CIPAT/Prefabs/Bat.prefab`
- Modify: `Assets/Scenes/CIPAT_SmashHouse.unity`
- Possibly modify: `ProjectSettings/TagManager.asset` (add `Weapon` tag)

**Step 1: Build bat mesh**

- `GameObject → 3D Object → Cylinder` named `Bat`
- Scale approx `(0.04, 0.35, 0.04)` so it reads as a bat/club

**Step 2: Physics + grab components**

On root `Bat` add:
- `Rigidbody` (gravity on, Collision Detection = Continuous Dynamic)
- Collider (capsule/cylinder; convex if mesh collider)
- `XR Grab Interactable` (Action-based)
- Tag: `Weapon`
- Movement Type: **Velocity Tracking** preferred for smash feel

**Step 3: Prefab and place**

- Save as `Assets/CIPAT/Prefabs/Bat.prefab`
- Leave one instance on a reachable table in `CIPAT_SmashHouse`

**Step 4: Verify grab in Play Mode**

- Play → grip/grab bat → bat follows hand
- If grab fails: ensure XR Origin has Input Action Manager referencing Starter Assets actions

**Step 5: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Prefabs/Bat.prefab" \
        "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity" \
        "BE/Sem 7/avr/VirtualHouseSmash/ProjectSettings/TagManager.asset"
git commit -m "feat(avr): add XR grabable bat prefab"
```

---

### Task 5: Add haptic helper + breakable script

**Files:**
- Create: `Assets/CIPAT/Scripts/HapticUtil.cs`
- Create: `Assets/CIPAT/Scripts/BreakableObject.cs`

**Step 1: Create folders**

- `Assets/CIPAT/Scripts`
- `Assets/CIPAT/Audio`
- `Assets/CIPAT/Prefabs` (if missing)

**Step 2: Write `HapticUtil.cs`**

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

namespace Cipat
{
    public static class HapticUtil
    {
        public static void Pulse(XRBaseController controller, float amplitude, float duration)
        {
            if (controller == null) return;
            amplitude = Mathf.Clamp01(amplitude);
            duration = Mathf.Max(0f, duration);
            controller.SendHapticImpulse(amplitude, duration);
        }

        public static void PulseFromInteractor(IXRInteractor interactor, float amplitude, float duration)
        {
            if (interactor is XRBaseControllerInteractor controllerInteractor)
                Pulse(controllerInteractor.xrController, amplitude, duration);
        }
    }
}
```

If your XRIT version renamed types, adapt to the local `SendHapticImpulse` controller API. Keep one null-safe pulse helper.

**Step 3: Write `BreakableObject.cs`**

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;

namespace Cipat
{
    [RequireComponent(typeof(Collider))]
    public class BreakableObject : MonoBehaviour
    {
        [SerializeField] AudioClip breakSound;
        [SerializeField] [Range(0f, 1f)] float hapticAmplitude = 0.7f;
        [SerializeField] float hapticDuration = 0.08f;
        [SerializeField] float breakSpeedThreshold = 1.2f;
        [SerializeField] GameObject debrisPrefab;
        [SerializeField] int debrisCount = 5;
        [SerializeField] float debrisForce = 2f;
        [SerializeField] bool disableInsteadOfDestroy = true;

        bool broken;

        void OnCollisionEnter(Collision collision)
        {
            if (broken) return;
            if (collision.collider == null) return;
            if (!collision.collider.CompareTag("Weapon")) return;
            if (collision.relativeVelocity.magnitude < breakSpeedThreshold) return;

            broken = true;

            ContactPoint contact = collision.GetContact(0);
            if (breakSound != null)
                AudioSource.PlayClipAtPoint(breakSound, contact.point);

            TryHapticFromBat(collision.collider);
            SpawnDebris(contact.point, collision.relativeVelocity);

            if (disableInsteadOfDestroy)
                gameObject.SetActive(false);
            else
                Destroy(gameObject);
        }

        void TryHapticFromBat(Collider batCollider)
        {
            var grab = batCollider.GetComponentInParent<XRGrabInteractable>();
            if (grab == null) return;

            var interactors = grab.interactorsSelecting;
            for (int i = 0; i < interactors.Count; i++)
                HapticUtil.PulseFromInteractor(interactors[i], hapticAmplitude, hapticDuration);
        }

        void SpawnDebris(Vector3 point, Vector3 hitVelocity)
        {
            if (debrisPrefab == null || debrisCount <= 0) return;

            for (int i = 0; i < debrisCount; i++)
            {
                var piece = Instantiate(
                    debrisPrefab,
                    point + Random.insideUnitSphere * 0.05f,
                    Random.rotation);
                var rb = piece.GetComponent<Rigidbody>();
                if (rb != null)
                {
                    rb.AddForce(
                        (hitVelocity.normalized + Random.insideUnitSphere) * debrisForce,
                        ForceMode.Impulse);
                }
                Destroy(piece, 3f);
            }
        }
    }
}
```

**Step 4: Compile check**

- Return to Unity and wait for compile
- Expected: 0 errors
- If `interactorsSelecting` is missing in your XRIT version, use `grab.firstInteractorSelecting` and pulse once

**Step 5: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts"
git commit -m "feat(avr): add BreakableObject and HapticUtil"
```

---

### Task 6: Debris prefab + audio clips

**Files:**
- Create: `Assets/CIPAT/Prefabs/DebrisChunk.prefab`
- Add: `Assets/CIPAT/Audio/glass_break.wav` (or `.ogg`)
- Add: `Assets/CIPAT/Audio/ceramic_thud.wav`
- Optional: `Assets/CIPAT/Audio/wood_thud.wav`

**Step 1: Debris prefab**

- Small Cube scale `(0.05, 0.05, 0.05)`
- Add `Rigidbody`
- Save as `DebrisChunk`
- No extra script; `BreakableObject` destroys pieces after 3s

**Step 2: Import 2–3 short SFX**

- Use license-OK clips (Kenney / Freesound CC0 / similar)
- Put under `Assets/CIPAT/Audio`
- Do **not** submit the CIPAT demo with silent breaks

**Step 3: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Prefabs/DebrisChunk.prefab" \
        "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Audio"
git commit -m "feat(avr): add debris prefab and break audio clips"
```

---

### Task 7: Convert selected house props into smashables

**Files:**
- Modify: `Assets/Scenes/CIPAT_SmashHouse.unity`
- Optional create: `Assets/CIPAT/Prefabs/Breakable_Vase1.prefab` (variant)
- Prefer small props:
  - `(Prb)LaunchTable_vase1` … `vase4`
  - `(Prb)Lamp`
  - `(Prb)Container1` / `Container2`
  - `(Prb)CoffeTable_smallPlant`
- Avoid day-1: fridge, sofa, wardrobe, walls

**Step 1: Optional tag `Breakable`**

- Tag Manager → add `Breakable` for debugging

**Step 2: For each of 4–6 target instances**

1. Select instance
2. Uncheck **Static**
3. Add `Rigidbody` (mass ~0.3–1.0)
4. Ensure non-trigger collider exists
5. Add `BreakableObject`
6. Assign sound + `DebrisChunk`
7. Tune:
   - glass/vase: amp `0.7`, duration `0.08`, threshold `1.0–1.5`
   - wood/container: amp `0.4`, duration `0.12`, threshold `1.5–2.0`

**Step 3: Make a prefab variant after first success**

- Stamp more breakables from `Breakable_Vase1` instead of redoing components

**Step 4: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity" \
        "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Prefabs" \
        "BE/Sem 7/avr/VirtualHouseSmash/ProjectSettings/TagManager.asset"
git commit -m "feat(avr): wire breakable props with audio and haptics fields"
```

---

### Task 8: Play Mode verification + CIPAT evidence

**Files:**
- Create: `BE/Sem 7/avr/docs/cipat-demo-notes.md`
- Tune only as needed: thresholds / bat collider

**Step 1: Acceptance checklist**

1. Play `CIPAT_SmashHouse`
2. Simulator moves headset + controllers
3. Grab bat
4. Swing into vase → prop disables/hides
5. Break sound plays
6. Debris appears briefly
7. No exception spam
8. Already-broken prop does not retrigger
9. Soft tap below threshold does not break

**Step 2: Haptics in Editor**

- Device Simulator often will not physically vibrate
- Optional temporary `Debug.Log` in `HapticUtil.Pulse` proves the call fired
- Remove noisy logs before final recording

**Step 3: Record evidence**

- 20–40s screen recording
- Hierarchy screenshot: XR Origin, Bat, breakables
- Inspector screenshot: `BreakableObject` audio/haptic fields

**Step 4: Notes file**

```markdown
# CIPAT Demo Notes — Virtual House Smash

- Environment: nappin HouseInteriorPack (imported)
- Interaction: XRIT grab bat + physics collision break
- Auditory: AudioSource.PlayClipAtPoint on break
- Haptic: controller SendHapticImpulse via HapticUtil
- Demo path: Unity Editor + XR Device Simulator
- Later: Android OpenXR build for Galaxy XR headset
```

**Step 5: Commit**

```bash
git add "BE/Sem 7/avr/docs/cipat-demo-notes.md" \
        "BE/Sem 7/avr/VirtualHouseSmash/Assets" \
        "BE/Sem 7/avr/VirtualHouseSmash/ProjectSettings"
git commit -m "docs(avr): CIPAT demo notes and tuned smash scene"
```

---

### Task 9 (optional buffer): Reset helper + Galaxy stub

**Only if Tasks 1–8 are done.**

**Files:**
- Create: `Assets/CIPAT/Scripts/SceneReset.cs`

**Step 1: R-key reset**

```csharp
using UnityEngine;
using UnityEngine.SceneManagement;

namespace Cipat
{
    public class SceneReset : MonoBehaviour
    {
        void Update()
        {
            if (Input.GetKeyDown(KeyCode.R))
                SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex);
        }
    }
}
```

- Empty GameObject `Systems` + `SceneReset`
- Add scene to Build Settings

**Step 2: Galaxy later (docs only today)**

- Android platform + OpenXR when headset exists
- Confirm real controller haptics on device
- No store upload required unless asked

**Step 3: Commit if used**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/SceneReset.cs" \
        "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity" \
        "BE/Sem 7/avr/VirtualHouseSmash/ProjectSettings/EditorBuildSettings.asset"
git commit -m "feat(avr): add R-key scene reset for demo loops"
```

---

## Execution order

1. Project + import house
2. XR packages + simulator
3. XR Origin in scene copy
4. Bat grab prefab
5. `HapticUtil` + `BreakableObject`
6. Debris + audio
7. Mark 4–6 props breakable
8. Verify + record evidence
9. Optional reset / Android notes

## Out of scope

- Real fracture / VFX graphs
- Breaking fridge/sofa
- Multiplayer
- WebXR rewrite
- Perfect Galaxy packaging on day 1

## Risk cheatsheet

| Problem | Fix |
|---------|-----|
| Can't grab | Input Action Manager missing; Active Input Handling not Input System |
| No break | Bat missing `Weapon` tag; prop still Static; threshold too high; no Rigidbody on prop |
| Physics explosion | Continuous Dynamic on bat; lower debris force |
| Pink materials | Stay on URP; avoid HDRP nested package |
| Haptic “broken” in Editor | Expected; log pulse; verify on headset later |
