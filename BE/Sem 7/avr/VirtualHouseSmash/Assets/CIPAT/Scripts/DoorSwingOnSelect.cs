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
            grab.trackPosition = false;
            grab.trackRotation = false;
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
            var mgr = grab.interactionManager;
            if (mgr == null) return;
            for (int i = grab.interactorsSelecting.Count - 1; i >= 0; i--)
                mgr.SelectExit(grab.interactorsSelecting[i], grab);
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
