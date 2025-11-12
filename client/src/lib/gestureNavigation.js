export default function createGestureHandler(navigate, options = {}) {
  const cooldownMs = options.cooldownMs ?? 1500;
  let lastGesture = null;
  let lastTime = 0;

  const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y);

  function isFingerExtended(landmarks, tipIdx, pipIdx) {
    // For upright hands: tip.y < pip.y means the finger is extended (y grows downward)
    if (!landmarks[tipIdx] || !landmarks[pipIdx]) return false;
    return landmarks[tipIdx].y < landmarks[pipIdx].y;
  }

  function detectGesture(landmarks) {
    if (!landmarks || landmarks.length < 21) return null;

    // approximate palm/hand scale using wrist (0) to middle_finger_mcp (9)
    const palmSize = Math.max(0.001, dist(landmarks[0], landmarks[9]));

    // thumb - index pinch distance
    const thumbIndexDist = dist(landmarks[4], landmarks[8]);

    const indexExtended = isFingerExtended(landmarks, 8, 6);
    const middleExtended = isFingerExtended(landmarks, 12, 10);
    const ringExtended = isFingerExtended(landmarks, 16, 14);
    const pinkyExtended = isFingerExtended(landmarks, 20, 18);

    const extendedCount = [
      indexExtended,
      middleExtended,
      ringExtended,
      pinkyExtended,
    ].filter(Boolean).length;

    // Zero: thumb touching index (pinch) — threshold is proportional to palm size
    if (thumbIndexDist < palmSize * 0.35) {
      return "zero";
    }

    // One: only index is extended
    if (extendedCount === 1 && indexExtended) {
      return "one";
    }

    // Two: index and middle extended, ring and pinky not extended
    if (
      extendedCount === 2 &&
      indexExtended &&
      middleExtended &&
      !ringExtended &&
      !pinkyExtended
    ) {
      return "two";
    }

    return null;
  }

  return function handleHands(multiHandLandmarks) {
    try {
      if (!multiHandLandmarks || multiHandLandmarks.length === 0) return;

      // Use the first detected hand for gesture (could be extended later)
      const landmarks = multiHandLandmarks[0];
      const g = detectGesture(landmarks);
      if (!g) return;

      const now = Date.now();
      if (g === lastGesture && now - lastTime < cooldownMs) return; // cooldown

      lastGesture = g;
      lastTime = now;

      if (g === "zero") {
        // go to dashboard
        navigate("/dashboard");
      } else if (g === "one") {
        // go to theory
        navigate("/theory");
      } else if (g === "two") {
        // go to practice
        navigate("/practice");
      }
    } catch (err) {
      console.debug("gesture handler error", err);
    }
  };
}
