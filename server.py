# api_inferencia.py
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import tensorflow as tf
import io

# Cargar el modelo entrenado
modelo = tf.keras.models.load_model("modelo_base.h5")

app = FastAPI()

@app.post("/predecir/")
async def predecir_digito(file: UploadFile = File(...)):
    try:
        # Leer y procesar la imagen
        contenido = await file.read()
        imagen = Image.open(io.BytesIO(contenido)).convert('L')  # Escala de grises

        imagen = imagen.resize((28, 28))  # Tamaño esperado por el modelo
        imagen_array = np.array(imagen).astype('float32') / 255.0
        imagen_array = imagen_array.reshape(1, 28, 28, 1)

        # Realizar predicción
        prediccion = modelo.predict(imagen_array)
        digito = int(np.argmax(prediccion))
        confianza = float(np.max(prediccion))

        return JSONResponse(content={"digito": digito, "confianza": confianza})
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
