import { useEffect, useRef } from "react";
import { Hands } from "@mediapipe/hands";
import { Camera } from "@mediapipe/camera_utils";

export default function HandTracking() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    let camera = null;
    let resizeObserver = null;
    const hands = new Hands({
      locateFile: (file) => {
        return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
      },
    });

    hands.setOptions({
      maxNumHands: 2,
      modelComplexity: 1,
      minDetectionConfidence: 0.7,
      minTrackingConfidence: 0.7,
    });

    hands.onResults(onResults);

    function onResults(results) {
      const canvasCtx = canvasRef.current.getContext("2d");
      canvasCtx.save();
      canvasCtx.clearRect(
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );
      canvasCtx.drawImage(
        results.image,
        0,
        0,
        canvasRef.current.width,
        canvasRef.current.height
      );

      if (results.multiHandLandmarks) {
        for (const landmarks of results.multiHandLandmarks) {
          drawLandmarks(canvasCtx, landmarks);
        }
      }
      canvasCtx.restore();
    }

    function drawLandmarks(ctx, landmarks) {
      ctx.fillStyle = "red";
      for (const point of landmarks) {
        ctx.beginPath();
        ctx.arc(
          point.x * canvasRef.current.width,
          point.y * canvasRef.current.height,
          4,
          0,
          2 * Math.PI
        );
        ctx.fill();
      }
    }

    function getContainerSize() {
      const el = containerRef.current;
      if (!el) return { width: 640, height: 480 };
      const width = Math.max(32, el.clientWidth); // avoid zero
      const height = Math.round((width * 3) / 4); // 4:3 aspect
      return { width, height };
    }

    function setupCamera() {
      const { width, height } = getContainerSize();

      // set canvas drawing buffer to match displayed size
      const canvas = canvasRef.current;
      if (canvas) {
        canvas.width = width;
        canvas.height = height;
        // make it scale responsively via CSS
        canvas.style.width = "100%";
        canvas.style.height = "auto";
      }

      if (
        typeof videoRef.current !== "undefined" &&
        videoRef.current !== null
      ) {
        // if a previous camera exists, try to stop it
        try {
          if (camera && typeof camera.stop === "function") camera.stop();
        } catch {
          // ignore
        }

        camera = new Camera(videoRef.current, {
          onFrame: async () => {
            await hands.send({ image: videoRef.current });
          },
          width,
          height,
        });
        camera.start();
      }
    }

    // initial setup
    setupCamera();

    // respond to container resizes
    if (window.ResizeObserver && containerRef.current) {
      resizeObserver = new ResizeObserver(() => {
        setupCamera();
      });
      resizeObserver.observe(containerRef.current);
    } else {
      // fallback: window resize
      const onResize = () => setupCamera();
      window.addEventListener("resize", onResize);
      // cleanup will remove it
      resizeObserver = {
        disconnect: () => window.removeEventListener("resize", onResize),
      };
    }
    return () => {
      try {
        if (camera && typeof camera.stop === "function") camera.stop();
      } catch {
        // ignore
      }
      try {
        if (resizeObserver && typeof resizeObserver.disconnect === "function")
          resizeObserver.disconnect();
      } catch {
        // ignore
      }
    };
  }, []);

  return (
    <div ref={containerRef} className="flex flex-col items-center w-full">
      <video ref={videoRef} className="hidden" playsInline></video>
      <canvas
        ref={canvasRef}
        className="border rounded-lg shadow-md w-full h-auto"
      ></canvas>
    </div>
  );
}
