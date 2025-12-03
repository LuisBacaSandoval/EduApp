import { createContext, useContext, useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { useSpeechRecognition } from "../hooks/useSpeechRecognition";
import { handleVoiceCommand } from "../lib/voiceCommands";
import { PreferencesContext } from "./PreferencesContext";

const VoiceContext = createContext(null);

export function VoiceProvider({ children }) {
    const navigate = useNavigate();

    const { interactionMode } = useContext(PreferencesContext);
    const canActivate = interactionMode === "voz";

    const [enabled, setEnabled] = useState(false);
    const [lastTranscript, setLastTranscript] = useState("");
    const [lastCommand, setLastCommand] = useState(null);
    const [error, setError] = useState(null);

    const onResult = useCallback(
        (transcript) => {
            setLastTranscript(transcript);
            const { matched, command, route } = handleVoiceCommand(transcript, navigate);
            if (matched) {
                setLastCommand({ command, route, at: new Date().toISOString() });
            }
        },
        [navigate]
    );

    const onError = useCallback((event) => {
        setError(event.error || "Error desconocido en reconocimiento de voz");
    }, []);

    const { isSupported, isListening, start, stop } = useSpeechRecognition({
        lang: "es-ES",
        onResult,
        onError,
        onEnd: () => {
            if (enabled && canActivate) {
                start();
            }
        },
    });

    const activateMic = () => {
        if (!isSupported) {
            setError("Tu navegador no soporta reconocimiento de voz.");
            return;
        }
        setEnabled(true);
        start(); // aquí el navegador pedirá permiso al usuario
    };

    const deactivateMic = () => {
        setEnabled(false);
        stop();
    };

    // Si el usuario cierra sesión, apagamos el micro
    useEffect(() => {
        if (!canActivate && enabled) {
            deactivateMic();
        }
    }, [canActivate, enabled]);

    const value = {
        isSupported,
        isListening,
        enabled,
        lastTranscript,
        lastCommand,
        error,
        activateMic,
        deactivateMic,
    };

    return <VoiceContext.Provider value={value}>{children}</VoiceContext.Provider>;
}

export function useVoiceContext() {
    const ctx = useContext(VoiceContext);
    if (!ctx) {
        throw new Error("useVoiceContext debe usarse dentro de <VoiceProvider>");
    }
    return ctx;
}
