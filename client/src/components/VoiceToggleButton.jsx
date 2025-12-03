import { useVoiceContext } from "../context/VoiceContext";

export function VoiceToggleButton() {
    const {
        isSupported,
        isListening,
        enabled,
        activateMic,
        deactivateMic,
        error,
        lastTranscript,
    } = useVoiceContext();

    if (!isSupported) {
        return (
            <div className="text-xs text-red-500">
                Tu navegador no soporta reconocimiento de voz.
            </div>
        );
    }

    const isActive = enabled && isListening;

    return (
        <div className="flex items-center gap-2">
            <button
                type="button"
                onClick={isActive ? deactivateMic : activateMic}
                className={`inline-flex items-center rounded-full px-4 py-2 text-sm font-medium shadow
          transition
          ${isActive
                        ? "bg-red-500 hover:bg-red-600 text-white"
                        : "bg-emerald-500 hover:bg-emerald-600 text-white"
                    }`}
            >
                <span className="mr-2">
                    {isActive ? "Desactivar micrófono" : "Activar micrófono"}
                </span>
                <span
                    className={`h-2 w-2 rounded-full ${isActive ? "bg-green-300" : "bg-gray-200"
                        }`}
                />
            </button>

            {
                lastTranscript && (
                    <span className="text-xs text-gray-400 italic">
                        Comando: "{lastTranscript}"
                    </span>
                )
            }

            {error && (
                <span className="text-xs text-red-500 max-w-xs truncate">
                    {error}
                </span>
            )}
        </div>
    );
}
