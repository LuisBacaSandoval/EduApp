import { useEffect, useRef, useState } from "react";

export function useSpeechRecognition({
    lang = "es-ES",
    onResult,
    onError,
    onEnd,
} = {}) {
    const recognitionRef = useRef(null);
    const [isSupported, setIsSupported] = useState(false);
    const [isListening, setIsListening] = useState(false);

    useEffect(() => {
        const SpeechRecognition =
            window.SpeechRecognition || window.webkitSpeechRecognition;

        if (!SpeechRecognition) {
            setIsSupported(false);
            return;
        }

        const recognition = new SpeechRecognition();
        recognition.lang = lang;
        recognition.continuous = true;
        recognition.interimResults = false;

        recognition.onresult = (event) => {
            const lastResult = event.results[event.results.length - 1];
            const transcript = lastResult[0].transcript.trim();
            if (onResult) onResult(transcript);
        };

        recognition.onerror = (event) => {
            console.error("Speech recognition error:", event);
            if (onError) onError(event);
            setIsListening(false);
        };

        recognition.onend = () => {
            setIsListening(false);
            if (onEnd) onEnd();
        };

        recognitionRef.current = recognition;
        setIsSupported(true);

        return () => {
            recognition.stop();
        };
    }, [lang, onResult, onError, onEnd]);

    const start = () => {
        if (!recognitionRef.current || isListening) return;
        try {
            recognitionRef.current.start();
            setIsListening(true);
        } catch (e) {
            console.error("Error al iniciar reconocimiento:", e);
        }
    };

    const stop = () => {
        if (!recognitionRef.current || !isListening) return;
        recognitionRef.current.stop();
        setIsListening(false);
    };

    return {
        isSupported,
        isListening,
        start,
        stop,
    };
}
