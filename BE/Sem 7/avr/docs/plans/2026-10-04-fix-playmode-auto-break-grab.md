# Fix Play Mode Auto-Break + Bat Grab Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Stop smashables from exploding the instant Play starts, and make the bat reliably grabbable with XR Device Simulator / headset so the CIPAT demo is usable.

**Architecture:** Two independent root causes. (1) Physics: bat + props are non-kinematic with gravity and spawn slightly above the coffee table, so they freefall on Play; any Weapon-tagged bat contact above ~1.2 m/s triggers `BreakableObject`. Fix by seating objects on the table, keeping the bat kinematic until grabbed, and ignoring break collisions unless the bat is currently selected. (2) Interaction: smash scene has XR Origin + Device Simulator but is missing the `XR Interaction Manager` (+ `EventSystem`) that the XRIT DemoScene includes—add those so grabs resolve. Do not auto-parent the bat into the hand unless we add an explicit demo “start with bat” option later.

**Tech Stack:** Unity 6000.6 URP, XR Interaction Toolkit 3.6.1, OpenXR, existing `Cipat.BreakableObject` / `Bat.prefab` / editor bootstraps.

---

### Task 1: Harden `BreakableObject` so freefall cannot false-trigger

**Files:**
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/BreakableObject.cs`
- Modify (optional mirror): keep editor bootstrap thresholds as-is

**Step 1: Change break gate to require an actively selected bat**

In `OnCollisionEnter`, after the `Weapon` tag check, require the bat’s `XRGrabInteractable` to currently have a selecting interactor. Soft contacts from a loose falling bat must no-op.

Replace the collision handler body logic with:

```csharp
void OnCollisionEnter(Collision collision)
{
    if (broken) return;
    if (collision.collider == null) return;
    if (!collision.collider.CompareTag("Weapon")) return;

    var grab = collision.collider.GetComponentInParent<XRGrabInteractable>();
    if (grab == null) return;
    if (grab.interactorsSelecting == null || grab.interactorsSelecting.Count == 0)
        return; // loose / falling bat — ignore

    if (collision.relativeVelocity.magnitude < breakSpeedThreshold) return;

    broken = true;
    ContactPoint contact = collision.GetContact(0);
    if (breakSound != null)
        AudioSource.PlayClipAtPoint(breakSound, contact.point);

    for (int i = 0; i < grab.interactorsSelecting.Count; i++)
        HapticUtil.PulseFromInteractor(grab.interactorsSelecting[i], hapticAmplitude, hapticDuration);

    SpawnDebris(contact.point, collision.relativeVelocity);

    if (disableInsteadOfDestroy)
        gameObject.SetActive(false);
    else
        Destroy(gameObject);
}
```

Remove the old `TryHapticFromBat` helper if it becomes unused.

**Step 2: Sanity-check in Editor (manual)**

Play Mode briefly: props may still fall/settle, but they must **not** despawn/play break audio until the bat is grabbed and swung.

**Step 3: Commit**

```bash
git add "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/BreakableObject.cs"
git commit -m "$(cat <<'MSG'
fix(avr): only break smashables when bat is grabbed

Loose freefall Weapon contacts were firing BreakableObject on Play.
MSG
)"
```

---

### Task 2: Keep bat stable until grab (kinematic until select)

**Files:**
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Prefabs/Bat.prefab` (via bootstrap preferred)
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatBatBootstrap.cs`
- Re-run bootstrap OR edit prefab + scene instance so scene picks up changes

**Step 1: Update bat bootstrap defaults**

In `CipatBatBootstrap.BuildOrUpdateBatPrefab`:
- Set `rb.isKinematic = true` and `rb.useGravity = false` while idle on the table.
- Keep `XRGrabInteractable` with `movementType = VelocityTracking`, `throwOnDetach = true`.
- Subscribe via a tiny runtime helper (preferred) so grab/select toggles physics:

Create `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/GrabPhysicsToggle.cs`:

```csharp
using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit;
using UnityEngine.XR.Interaction.Toolkit.Interactables;

namespace Cipat
{
    [RequireComponent(typeof(Rigidbody))]
    [RequireComponent(typeof(XRGrabInteractable))]
    public class GrabPhysicsToggle : MonoBehaviour
    {
        Rigidbody rb;
        XRGrabInteractable grab;

        void Awake()
        {
            rb = GetComponent<Rigidbody>();
            grab = GetComponent<XRGrabInteractable>();
            SetIdle();
        }

        void OnEnable()
        {
            grab.selectEntered.AddListener(OnSelectEntered);
            grab.selectExited.AddListener(OnSelectExited);
        }

        void OnDisable()
        {
            grab.selectEntered.RemoveListener(OnSelectEntered);
            grab.selectExited.RemoveListener(OnSelectExited);
        }

        void OnSelectEntered(SelectEnterEventArgs _)
        {
            rb.isKinematic = false;
            rb.useGravity = true;
        }

        void OnSelectExited(SelectExitEventArgs _)
        {
            // After throw/drop, keep dynamic so it can land.
            rb.isKinematic = false;
            rb.useGravity = true;
        }

        void SetIdle()
        {
            rb.isKinematic = true;
            rb.useGravity = false;
            rb.linearVelocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
        }
    }
}
```

Note: if this Unity version still uses `rb.velocity` (not `linearVelocity`), use `velocity` / `angularVelocity` accordingly.

Add the component in `CipatBatBootstrap` when building the prefab.

**Step 2: Rebuild bat into scene**

Run existing bat bootstrap from Unity batch / menu equivalent so `Bat.prefab` + scene instance refresh at coffee-table pose `(-13, 0.85, -6.7)`.

If batch is inconvenient, manually: open prefab, set Rigidbody kinematic+no gravity, add `GrabPhysicsToggle`, save; confirm scene instance follows.

**Step 3: Commit**

```bash
git add \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Scripts/GrabPhysicsToggle.cs" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatBatBootstrap.cs" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Prefabs/Bat.prefab" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity"
git commit -m "$(cat <<'MSG'
fix(avr): keep bat kinematic on table until grabbed
MSG
)"
```

---

### Task 3: Seat smashables on the coffee table (stop freefall pileup)

**Files:**
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatMoveBreakablesBootstrap.cs`
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity` (via bootstrap)

**Evidence:** `(Prb)CoffeTable` is at `(-13.024, 0.326, -6.887)`. Smashables were moved to y=`0.95` around `(-13, -6.7)` with non-kinematic gravity—above the tabletop—so they fall on Play and slam into each other / the bat.

**Step 1: Change move bootstrap anchor**

Use table-relative placement:

```csharp
// Tabletop ~ coffee table origin y + small lift for collider bottoms.
static readonly Vector3 Anchor = new Vector3(-13.02f, 0.72f, -6.89f);
```

Tune `0.72` in Play Mode once so prop bottoms rest on the mesh (not sink, not hover >2cm). Prefer setting each prop’s y from its collider bounds after move:

```csharp
// After setting xz, drop y so collider bottom sits on tableY.
const float TableTopY = 0.70f; // tune
var col = go.GetComponent<Collider>();
float bottom = col != null ? col.bounds.min.y : go.transform.position.y;
float delta = TableTopY - bottom;
go.transform.position += new Vector3(0f, delta, 0f);
```

Also set smashable Rigidbodies to **wake carefully**: keep dynamic OK once seated; optional `rb.Sleep()` after place in bootstrap does not persist—skip. Rely on Task 1 gate + good seating.

**Step 2: Strip duplicate child BoxColliders on wired vases**

Vase1/2/3 currently have **root** `BoxCollider` (added by breakable bootstrap) **and** child mesh `BoxCollider`s → double collision mass/jitter. In `CipatBreakableBootstrap.EnsureNonTriggerCollider` / a one-shot cleanup: if root has a solid collider, disable or remove redundant child BoxColliders that match the same bounds (keep MeshColliders only if non-convex issues—prefer single root box for smashables).

Minimal cleanup in move/breakable bootstrap after wire:

```csharp
foreach (var c in go.GetComponentsInChildren<Collider>(true))
{
    if (c.gameObject == go) continue;
    if (c is BoxCollider)
        Object.DestroyImmediate(c);
}
```

**Step 3: Re-run move bootstrap, Play-test settle**

Expect: on Play, props stay put (or tiny settle), no break audio, bat still on table.

**Step 4: Commit**

```bash
git add \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatMoveBreakablesBootstrap.cs" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatBreakableBootstrap.cs" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity"
git commit -m "$(cat <<'MSG'
fix(avr): seat smashables on coffee table and drop duplicate colliders
MSG
)"
```

---

### Task 4: Add XR Interaction Manager + EventSystem to smash scene

**Files:**
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatXrBootstrap.cs` (`SetupSmashHouseScene`)
- Modify: `BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity`
- Reference: `BE/Sem 7/avr/VirtualHouseSmash/Assets/Samples/XR Interaction Toolkit/3.6.1/Starter Assets/DemoScene.unity` (has both)

**Evidence:** Smash scene has `XR Origin (XR Rig)` + `XR Device Simulator` but **zero** `XR Interaction Manager` / `EventSystem` objects. DemoScene has both. Bat `m_InteractionManager: {fileID: 0}` (auto-find). Without a manager in-scene, grab select is unreliable depending on XRIT version/auto-create timing.

**Step 1: Extend `SetupSmashHouseScene`**

After ensuring XR Origin / Device Simulator:

```csharp
EnsureXrInteractionManager();
EnsureEventSystem();
```

Implement:

```csharp
static void EnsureXrInteractionManager()
{
    if (Object.FindFirstObjectByType<UnityEngine.XR.Interaction.Toolkit.XRInteractionManager>() != null)
        return;
    var go = new GameObject("XR Interaction Manager");
    go.AddComponent<UnityEngine.XR.Interaction.Toolkit.XRInteractionManager>();
}

static void EnsureEventSystem()
{
    if (Object.FindFirstObjectByType<UnityEngine.EventSystems.EventSystem>() != null)
        return;
    var go = new GameObject("EventSystem");
    go.AddComponent<UnityEngine.EventSystems.EventSystem>();
    // Prefer XR UI input module if type exists; else standalone Input System UI module.
    var xrUi = System.Type.GetType("UnityEngine.XR.Interaction.Toolkit.UI.XRUIInputModule, Unity.XR.Interaction.Toolkit");
    if (xrUi != null) go.AddComponent(xrUi);
    else go.AddComponent<UnityEngine.InputSystem.UI.InputSystemUIInputModule>();
}
```

Adjust namespaces/type names to match XRIT 3.6.1 in this project (check DemoScene components if compile fails).

**Step 2: Run `SetupSmashHouseScene` (or manually add the two objects once)**

Confirm Hierarchy shows:
- XR Origin (XR Rig)
- XR Device Simulator
- XR Interaction Manager
- EventSystem

**Step 3: Play Mode grab check**

1. Click **Game** view (focus required for Device Simulator).
2. Use simulator controls to move hand to bat and grip/select.
3. Bat should attach and follow.

If still dead: verify Project Settings → Active Input Handling is **Input System Package** or **Both** (currently `activeInputHandler: 2` = Both — OK).

**Step 4: Commit**

```bash
git add \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/CIPAT/Editor/CipatXrBootstrap.cs" \
  "BE/Sem 7/avr/VirtualHouseSmash/Assets/Scenes/CIPAT_SmashHouse.unity"
git commit -m "$(cat <<'MSG'
fix(avr): add XR Interaction Manager and EventSystem to smash scene
MSG
)"
```

---

### Task 5: Update friend instructions + demo notes

**Files:**
- Modify: `BE/Sem 7/avr/instructions.md`
- Modify: `BE/Sem 7/avr/docs/cipat-demo-notes.md`

**Step 1: Document expected start state**

Add/adjust:
- Bat starts **on the coffee table**, not already in hand — grab it first.
- Click Game view before using Device Simulator keys/mouse.
- Props should stay intact until you swing the grabbed bat.
- Troubleshooting row: “Items break on Play” → outdated after fix; replace with “If props fall through table, re-run move bootstrap / raise TableTopY”.

**Step 2: Commit**

```bash
git add "BE/Sem 7/avr/instructions.md" "BE/Sem 7/avr/docs/cipat-demo-notes.md"
git commit -m "$(cat <<'MSG'
docs(avr): clarify bat grab start and Play Mode troubleshooting
MSG
)"
```

---

### Task 6: End-to-end verification (manual CIPAT checklist)

**Step 1: Play Mode checklist**

1. Open `Assets/Scenes/CIPAT_SmashHouse.unity`
2. Press Play
3. **Pass:** no break sounds; smashables remain active
4. Click Game view; use Device Simulator to grip bat
5. **Pass:** bat follows hand
6. Swing into a vase/container
7. **Pass:** break sound + object disables + debris
8. Soft tap **Pass:** no break below threshold

**Step 2: Push when green**

```bash
git push
```

---

## Out of scope (do not do in this fix)

- Auto-spawning the bat parented to the controller on Play
- Full mesh fracture / GPU shatter
- Retuning every furniture collider in the house pack
- Git LFS migration for the unitypackage
