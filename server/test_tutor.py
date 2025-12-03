import requests
from datetime import datetime

BASE_URL = "http://localhost:8000/api"


def iniciar_tutor(tema: str) -> tuple[str, list[dict]]:
    """Inicia una conversación con UNIprofe y devuelve mensaje inicial + historial."""
    resp = requests.post(f"{BASE_URL}/tutor/iniciar", json={"tema": tema})
    resp.raise_for_status()
    data = resp.json()
    print(f"\n🤖 UNIprofe: {data['mensaje']}\n")

    historial = [{
        "role": "tutor",
        "content": data["mensaje"],
        "timestamp": datetime.now().isoformat()
    }]
    return data["tema"], historial


def enviar_mensaje(tema: str, mensaje: str, historial: list[dict]) -> str:
    """Envía un mensaje al tutor y actualiza el historial."""
    resp = requests.post(
        f"{BASE_URL}/tutor/mensaje",
        json={
            "tema": tema,
            "mensaje": mensaje,
            "historial": historial,
        },
    )
    resp.raise_for_status()
    data = resp.json()
    respuesta = data["respuesta"]

    print(f"👤 Tú: {mensaje}")
    print(f"🤖 UNIprofe: {respuesta}\n")

    # Actualizar historial
    ahora = datetime.now().isoformat()
    historial.append({"role": "user", "content": mensaje, "timestamp": ahora})
    historial.append({"role": "tutor", "content": respuesta, "timestamp": ahora})
    return respuesta


def conversacion_interactiva() -> None:
    """Conversación interactiva con el tutor en consola."""
    print("=" * 60)
    print("🎓 CHAT CON UNIprofe (Tutor Virtual)")
    print("=" * 60)

    tema = input("\n📚 Escribe el tema sobre el que quieres aprender: ").strip()
    if not tema:
        print("❌ No escribiste ningún tema. Saliendo.")
        return

    try:
        tema, historial = iniciar_tutor(tema)
    except Exception as e:
        print(f"❌ Error al iniciar tutor: {e}")
        return

    print("💬 Escribe tus preguntas. Escribe 'salir' para terminar.\n")

    while True:
        mensaje = input("👤 Tú: ").strip()

        if mensaje.lower() in {"salir", "exit", "quit"}:
            print("\n👋 UNIprofe: Me alegra haberte ayudado, ¡nos vemos en otra ocasión! 😊")
            break

        if not mensaje:
            print("⚠️ No escribiste nada. Si no tienes más dudas, escribe 'salir'.\n")
            continue

        try:
            enviar_mensaje(tema, mensaje, historial)
        except Exception as e:
            print(f"❌ Error al enviar mensaje: {e}")
            break


if __name__ == "__main__":
    conversacion_interactiva()
