import Home from "./pages/Home";
import DashboardPage from "./pages/DashboardPage";
import TheoryPage from "./pages/TheoryPage";
import PracticePage from "./pages/PracticePage";
import FastPracticePage from "./pages/FastPracticePage";
import HelpPage from "./pages/HelpPage";
import PersonalizePage from "./pages/PersonalizePage";
import PracticeStudents from "./pages/PracticeStudents";

export const routes = [
  { path: "/", element: <Home /> },
  { path: "/personalize-content", element: <PersonalizePage /> },
  { path: "/dashboard", element: <DashboardPage /> },
  { path: "/theory", element: <TheoryPage /> },
  { path: "/tutor", element: <PracticePage /> },
  { path: "/fast-practice", element: <FastPracticePage /> },
  { path: "/practice-students", element: <PracticeStudents /> },
  { path: "/help", element: <HelpPage /> },
];
