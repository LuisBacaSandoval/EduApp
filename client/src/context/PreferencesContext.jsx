import { createContext, useState } from "react";

export const PreferencesContext = createContext();

export const PreferencesProvider = ({ children }) => {
  // valores posibles: "camara" | "voz" | "normal"
  const [interactionMode, setInteractionMode] = useState("normal");

  const value = { interactionMode, setInteractionMode };

  return (
    <PreferencesContext.Provider value={value}>
      {children}
    </PreferencesContext.Provider>
  );
};
