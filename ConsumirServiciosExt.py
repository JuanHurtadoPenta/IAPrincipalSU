import requests
def EnviarRespuestaWhats(respuesta,codigo_cliente):
    # URL del endpoint (asegúrate de cambiarlo si es diferente)
    url = "https://private-anon-006ae1d487-chatbotcoreapi1.apiary-mock.com/chatbot/core/process/message"
    # Datos que vas a enviar en el cuerpo de la solicitud POST
    payload = {
        "client_code": codigo_cliente,
        "ref_data": {
            "ref_text": respuesta
        }
    }
    # Encabezados de la solicitud
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJCT1QgSUEiLCJ1c2VySWQiOiI1IiwiZXhwIjoxNzg5MzE4ODI5LCJpc3MiOiJmcm9udGVuZC1kb21haW4uY29tIiwiYXVkIjoiYmFja2VuZC1kb21haW4uY29tIn0.Fip4-3bIR0pUSgPxPOnZ7rIf8TrNXgW6ue_ykZ3FLzQ"
    }

    # Realizar la solicitud POST
    response = requests.post(url, json=payload, headers=headers)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
            print("La respuesta se ha enviado al whatsapp del contacto.")
            print(response.text)
    else:
         print("NO se pudo enviar la respuesta al whatsapp del contacto.")