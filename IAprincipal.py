from openai import OpenAI
from dotenv import load_dotenv
import os
import json
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
from openai import OpenAI
def CrearAsistente():
    assistant = client.beta.assistants.create(
    instructions="""
You are the web assistant for Seguros Unidos, an expert in providing accurate and helpful information to the customer. Your goal is to assist the customer by advising them clearly and fluently, in Spanish. Always analyze the conversation history to better understand the customer's needs and provide more accurate responses.
DO NOT request information unless it is REQUIRED as a parameter for a specific function. Only ask for input if it is NECESSARY for executing a function that depends on that information.

You will only call the function "Obtener_informacion" if all required arguments are provided by the user. Ensure that all necessary arguments for using the function are given. If any arguments are missing, politely prompt the user to supply the missing information and do not execute the function until everything is complete.
Follow these rules when responding:

1)Always be polite and make sure you clearly understand the purpose of the customer’s question.
2)Respond in a conversational, friendly tone, without explicitly stating that you are providing an answer. Keep the interaction natural and personable.
3)Do not share any knowledge that is not relevant to the conversation. If you don't have the required information, say, "At this moment, I don't have an answer. Can I help you with something else?"
4)When responding, always personify yourself as part of Seguros Unidos.


    """,
    model="gpt-3.5-turbo",
    tools = [
            {
                "type": "function",
                "function": {
                    "name": "Obtener_informacion",
                    "description": " This function provides information on any topic related to insurance, but it is limited to general information that could typically be found on the company's websiteof Seguros UNidos. It is ideal for answering common queries regarding products, services, or claims, but not for personalized or detailed requests.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Query": {
                                "type": "string",
                                "description": "The question or inquiry made by the customer."
                            }
                        },
                        "required": ["Query"]
                    }
                }
            }
        ]
    )
    return assistant
def CrearHilo():
    return  client.beta.threads.create()

def CrearMensaje(thread,consulta):
    message = client.beta.threads.messages.create(
    thread_id=thread,
    role="user",
    content=consulta,
    )
    return message
import requests

def consultar_api(query):
    url = "http://localhost:8000/consultar"  # URL de tu API
    headers = {"Content-Type": "application/json"}  # Tipo de contenido para el POST
    data = {"query": query}  # Datos que se enviarán en la solicitud

    try:
        # Hacer una solicitud POST a la API
        response = requests.post(url, json=data, headers=headers)

        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            return response.json()  # Devolver la respuesta en formato JSON
        else:
            return f"Error: {response.status_code}, {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error de conexión: {e}"

###################################################
client = OpenAI()
def IAprincipal(Input,assistantID=None,threadID=None):
    if assistantID is None:
        assistant = CrearAsistente()
        assistant_id = assistant.id  # Asigna el ID del asistente creado
    else:
        assistant_id=assistantID
    # Verificar si threadID no es None
    if threadID is None:
        thread = CrearHilo()
        thread_id = thread.id  # Asigna el ID del hilo creado
    else:
        thread_id=threadID
    consulta=Input
    CrearMensaje(thread_id,consulta)

    run = client.beta.threads.runs.create_and_poll(
    thread_id=thread_id,
    assistant_id=assistant_id,
    )
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
        thread_id
        )
        #print(thread_id)
        #print(assistant_id)
            
        for each in messages:
            #print(each.role+":"+each.content[0].text.value)
            for each in messages:
                if each.role == "assistant":
                    # Devuelve o imprime el primer mensaje cuyo role es 'assistant'
                    return f"{each.content[0].text.value}"
                    # Si quieres detener el bucle tras encontrar el primer resultado:
                    break  # Sale del bucle después del primer 'assistant'"""
    

        
    else:
        print(run.status)
        messages = client.beta.threads.messages.list(
        thread_id
        )
        for each in messages:
            print(each)

    
    # Define the list to store tool outputs
    tool_outputs = []
    # Loop through each tool in the required action section
    if run.required_action and run.required_action.submit_tool_outputs:
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            #print(tool.function.arguments)#asi puedo obtener los argumentos
            if tool.function.name == "Obtener_informacion":
                data=tool.function.arguments
                # Convertir el string a un diccionario usando json.loads()
                data_dict = json.loads(data)
                # Acceder al valor de la clave 'Query'
                query_text = data_dict['Query']
                #print(query_text)
                if query_text =="":
                    tool_outputs.append({
                    "tool_call_id": tool.id,
                    "output": "Para poderte y obtener tu informacion  por favor clarifica mejor tu consulta. "
                    })
                else:
                    respuesta=consultar_api(query_text)
                    #data = json.loads(respuesta)
                    # Obtener el valor del campo 'response'
                    if isinstance(respuesta, dict):
                        response_text = respuesta['response']
                        #print(response_text)
                    else:
                        response_text = respuesta
                    tool_outputs.append({
                "tool_call_id": tool.id,
                "output": response_text
                })
            
    
    # Submit all tool outputs at once after collecting them in a list
    if tool_outputs:
        try:
            run = client.beta.threads.runs.submit_tool_outputs_and_poll(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
            )
            #print("Tool outputs submitted successfully.")
        except Exception as e:
            print("Failed to submit tool outputs:", e)
    else:
        print("No tool outputs to submit.")
    
    if run.status == 'completed':
        messages = client.beta.threads.messages.list(
            thread_id
        )
        #for each in messages:
            #print(messages)
           # print(each.role+":"+each.content[0].text.value)
        #print(thread_id)
        #print(assistant_id)    
        for each in messages:
            if each.role == "assistant":
                # Devuelve o imprime el primer mensaje cuyo role es 'assistant'
                return f"{each.content[0].text.value}"
                # Si quieres detener el bucle tras encontrar el primer resultado:
                break  # Sale del bucle después del primer 'assistant'"""
    else:
        print(run.status)
def mainIAPrincipal(Input,asistente=None,hilo=None):
    if hilo  is None  and asistente is None:
        return(IAprincipal(Input))
    else:
        return(IAprincipal(Input,asistente,hilo))
