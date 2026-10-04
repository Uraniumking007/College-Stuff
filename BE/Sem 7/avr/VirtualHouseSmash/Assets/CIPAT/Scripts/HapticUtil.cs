using UnityEngine;
using UnityEngine.XR.Interaction.Toolkit.Interactors;

namespace Cipat
{
    public static class HapticUtil
    {
        public static void PulseFromInteractor(IXRInteractor interactor, float amplitude, float duration)
        {
            if (interactor == null) return;
            amplitude = Mathf.Clamp01(amplitude);
            duration = Mathf.Max(0f, duration);

            // XRIT 3.x: XRBaseInputInteractor.SendHapticImpulse (replaces XRBaseControllerInteractor.xrController).
            if (interactor is XRBaseInputInteractor inputInteractor)
                inputInteractor.SendHapticImpulse(amplitude, duration);
        }
    }
}
