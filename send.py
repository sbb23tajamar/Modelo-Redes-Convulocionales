# send.py
import requests
import argparse

def enviar_imagen(ruta_imagen, url="http://localhost:8000/predecir/"):
    try:
        with open(ruta_imagen, "rb") as img_file:
            archivos = {"file": img_file}
            respuesta = requests.post(url, files=archivos)

        if respuesta.status_code == 200:
            resultado = respuesta.json()
            print(f"✅ Dígito Predicho: {resultado['digito']} (Confianza: {resultado['confianza']:.2f})")
        else:
            print(f"❌ Error: {respuesta.status_code} - {respuesta.text}")
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {ruta_imagen}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cliente para enviar imágenes a la API de predicción de dígitos")
    parser.add_argument("--imagen", type=str, required=True, help="Ruta de la imagen a enviar")
    args = parser.parse_args()

    enviar_imagen(args.imagen)
