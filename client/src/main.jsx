import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.jsx";
import { BrowserRouter } from "react-router-dom";
import { PreferencesProvider } from "./context/PreferencesContext.jsx";
import { VoiceProvider } from "./context/VoiceContext.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <BrowserRouter>
      <PreferencesProvider>
        <VoiceProvider>
          <App />
        </VoiceProvider>
      </PreferencesProvider>
    </BrowserRouter>
  </StrictMode>
);
