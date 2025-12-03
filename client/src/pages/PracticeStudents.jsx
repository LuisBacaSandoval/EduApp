import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import Sidebar from "../components/SideBar";
import RightPanel from "../components/RightPanel";
import { supabase } from "../lib/supabaseClient";

const uuidRegex =
  /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

const PracticeStudents = () => {
  const { search } = useLocation();
  const [data, setData] = useState([]);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [studentName, setStudentName] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(null);
  const [correctCount, setCorrectCount] = useState(0);
  const [incorrectCount, setIncorrectCount] = useState(0);

  const code = useMemo(() => {
    const params = new URLSearchParams(search);
    return params.get("code");
  }, [search]);

  const isValid = useMemo(() => {
    return typeof code === "string" && uuidRegex.test(code);
  }, [code]);

  useEffect(() => {
    fetchData();
  }, []);

  async function fetchData() {
    const { data, error } = await supabase
      .from("questions")
      .select("*")
      .eq("code", code)
      .maybeSingle();

    if (error) {
      console.error("Error obteniendo la pregunta:", error);
      setData(null);
    } else {
      setData(data);
    }
  }

  const handleAnswerSelect = (qId, answerIndex) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [qId]: answerIndex,
    }));
  };

  const handleSubmitResponses = async () => {
    if (!studentName.trim()) {
      alert("Por favor ingresa tu nombre antes de enviar.");
      return;
    }
    setSubmitting(true);
    try {
      const questions = data.data.questions;

      let correct = 0;
      let incorrect = 0;

      questions.forEach((q) => {
        if (selectedAnswers[q.id] === q.correctAnswer) correct++;
        else incorrect++;
      });

      const computedScore = Math.round((correct / questions.length) * 100);

      const { error } = await supabase.from("student_responses").insert([
        {
          name: studentName,
          correct_answers: correct,
          incorrect_answers: incorrect,
          score: computedScore,
          code,
        },
      ]);

      if (error) {
        console.error(error);
        alert("Hubo un error guardando tus respuestas");
      } else {
        setCorrectCount(correct);
        setIncorrectCount(incorrect);
        setScore(computedScore);
        setSubmitted(true);
      }
    } catch (err) {
      console.error(err);
      alert("Hubo un error guardando tus respuestas");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex flex-row h-screen">
      <Sidebar />

      <div className="flex flex-4 p-8 flex-col bg-white max-h-screen overflow-y-auto">
        <h1 className="text-3xl font-bold mb-3 text-primary">
          Práctica para Estudiantes
        </h1>
        {!code && (
          <div className="p-4 mb-4 bg-yellow-50 border border-yellow-200 rounded">
            <p className="text-sm text-yellow-800">
              Falta el parámetro <strong>code</strong> en la URL.
            </p>
            <p className="text-xs text-gray-600">
              Ejemplo:{" "}
              <code>
                /practice-students?code=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
              </code>
            </p>
          </div>
        )}

        {code && !isValid && (
          <div className="p-4 mb-4 bg-red-50 border border-red-200 rounded">
            <p className="text-sm text-red-700">
              El código proporcionado no tiene el formato UUID correcto.
            </p>
          </div>
        )}

        {code && isValid && data && (
          <>
            <div className="p-3 mb-4 bg-green-50 border border-green-200 rounded">
              <p className="text-sm text-green-700">
                Código válido: <strong>{code}</strong>
              </p>
            </div>

            <div className="mb-6">
              <label className="font-medium">Tu nombre:</label>
              <input
                type="text"
                className="border border-gray-300 rounded-md p-2 w-full mt-1"
                placeholder="Ingresa tu nombre completo"
                value={studentName}
                onChange={(e) => setStudentName(e.target.value)}
                disabled={submitting || submitted}
              />
            </div>

            {submitted && (
              <div className="p-4 mb-4 bg-white border border-gray-200 rounded-lg">
                <h2 className="text-2xl font-bold text-gray-800 mb-2">
                  ¡Gracias {studentName}!
                </h2>
                <p className="text-lg text-indigo-600 font-semibold mb-1">
                  {score}%
                </p>
                <p className="text-sm text-gray-700">
                  Correctas: <strong>{correctCount}</strong> — Incorrectas:{" "}
                  <strong>{incorrectCount}</strong>
                </p>
              </div>
            )}

            {/* 📌 Render preguntas */}
            {data.data?.questions?.length > 0 ? (
              <div className="space-y-6">
                {data.data.questions.map((q, index) => (
                  <div
                    key={q.id}
                    className={
                      `p-4 rounded-lg border ` +
                      (submitted
                        ? selectedAnswers[q.id] === q.correctAnswer
                          ? "bg-green-50 border-green-300"
                          : "bg-red-50 border-red-300"
                        : "bg-gray-50 border-gray-200 shadow-sm")
                    }
                  >
                    <h3 className="text-lg font-semibold mb-2">
                      {index + 1}. {q.content}
                    </h3>

                    {/* 📌 Alternativas */}
                    <ul className="space-y-2">
                      {q.possibleAnswers.map((answer, i) => (
                        <li key={i}>
                          <label
                            className={`flex items-center gap-2 cursor-pointer ${
                              submitted ? "opacity-90" : ""
                            }`}
                          >
                            <input
                              type="radio"
                              name={`question-${q.id}`}
                              value={answer}
                              className="accent-primary"
                              onChange={() => handleAnswerSelect(q.id, i)}
                              checked={selectedAnswers[q.id] === i}
                              disabled={submitting || submitted}
                            />
                            <span>{answer}</span>
                          </label>
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}

                <button
                  className="mt-6 bg-primary text-white font-semibold py-2 px-4 rounded-md hover:bg-primary-dark transition disabled:opacity-60 disabled:cursor-not-allowed"
                  onClick={handleSubmitResponses}
                  disabled={submitting || submitted}
                >
                  {submitting ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg
                        className="animate-spin h-4 w-4"
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
                      Enviando...
                    </span>
                  ) : submitted ? (
                    "Enviado"
                  ) : (
                    "Enviar respuestas"
                  )}
                </button>
              </div>
            ) : (
              <p className="text-red-600">
                No hay preguntas para esta práctica.
              </p>
            )}
          </>
        )}

        {!data && code && isValid && (
          <div className="p-4 mb-4 bg-red-50 border border-red-200 rounded">
            <p className="text-sm text-red-700">
              No se encontró ninguna pregunta para el código proporcionado.
            </p>
          </div>
        )}
      </div>

      <RightPanel />
    </div>
  );
};

export default PracticeStudents;
