import { useState } from 'react';
import { LayoutDashboard, BookOpen, ListChecks, Users, HelpCircle, Settings, LogOut, Trophy, ChevronRight, ChevronLeft } from 'lucide-react';
import SidebarButton from './SidebarButton.jsx';

export default function Sidebar() {

  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <div className={`h-screen bg-linear-to-b from-indigo-600 to-indigo-700 flex flex-col transition-all duration-300 relative overflow-clip ${isCollapsed ? 'w-20' : 'w-64'}`}>
      {/* User Profile Section */}
      {/* TODO: Replace hardcode data with actual data from backend */}
      <div className="p-4">
        <div className={`bg-white rounded-2xl shadow-lg transition-all duration-300 ${isCollapsed ? 'p-1.5' : 'p-3'}`}>
          {!isCollapsed ? (
            <>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-linear-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center">
                    <span className="text-white font-semibold text-lg">U</span>
                  </div>
                  <div>
                    <p className="font-semibold text-gray-800">Usuario</p>
                    <p className="text-xs text-gray-500">usuario@mail.com</p>
                  </div>
                </div>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-indigo-600 font-medium">105 PTS</span>
                <div className="flex items-center gap-1">
                  <span className="text-gray-700 font-medium">54</span>
                  <Trophy className="w-4 h-4 text-yellow-500" />
                </div>
              </div>
            </>
          ) : (
            <div className="flex flex-col items-center gap-2">
              <div className="w-10 h-10 bg-linear-to-br from-blue-400 to-indigo-500 rounded-full flex items-center justify-center">
                <span className="text-white font-semibold text-lg">U</span>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="flex-1 px-4 space-y-3">
        <SidebarButton icon={LayoutDashboard} isCollapsed={isCollapsed} to={"/dashboard"}>Dashboard</SidebarButton>
        <SidebarButton icon={BookOpen} isCollapsed={isCollapsed} to={"/theory"}>Teoría</SidebarButton>
        <SidebarButton icon={ListChecks} isCollapsed={isCollapsed} to={"/practice"}>Práctica</SidebarButton>
        <SidebarButton icon={Users} isCollapsed={isCollapsed}>Comunidad</SidebarButton>
        <SidebarButton icon={HelpCircle} isCollapsed={isCollapsed} to={"/help"}>Ayuda</SidebarButton>
      </nav>

      {/* Bottom Navigation */}
      <div className="p-4 space-y-3">
        <SidebarButton icon={Settings} isCollapsed={isCollapsed} to={"/personalize-content"}>Ajustes</SidebarButton>
        <SidebarButton icon={LogOut} isCollapsed={isCollapsed} to={"/"} >Salir</SidebarButton>
      </div>

      {/* Toggle Button */}
      <button
        onClick={() => setIsCollapsed(!isCollapsed)}
        className="absolute top-1/2 -translate-y-1/12 -right-6 bg-white hover:bg-gray-50 rounded-lg p-2 shadow-lg transition-all duration-300 cursor-pointer hover:scale-110 z-20 border-2 border-indigo-200"
        aria-label={isCollapsed ? 'Expandir sidebar' : 'Contraer sidebar'}
      >
        {isCollapsed ? (
          <ChevronRight className="w-5 h-5 text-indigo-600 relative right-3" />
        ) : (
          <ChevronLeft className="w-5 h-5 text-indigo-600 relative right-3" />
        )}
      </button>
    </div>
  );
}