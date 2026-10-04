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
            // Zero velocities while still dynamic — Unity 6 rejects velocity writes on kinematic bodies.
            rb.linearVelocity = Vector3.zero;
            rb.angularVelocity = Vector3.zero;
            rb.useGravity = false;
            rb.isKinematic = true;
        }
    }
}
