import RightPanel from "../components/RightPanel";
import Sidebar from "../components/SideBar";

const PracticePage = () => {
  return (
    <div className="flex flex-row h-screen">
      <Sidebar />
      {/* Main Content */}
      <div className="flex flex-4 p-8 flex-col bg-white">
        <h1 className="text-3xl font-bold mb-3 text-primary">Tutor virtual</h1>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-7xl">
          CONTENIDO
        </div>
      </div>

      <RightPanel />
    </div>
  );
};

export default PracticePage;
