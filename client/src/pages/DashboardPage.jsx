import Sidebar from "../components/SideBar";
import Card from "../components/Card";

import image1 from "../assets/dashboard/card_placeholder_1.png";
import image2 from "../assets/dashboard/card_placeholder_2.png";
import image3 from "../assets/dashboard/card_placeholder_3.png";
import image4 from "../assets/dashboard/card_placeholder_4.png";
import image5 from "../assets/dashboard/recomended_placeholder_1.png";
import RightPanel from "../components/RightPanel";

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
              //"Retroalimentación inmediata"
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

      <RightPanel />
    </div>
  );
};

export default DashboardPage;
