import { CircleDot, Clock, NotebookPen, Trophy } from "lucide-react";

import Sidebar from "../components/SideBar";
import Card from "../components/Card";

import image1 from "../assets/dashboard/card_placeholder_1.png";
import image2 from "../assets/dashboard/card_placeholder_2.png";
import image3 from "../assets/dashboard/card_placeholder_3.png";
import image4 from "../assets/dashboard/card_placeholder_4.png";
import image5 from "../assets/dashboard/recomended_placeholder_1.png";

const DashboardPage = () => {
  return (
    <div className="flex flex-row h-screen">
      <Sidebar />
      {/* Main Content */}
      <div className="flex flex-4 flex-col bg-white p-4">
        <h1 className="text-4xl font-semibold mb-4">Dashboard</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl">
          {/* Card 1 - Generar teoría */}
          <Card
            title="Generar teoría"
            subtitle="Crea tu material de estudio"
            to={"/theory"}
            features={[
              "Contenido automático personalizado",
              "Adaptado a tu nivel"
            ]}
            image={image1}
          />

          {/* Card 2 - Genera preguntas */}
          <Card
            title="Genera preguntas"
            subtitle="Crea tus preguntas de estudio"
            to={"/practice"}
            features={[
              "Preguntas variadas por nivel",
              "Retroalimentación inmediata"
            ]}
            image={image2}
          />

          {/* Card 3 - Aprendizaje rápido */}
          <Card
            title="Aprendizaje rápido"
            subtitle="Crea preguntas rápidas"
            to={"#"}
            features={[
              "Sesiones rápidas de estudio",
              "Aprende con voz y gestos"
            ]}
            image={image3}
          />

          {/* Card 4 - Otros usuarios */}
          <Card
            title="Otros usuarios"
            subtitle="Compara tus resultados"
            to={"#"}
            features={[
              "Compite con otros usuarios",
              "Sube en el ranking global"
            ]}
            image={image4}
          />
        </div>

        <div className="flex flex-1 flex-col mt-4">
          <h2 className="text-4xl font-semibold mb-4">Recomendados para ti</h2>
          <div className="relative">
            <img src={image5} className="w-64 rounded-2xl" />
            <text className="absolute top-3/5 z-10 bg-white w-64 text-black text-center font-bold text-2xl">Arte</text>
          </div>
        </div>
      </div>

      {/* Right Side - Exclusive from Dashboard */}
      <div className="flex flex-1 flex-col bg-indigo-600 p-4 gap-y-3">
        <h1 className="text-2xl font-semibold mb-4">Rendimiento</h1>

        <div className="bg-white rounded-2xl flex flex-row p-2 justify-between">
          <div className="flex flex-col">
            <h4 className="text-base font-semibold">Último quizz</h4>
            <h6 className="text-xs">Resultados de tu último quizz</h6>
            <span className="text-base">9/10</span>
          </div>
          <div className="bg-indigo-500 w-12 h-12 rounded-md self-center flex items-center justify-center">
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
    </div>
  );
};

export default DashboardPage;
