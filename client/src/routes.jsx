import Home from "./pages/Home";
import DashboardPage from "./pages/DashboardPage";
import TheoryPage from "./pages/TheoryPage";
import PracticePage from "./pages/PracticePage";
import HelpPage from "./pages/HelpPage";
import PersonalizePage from "./pages/PersonalizePage";

export const routes = [
  { path: "/", element: <Home /> },
  { path: "/personalize-content", element: <PersonalizePage /> },
  { path: "/dashboard", element: <DashboardPage /> },
  { path: "/theory", element: <TheoryPage /> },
  { path: "/practice", element: <PracticePage /> },
  { path: "/help", element: <HelpPage /> },
];
