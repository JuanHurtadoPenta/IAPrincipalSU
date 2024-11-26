from PosgressJega  import obtener_preguntas,obtener_respuestas
def formatear_fechas(respuestas):
    """Transforma las fechas en el formato día-mes-año y hora en la lista de respuestas."""
    for respuesta in respuestas:
        # Formatea pre_fecha_pregunta
        respuesta["pre_fecha_pregunta"] = respuesta["pre_fecha_pregunta"].strftime("%d-%m-%Y %H:%M")
        
        # Formatea res_fecha_respuesta
        respuesta["res_fecha_respuesta"] = respuesta["res_fecha_respuesta"].strftime("%d-%m-%Y %H:%M")
    
    return respuestas

# Llamada a la función para formatear las fechas
import json
from datetime import datetime

def formatear_para_json(respuestas):
    """Genera una lista de preguntas y respuestas en formato JSON para Power Automate."""
    datos = []
    
    for respuesta in respuestas:
        entrada = {
            "pre_id": respuesta["pre_id"],
            "pre_pregunta": respuesta["pre_pregunta"],
            "pre_fecha_pregunta": respuesta["pre_fecha_pregunta"].strftime("%d-%m-%Y %H:%M"),
            "res_respuesta": respuesta["res_respuesta"],
            "res_fecha_respuesta": respuesta["res_fecha_respuesta"].strftime("%d-%m-%Y %H:%M"),
            "res_id": respuesta["res_id"]
        }
        datos.append(entrada)
    
    # Convertir a JSON para enviar a Power Automate
    return json.dumps(datos)
pre_id_usuario = 1  # Cambia este valor según sea necesario
def Obtener_historial(pre_id_usuario):
    preguntas = obtener_preguntas(pre_id_usuario)
    respuestas = obtener_respuestas(preguntas)
    historial = []
    for respuesta in respuestas:
        # Formatear fechas
        pre_fecha = respuesta["pre_fecha_pregunta"].strftime("%d-%m-%Y %H:%M")
        res_fecha = respuesta["res_fecha_respuesta"].strftime("%d-%m-%Y %H:%M")
        
        # Formato para cada interacción
        entrada_chat = (
            f"Pregunta ({pre_fecha}): {respuesta['pre_pregunta']}\n"
            f"Respuesta ({res_fecha}): {respuesta['res_respuesta']}\n"
        )
        
        historial.append(entrada_chat)
    historial=formatear_para_json(respuestas)
    return historial

