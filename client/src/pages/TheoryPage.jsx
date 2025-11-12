import React, { useState } from "react";
import Sidebar from "../components/SideBar";
import RightExclusivePanel from "../components/RightExclusivePanel";
import API_CLIENT from "../lib/api.config";

const TheoryPage = () => {
  const recommendedTopics = ["Matemática", "Ciencia", "Programación"];

  const [topic, setTopic] = useState("");
  const [loading, setLoading] = useState(false);
  const [generatedContent, setGeneratedContent] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!topic) {
      alert(
        "Por favor ingresa un tema de estudio o selecciona uno recomendado."
      );
      return;
    }

    setLoading(true);
    setGeneratedContent("");

    try {
      const response = await API_CLIENT.post("api/teoria/generar", {
        tema: topic,
      });

      const fallback = "Ocurrió un problema al generar el contenido.";

      const serverContentRaw =
        response?.data?.contenido ||
        response?.data?.texto ||
        response?.data ||
        "";

      let serverContent = "";
      if (serverContentRaw && typeof serverContentRaw === "object") {
        serverContent =
          serverContentRaw.teoria ||
          serverContentRaw.contenido ||
          serverContentRaw.texto ||
          JSON.stringify(serverContentRaw, null, 2);
      } else {
        serverContent = String(serverContentRaw || "");
      }

      setGeneratedContent(serverContent || fallback);
    } catch (err) {
      console.error(err);
      setGeneratedContent("Ocurrió un problema al generar el contenido.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-row min-h-screen">
      <Sidebar />

      <main className="flex-1 p-8 flex items-start">
        <div className="w-full max-w-3xl">
          <h1 className="text-3xl font-bold mb-3 text-primary">
            Construye tu conocimiento
          </h1>
          <p className="text-lg text-gray-700 mb-6">
            Genera teoría personalizada y conviértete en el protagonista de tu
            propio aprendizaje.
          </p>

          <form
            onSubmit={handleSubmit}
            className="border-2 border-indigo-200 rounded-2xl p-6"
          >
            <div className="flex flex-col mb-4">
              <label
                htmlFor="study-topic"
                className="font-semibold mb-2 text-xl"
              >
                Tema de estudio
              </label>
              <input
                id="study-topic"
                type="text"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="Inteligencia artificial"
                className="w-full border rounded-md h-10 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </div>

            <div className="mb-4">
              <h3 className="font-semibold text-lg mb-3">Temas recomendados</h3>
              <div className="flex flex-wrap">
                {recommendedTopics.map((t) => (
                  <button
                    key={t}
                    type="button"
                    onClick={() => setTopic(t)}
                    className="mr-3 mb-3 px-4 py-2 rounded-md text-sm bg-black text-white inline-block hover:opacity-90"
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex justify-center">
              <button
                type="submit"
                disabled={loading}
                className={`bg-indigo-600 text-white px-8 py-3 rounded-xl w-1/2 transition-colors ${
                  loading
                    ? "opacity-60 cursor-not-allowed"
                    : "hover:bg-indigo-700"
                }`}
              >
                {loading ? (
                  <span className="flex items-center justify-center gap-3">
                    <svg
                      className="animate-spin h-5 w-5"
                      xmlns="http://www.w3.org/2000/svg"
                      fill="none"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                      ></circle>
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                      ></path>
                    </svg>
                    Generando...
                  </span>
                ) : (
                  "Generar"
                )}
              </button>
            </div>
          </form>

          {/* Área donde se muestra el contenido generado */}
          {generatedContent && (
            <div className="max-h-[50vh] mt-6 p-6 border rounded-2xl bg-white shadow-sm overflow-y-auto">
              {(() => {
                const lines = String(generatedContent).split("\n");
                const first = lines[0] || "";
                const rest = lines.slice(1).join("\n");

                if (first.startsWith("## ")) {
                  return (
                    <div>
                      <h2 className="text-2xl font-bold mb-3">
                        {first.replace(/^##\s+/, "")}
                      </h2>
                      <p className="text-gray-700 whitespace-pre-line">
                        {rest || generatedContent.replace(/^##\s+.*\n?/, "")}
                      </p>
                    </div>
                  );
                }

                return (
                  <p className="text-gray-700 whitespace-pre-line">
                    {generatedContent}
                  </p>
                );
              })()}
            </div>
          )}
        </div>
      </main>

      <RightExclusivePanel />
    </div>
  );
};

export default TheoryPage;
