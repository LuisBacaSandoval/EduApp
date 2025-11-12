import React from "react";
import { CircleDot, Clock, NotebookPen, Trophy } from "lucide-react";

export default function RightExclusivePanel({ fixedWidth = false }) {
  const containerClass = `${
    fixedWidth ? "w-64" : "flex-1"
  } max-w-[256px] flex flex-col bg-indigo-600 p-4 gap-y-3`;

  return (
    <div className={containerClass}>
      <h1 className="text-2xl font-semibold mb-4">Rendimiento</h1>

      <div className="bg-white rounded-2xl flex flex-row p-2 justify-between">
        <div className="flex flex-col">
          <h4 className="text-base font-semibold">Último quizz</h4>
          <h6 className="text-xs">Resultados de tu último quizz</h6>
          <span className="text-base">9/10</span>
        </div>
        <div className="bg-primary w-12 h-12 rounded-md self-center flex items-center justify-center">
          <CircleDot className="text-white" />
        </div>
      </div>

      <div className="bg-white rounded-2xl flex flex-row p-2 justify-between">
        <div className="flex flex-col">
          <h4 className="text-base font-semibold">Esta semana</h4>
          <h6 className="text-xs">Total de quizz esta semana</h6>
          <span className="text-base">15</span>
        </div>
        <div className="bg-indigo-500 w-12 h-12 rounded-md self-center flex items-center justify-center">
          <NotebookPen className="text-white" />
        </div>
      </div>

      <div className="bg-white rounded-2xl flex flex-row p-2 justify-between">
        <div className="flex flex-col">
          <h4 className="text-base font-semibold">Total de horas</h4>
          <h6 className="text-xs">Total de horas esta semana</h6>
          <span className="text-base">50h</span>
        </div>
        <div className="bg-indigo-500 w-12 h-12 rounded-md self-center flex items-center justify-center">
          <Clock className="text-white" />
        </div>
      </div>

      <h1 className="text-2xl font-semibold mt-4">Tu Ranking</h1>
      <div className="bg-white rounded-2xl flex flex-col p-2 justify-between">
        <h6 className="self-center text-[0.5rem] ml-5">#54</h6>
        <Trophy className="text-black self-center" />
        <div className="flex flex-col self-center items-center">
          <span className="text-base">105</span>
          <h6 className="text-xs">puntos totales</h6>
        </div>
      </div>
    </div>
  );
}
