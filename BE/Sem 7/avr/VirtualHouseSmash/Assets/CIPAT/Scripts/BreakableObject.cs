using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit.Interactables;

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
