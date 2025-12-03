// Devuelve true si algún comando hizo match
export function handleVoiceCommand(transcript, navigate) {
    const text = transcript.toLowerCase();
    console.log("Comando de voz:", text);

    if (text.includes("inicio") || text.includes("dashboard")) {
        navigate("/dashboard");
        return { matched: true, command: "inicio", route: "/dashboard" };
    }

    if (text.includes("teoría") || text.includes("teoria") || text.includes("generar")) {
        navigate("/theory");
        return { matched: true, command: "teoria", route: "/theory" };
    }

    if (text.includes("práctica") || text.includes("practica") || text.includes("ejercicio")) {
        navigate("/practice");
        return { matched: true, command: "practica", route: "/pracitice" };
    }

    if (
        text.includes("configuración") ||
        text.includes("configuraciones") ||
        text.includes("configuracion") ||
        text.includes("ajustes") ||
        text.includes("personalización") ||
        text.includes("personalizacion")
    ) {
        navigate("/personalize-content");
        return { matched: true, command: "configuración", route: "/personalize-content" };
    }

    if (text.includes("cerrar sesión") || text.includes("cerrar sesion") || text.includes("salir")) {
        navigate("/");
        return { matched: true, command: "logout", route: "/" };
    }

    if (text.includes("ayuda")) {
        navigate("/help")
        return { matched: true, command: "ayuda", route: "/help" };
    }

    if (text.includes("atrás") || text.includes("atras") || text.includes("volver")) {
        navigate(-1);
        return { matched: true, command: "atrás", route: "back" };
    }

    if (text.includes("adelante")) {
        navigate(1);
        return { matched: true, command: "adelante", route: "forward" };
    }

    return { matched: false, command: null, route: null };
}
