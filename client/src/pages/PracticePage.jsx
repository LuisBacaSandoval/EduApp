import { useState } from "react";
import { Download, Award, CheckCircle, XCircle } from "lucide-react";

import Sidebar from "../components/SideBar";
import RightPanel from "../components/RightPanel";
import API_CLIENT from "../lib/api.config";

const PracticePage = () => {
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [quizData, setQuizData] = useState(null);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(null);
  const [error, setError] = useState('');


  /* Upload PDF */
  const validateFile = (file) => {
    if (file.type !== 'application/pdf') {
      setError('Por favor selecciona solo archivos PDF');
      return false;
    }
    setError('');
    return true;
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file && validateFile(file)) {
      setSelectedFile(file);
    }
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files.length > 0) {
      const file = files[0];
      if (validateFile(file)) {
        setSelectedFile(file);
      }
    }
  };

  const handleRemoveFile = () => {
    if (!loading) {
      setSelectedFile(null);
      setError('');
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  };


  /* Handle answers */
  const handleSubmit = async (e) => {
    e.preventDefault();

    setLoading(true);

    try {
      if (selectedFile == null) {
        setError('Por favor selecciona un archivo PDF antes de enviar.');
        setLoading(false);
        return;
      }

      const formData = new FormData();
      formData.append('file', selectedFile);
      const response = await API_CLIENT.post("/pdf/generar-preguntas", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        }
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

      if (serverContent.trim().length === 0) {
        throw new Error(fallback);
      }

      setQuizData(JSON.parse(serverContent));
      setAnswers({});
      setSubmitted(false);
      setScore(0);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Ocurrió un problema al generar el contenido.");
      setSelectedFile(null);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionId, answerIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  }

  const handleSubmitAnswer = () => {
    let correctCount = 0;
    quizData.questions.forEach(question => {
      if (answers[question.id] === question.correctAnswer) {
        correctCount++;
      }
    });

    setScore(correctCount);
    setSubmitted(true);
  }

  const resetQuiz = () => {
    setAnswers({});
    setSubmitted(false);
    setScore(0);
  }

  if (!quizData) {
    return (
      <div className="flex flex-row h-screen">
        <Sidebar />

        {/* Main Content */}
        <div className="flex flex-4 p-8 flex-col bg-white">
          <h1 className="text-3xl font-bold mb-3 text-primary">Evaluación Rápida</h1>
          <p className="text-lg text-gray-700 mb-6">Pon a prueba tu conocimiento con preguntas de opción múltiple.</p>
          <form
            onSubmit={handleSubmit}
            className="border-2 border-indigo-200 rounded-2xl p-6"
          >
            <div className="flex flex-col mb-4">
              <span className="font-semibold mb-2 text-xl">Subir PDF</span>
              <div className="space-y-4">
                <input
                  type="file"
                  accept=".pdf,application/pdf"
                  onChange={handleFileChange}
                  className="hidden"
                  id="pdf-input"
                />

                {!selectedFile && (<label
                  htmlFor="pdf-input"
                  onDragEnter={handleDragEnter}
                  onDragOver={handleDragOver}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                  className={`
            flex flex-col items-center justify-center
            px-6 py-12 border-2 border-dashed rounded-lg
            cursor-pointer transition-all duration-200
            ${isDragging
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-300 bg-gray-50 hover:bg-gray-100'
                    }
          `}
                >
                  <Download className={`w-12 h-12 mb-4 ${isDragging ? 'text-blue-500' : 'text-gray-400'}`} />
                  <p className="mb-2 text-sm text-gray-700">
                    <span className="font-semibold">Haz clic para subir</span> o arrastra y suelta
                  </p>
                  <p className="text-xs text-gray-500">
                    Solo archivos PDF
                  </p>
                </label>)}

                {error && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
                    <p className="text-sm text-red-600">{error}</p>
                  </div>
                )}

                {selectedFile && (
                  <div className="p-4 bg-white border border-gray-200 rounded-lg shadow-sm">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3 flex-1">
                        <div className="shrink-0">
                          <svg
                            className="w-10 h-10 text-red-500"
                            fill="currentColor"
                            viewBox="0 0 20 20"
                          >
                            <path
                              fillRule="evenodd"
                              d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4z"
                              clipRule="evenodd"
                            />
                          </svg>
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 truncate">
                            {selectedFile.name}
                          </p>
                          <p className="text-xs text-gray-500">
                            {formatFileSize(selectedFile.size)}
                          </p>
                        </div>
                      </div>
                      <button
                        onClick={handleRemoveFile}
                        className="ml-4 p-1 hover:bg-gray-100 rounded transition-colors"
                        title="Eliminar archivo"
                      >
                        <svg
                          className="w-5 h-5 text-gray-500 hover:text-red-500"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M6 18L18 6M6 6l12 12"
                          />
                        </svg>
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>

            <div className="flex justify-center">
              <button
                type="submit"
                disabled={loading}
                className={`bg-indigo-600 text-white px-8 py-3 rounded-xl w-1/2 transition-colors cursor-pointer ${loading
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
        </div>

        <RightPanel />
      </div>
    )
  }

  if (submitted) {
    const percentage = (score / quizData.questions.length) * 100;
    return (
      <div className="flex flex-row h-screen">
        <Sidebar />

        {/* Main Content */}
        <div className="flex flex-4 p-8 flex-col bg-white overflow-hidden">
          <h1 className="text-3xl font-bold mb-3 text-primary">Evaluación Rápida</h1>
          <p className="text-lg text-gray-700 mb-6">Pon a prueba tu conocimiento con preguntas de opción múltiple.</p>

          {/* Display score */}
          <div className="text-center mb-6">
            <Award className={`w-20 h-20 mx-auto mb-4 ${percentage >= 70 ? 'text-green-500' : 'text-orange-500'}`} />
            <h2 className="text-3xl font-bold text-gray-800 mb-2">¡Quiz Completado!</h2>
            <p className="text-5xl font-bold text-indigo-600 mb-2">{score}/{quizData.questions.length}</p>
            <p className="text-xl text-gray-600">{percentage.toFixed(0)}% correcto</p>
          </div>

          <div className="space-y-4 mb-6 h-full overflow-y-auto">
            {quizData.questions.map((question) => {
              const userAnswerIndex = answers[question.id];
              const correctAnswerIndex = question.correctAnswer;
              const isCorrect = userAnswerIndex === correctAnswerIndex;
              const userAnswerText = userAnswerIndex !== undefined ? question.possibleAnswers[userAnswerIndex] : 'Sin responder';
              const correctAnswerText = question.possibleAnswers[correctAnswerIndex];

              return (
                <div key={question.id} className={`p-4 rounded-lg border-2 ${isCorrect ? 'bg-green-50 border-green-300' : 'bg-red-50 border-red-300'}`}>
                  <div className="flex items-start gap-3">
                    {isCorrect ? (
                      <CheckCircle className="w-6 h-6 text-green-600 shrink-0 mt-1" />
                    ) : (
                      <XCircle className="w-6 h-6 text-red-600 shrink-0 mt-1" />
                    )}
                    <div className="flex-1">
                      <p className="font-semibold text-gray-800 mb-2">{question.content}</p>
                      <p className="text-sm text-gray-600">
                        <span className="font-medium">Tu respuesta:</span> {userAnswerText}
                      </p>
                      {!isCorrect && (
                        <p className="text-sm text-green-700 mt-1">
                          <span className="font-medium">Respuesta correcta:</span> {correctAnswerText}
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          <button
            onClick={resetQuiz}
            className="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition"
          >
            Intentar de Nuevo
          </button>
        </div>

        <RightPanel />
      </div>
    )
  }

  const allQuestionsAnswered = Object.keys(answers).length === quizData.questions.length;

  return (
    <div className="flex flex-row h-screen">
      <Sidebar />

      {/* Main Content */}
      <div className="flex flex-4 p-8 flex-col bg-white overflow-hidden">
        <h1 className="text-3xl font-bold mb-3 text-primary">Evaluación Rápida</h1>
        <p className="text-lg text-gray-700 mb-6">Pon a prueba tu conocimiento con preguntas de opción múltiple.</p>

        {/* Display quiz */}
        <div className="bg-white rounded-lg shadow-xl p-8 h-full overflow-y-auto">
          <div className="space-y-8">
            {quizData.questions.map((question, index) => (
              <div key={question.id} className="border-b border-gray-200 pb-6 last:border-b-0">
                <h3 className="text-lg font-semibold text-gray-800 mb-4">
                  {index + 1}. {question.content}
                </h3>

                <div className="space-y-3">
                  {question.possibleAnswers.map((answer, answerIndex) => (
                    <div
                      key={answerIndex}
                      onClick={() => handleAnswerChange(question.id, answerIndex)}
                      className={`flex items-start p-4 rounded-lg border-2 cursor-pointer transition ${answers[question.id] === answerIndex
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200 hover:border-indigo-300 hover:bg-gray-50'
                        }`}
                    >
                      <div className={`w-5 h-5 rounded-full border-2 mt-0.5 mr-3 flex items-center justify-center shrink-0 ${answers[question.id] === answerIndex
                        ? 'border-indigo-600 bg-indigo-600'
                        : 'border-gray-300'
                        }`}>
                        {answers[question.id] === answerIndex && (
                          <div className="w-2 h-2 bg-white rounded-full"></div>
                        )}
                      </div>
                      <span className="text-gray-700 flex-1">{answer}</span>
                    </div>
                  ))}
                </div>
              </div>
            ))}

            <button
              onClick={handleSubmitAnswer}
              disabled={!allQuestionsAnswered}
              className="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-indigo-700 transition disabled:bg-gray-300 disabled:cursor-not-allowed"
            >
              {allQuestionsAnswered
                ? 'Enviar Respuestas'
                : `Responde todas las preguntas (${Object.keys(answers).length}/${quizData.questions.length})`}
            </button>
          </div>
        </div>
      </div>

      <RightPanel />
    </div>
  );
};

export default PracticePage;
