import Home from "./pages/Home";
import DashboardPage from "./pages/DashboardPage";
import TheoryPage from "./pages/TheoryPage";
import PracticePage from "./pages/PracticePage";
import HelpPage from "./pages/HelpPage";

export const routes = [
  { path: "/", element: <Home /> },
  { path: "/dashboard", element: <DashboardPage /> },
  { path: "/theory", element: <TheoryPage /> },
  { path: "/practice", element: <PracticePage /> },
  { path: "/help", element: <HelpPage /> },
];
