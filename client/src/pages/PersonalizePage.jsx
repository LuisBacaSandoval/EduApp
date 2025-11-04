import { useState } from "react";
import image1 from "../assets/gesture.jpg";
import image2 from "../assets/keyboard.jpg";
import image3 from "../assets/microphone.jpg";

const interactionMethods = [
  {
    id: 1,
    label: "Click",
    color: "bg-segment-1",
    image: image1,
  },
  {
    id: 2,
    label: "Escribe",
    color: "bg-segment-2",
    image: image2,
  },
  {
    id: 3,
    label: "Voz",
    color: "bg-segment-3",
    image: image3,
  },
  {
    id: 4,
    label: "Elige interacción",
    color: "bg-segment-4",
    image: null,
  },
];

const PersonalizePage = () => {
  const [selected, setSelected] = useState(null);

  return (
    <div className="min-h-screen w-full bg-primary flex flex-col items-center justify-center p-6">
      <main className="w-full max-w-4xl mx-auto text-center space-y-12">
        <div className="space-y-4">
          <h1 className="text-5xl md:text-6xl font-bold text-white drop-shadow-lg">
            Personaliza tu forma de interactuar
          </h1>
        </div>

        <div className="w-full flex justify-center">
          <div className="relative w-full max-w-md mx-auto">
            {/* Circular segments */}
            <div className="relative aspect-square w-full">
              <div className="absolute inset-0 grid grid-cols-2 gap-4">
                {interactionMethods.map((method, index) => (
                  <button
                    key={method.id}
                    onClick={() => setSelected(method.id)}
                    className={`
                relative overflow-hidden rounded-3xl
                ${method.color} bg-opacity-20 backdrop-blur-sm
                border-4 border-white/30
                transition-all duration-300 hover:scale-105 hover:bg-opacity-30
                ${selected === method.id ? "ring-4 ring-white scale-105" : ""}
                ${index === 0 ? "rounded-tl-[100px]" : ""}
                ${index === 1 ? "rounded-tr-[100px]" : ""}
                ${index === 2 ? "rounded-bl-[100px]" : ""}
                ${index === 3 ? "rounded-br-[100px]" : ""}
              `}
                  >
                    <div className="absolute inset-0">
                      {/* If an image is provided, show it; otherwise show the requested text block */}
                      {method.image ? (
                        <img
                          src={method.image}
                          alt={method.label}
                          className="w-full h-full object-cover"
                        />
                      ) : (
                        <div className="w-full h-full flex items-center justify-center p-4 text-left">
                          <div className="text-white">
                            <p className="text-lg leading-tight">
                              Controlar la app con cámara, voz o de forma
                              normal.
                            </p>
                            <p className="mt-2 text-sm opacity-90">
                              Tú decides cómo aprender.
                            </p>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* Glow effect */}
                    <div
                      className={`
                absolute inset-0 ${method.color} opacity-0 hover:opacity-20 
                transition-opacity duration-300 animate-pulse-glow
              `}
                    />
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default PersonalizePage;
