from openai import OpenAI
import os
import json
import Mongodb
from dotenv import load_dotenv, find_dotenv
import os
import ConsumirServiciosExt
from PosgressJega import update_user_assistant_and_thread,assistant_and_thread_to_null

env_path = find_dotenv()
load_dotenv(env_path)
rutaMesajes="/app/lista_guardada.txt"
#rutaMesajes="lista_guardada.txt"
ThreadOriginal="thread_f3Y6uVVZjnDoyINiCrZbI1L8"

descripcionafinaiciero=""" "This module provides financial information on various  companies , offering analysis of financial data. It is ideal for answering common queries about a company’s financial health, trends,values acounts  and industry comparisons. It is designed to search the database for the information requested by the user or client and attempt to respond to their query using the data extracted from the database.",
"""
def CrearAsistente():
    print("hola")
    prompt="""
You are the web assistant of Eljuri Buissness Intelligence(EBI), an expert in providing accurate and helpful information to the customer. Your goal is to assist the customer by advising them clearly and fluently, in Spanish. Always analyze the conversation history to better understand the customer's needs and provide more accurate responses.
DO NOT request information unless it is REQUIRED as a parameter for a specific function. Only ask for input if it is NECESSARY for executing a function that depends on that information.

**When using the 'IndicadoresFinancieros' function, check the resulting table and analyze the customer's question carefully to select the correct column (valor  or valor acumulado) based on the query. Confirm the selected column type in your response to avoid ambiguity..**

*You will only call the function "Financiero" if all required arguments are provided by the user. Ensure that all necessary arguments for using the function are given. If any arguments are missing, politely prompt the user to supply the missing information and do not execute the function until everything is complete.*
Follow these rules when responding:

1)Always be polite and make sure you clearly understand the purpose of the customer’s question.
2)Respond in a conversational, friendly tone, without explicitly stating that you are providing an answer. Keep the interaction natural and personable.Its important to mention about if the value is 'mensual' o 'acumulado'
3)When responding, always personify yourself as part of EBI and in Spanish
4) Ensure the response is clear,resume  and concise,dont mention irelevant infomration, focuse only in respond the query.
7)***always Use emojis and arrows to separate values from accounts and also instead of line breaks. *** 
8) **When responding, do not mention formulas or explain calculations unless explicitly asked by the user. If the user asks, explain in a simple, understandable format (avoid using LaTeX or complex notation).**


Cuando llames a la funcion "Financiero" asegurate de cumplir los siguientes criterios:.
    1. NO omitas en el Query la palabra "acumulado específicamente si el cliente menciona "acumulado" o  "mensual específicamente si el cliente menciona "mensual" en la consulta.
    2. No omitas ningún detalle como el tipo de indicador, la empresa, el periodo o cualquier otra información relevante.
    3. Asegúrate de que el `Query` contenga **toda** la información de la consulta original.

"Cuando recibas datos de la función 'Financiero', sigue estas instrucciones al pie de la letra:  
1. **IDENTIFICA CLARAMENTE** el tipo de saldo solicitado por el usuario: 'Mensual' o 'Acumulado'. Si el usuario no especifica, **PREGUNTA CLARAMENTE**:  
   '¿Prefieres el saldo mensual o el saldo acumulado?'  
2. **SELECCIONA ÚNICAMENTE** los datos de la columna correspondiente al tipo de saldo solicitado:  
   - Si se solicita 'Mensual', utiliza **exclusivamente** los valores de la columna 'Saldo Mensual'.  
   - Si se solicita 'Acumulado', utiliza **exclusivamente** los valores de la columna 'Saldo Acumulado'.  
4. **VALIDA TU RESPUESTA** antes de enviarla. Confirma que el dato que estás devolviendo **CORRESPONDE** al tipo de saldo solicitado.  
   - Si se detecta un error en los datos o no coinciden con lo solicitado, **NO RESPONDAS** y solicita más información al usuario.  
5. **NO INCLUYAS NINGUNA INFORMACIÓN** irrelevante o no solicitada. Específicamente, **no menciones 'sal_tipo_Estado'** ni columnas no relacionadas con el tipo de saldo.  
6. **NUNCA ASUMAS** que el saldo es 'Acumulado' o 'Mensual' sin confirmación explícita o evidencia directa.  
7. IMPORTANTE: Tu prioridad es proporcionar datos precisos y etiquetarlos correctamente como 'Mensual' o 'Acumulado', según lo que se haya solicitado."


Cuando llames a la funcion "IndicadoresFinancieros" asegurate de cumplir los siguientes criterios:.
    1. NO omitas en el Query la palabra "acumulado específicamente si el cliente menciona "acumulado" en la consulta.
    2. No omitas ningún detalle como el tipo de indicador, la empresa, el periodo o cualquier otra información relevante.
    3. Asegúrate de que el `Query` contenga **toda** la información de la consulta original.
**Avoid redundant information:** Do not repeat details.

    """
    try:
        assistant = client.beta.assistants.create(
        instructions=prompt,
        model="gpt-3.5-turbo",
        temperature=0.5,
        top_p=0.5,
        tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "Financiero",
                        "description":"""Proporciona valores (No porcentajes) de:1. Balance General (ESF): o Activo:  Corriente: Efectivo y equivalentes, cuentas por cobrar CP, inventarios, anticipos a proveedores, pagos anticipados, activos por impuestos corrientes.  No Corriente: Propiedad, planta y equipo, depreciación acumulada, inversiones LP, activos por derecho de uso. o Pasivo:  Corriente: Proveedores, cuentas por pagar, obligaciones financieras CP, provisiones, administración tributaria, anticipos de clientes.  No Corriente: Obligaciones financieras LP, provisiones por beneficios de empleados, pasivos por derecho de uso. o Patrimonio: Capital, reservas, resultados acumulados. 2. Estado de Resultados Integral (ERI): o Ventas Netas: Ventas brutas, descuentos. o Costo de Ventas. o Gastos Operativos: Administración, ventas, publicidad, logística. o Utilidades: Bruta, operativa, neta. o Otros No Operacionales: Gastos e ingresos financieros, otros ingresos y gastos. 3.EBITDA """,
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "Query": {
                                    "type": "string",
                                    "description": "The complete question or inquiry from the customer about financial data, including specific details such as value type, company, period, and any other relevant information and  the current date if it is needed"
                                },
                                "Date":{
                                    "type":"string",
                                    "description":"The current date"
                                }

                            },
                            "required": ["Query","Date"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "IndicadoresFinancieros",
                         "description": "Consulta indicadores financieros clave como Apalancamiento Patrimonio, Capital Neto de Trabajo, % Utilidad Operacional, Rotación de Inventarios, % Gastos de Logística, Liquidez Corriente, % Utilidad Neta, Rotación Cuentas por Pagar, % Gastos Administrativos, Prueba Ácida, % Costo de Venta, % Margen Bruto, % Gastos de Ventas, ROA, Ciclo de Efectivo (días), Periodo Medio de Cobro (días), ROE (DuPont), % Gastos No Operacionales, % EBITDA, % Gastos de Publicidad, Días de Inventario (días), Capital Invertido, % Gastos Operacionales, Deuda/EBITDA, Razón de Endeudamiento, Cobertura de Intereses, Período Medio de Pago (días), % Venta Neta, y Rotación de Cartera.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "Query": {
                                    "type": "string",
                                    "description": "La pregunta o consulta completa sobre los indicadores financieros , incluyendo detalles específicos como el** tipo de indicador, empresa, período ,si es acumulado ** o cualquier otra información relevante."
                                },
                                "Date": {
                                    "type": "string",
                                    "description": "La fecha actual.The current date"
                                }
                            },
                            "required": ["Query", "Date"]
                        }
                    }
                }
            ]
        )
        return assistant
    except Exception as e:
       print("Error al crear el asistente:"+str(e))
       return ("Error al crear el asistente:"+str(e))
def CrearHilo():
    return  client.beta.threads.create()

def CrearMensaje(thread,consulta,fecha):
    fecha= " Current date:"+fecha+'\n'
    message = client.beta.threads.messages.create(
    thread_id=thread,
    role="user",
    content=fecha + consulta,
    )
    return message
def Delete_assitent_OpenAI(assitant):
    response = client.beta.assistants.delete(assitant)
    print(response)
def Delete_thread_OpenAI(thread):
    response = client.beta.threads.delete(thread)
    print(response)

import requests

def consultar_Financiero(query,canal,user_id,id_padre):
    #return "Para la empresa RACING, en febrero 2024, el saldo acumulado de las VENTAS NETAS es de 660821.87, el de las VENTAS BRUTAS es de 661317.46, la UTILIDAD BRUTA es de 144001.9, los GASTOS OPERACIONALES suman 293716.74, y la UTILIDAD NETA es de -330045.08. Estos montos corresponden al 'saldo acumulado (acumulado nacional)' según el 'Tipo Estado 'ERI'"
#def okey(query,canal,user_id):
    print(id_padre)
    url = "http://192.168.10.5:8383/nl2sql"  # URL de tu API
    headers = {"Content-Type": "application/json"}  # Tipo de contenido para el POST
    data = {"query": query,"canal": str(canal),"user_id": str(user_id),"id_padre":int(id_padre)}  # Datos que se enviarán en la solicitud
    try:
    # Hacer una solicitud POST a la API con timeout
        response = requests.post(url, json=data, headers=headers)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(response)
            try:
                print(response.text)  # o response.json() si la respuesta es en formato JSON)
                json_response = response.json()
                print("json:" +str(json_response))

                # Acceder a los valores del JSON
                sql_query = json_response.get('sql_query')
                id_pregunta = json_response.get('id_pregunta')

                return sql_query,str(id_pregunta)  # Devolver los valores obtenidos
            except ValueError:
                return "Error: La respuesta no es un JSON válido"
        else:
            return f"Error: {response.status_code}, {response.text}"

    except requests.exceptions.Timeout:
        return "Error: La solicitud a la API ha excedido el tiempo de espera"

    except requests.exceptions.RequestException as e:
        print(str(e))
        return f"Error de conexión: {e}"
def consultar_Financiero_KPI(query,canal,user_id,id_padre):
    #return "Para la empresa RACING, en febrero 2024, el saldo acumulado de las VENTAS NETAS es de 660821.87, el de las VENTAS BRUTAS es de 661317.46, la UTILIDAD BRUTA es de 144001.9, los GASTOS OPERACIONALES suman 293716.74, y la UTILIDAD NETA es de -330045.08. Estos montos corresponden al 'saldo acumulado (acumulado nacional)' según el 'Tipo Estado 'ERI'"
#def okey(query,canal,user_id):
    print(id_padre)
    url = "http://192.168.10.5:8383//nl2sqlKPI"  # URL de tu API
    headers = {"Content-Type": "application/json"}  # Tipo de contenido para el POST
    data = {"query": query,"canal": str(canal),"user_id": str(user_id),"id_padre":int(id_padre)}  # Datos que se enviarán en la solicitud
    try:
    # Hacer una solicitud POST a la API con timeout
        response = requests.post(url, json=data, headers=headers)
        # Verificar si la solicitud fue exitosa
        if response.status_code == 200:
            print(response)
            try:
                print(response.text)  # o response.json() si la respuesta es en formato JSON)
                json_response = response.json()
                print("json:" +str(json_response))

                # Acceder a los valores del JSON
                sql_query = json_response.get('sql_query')
                id_pregunta = json_response.get('id_pregunta')

                return sql_query,str(id_pregunta)  # Devolver los valores obtenidos
            except ValueError:
                return "Error: La respuesta no es un JSON válido"
        else:
            return f"Error: {response.status_code}, {response.text}"

    except requests.exceptions.Timeout:
        return "Error: La solicitud a la API ha excedido el tiempo de espera"

    except requests.exceptions.RequestException as e:
        print(str(e))
        return f"Error de conexión: {e}"
def crear_asistente_hilo( assistantID,threadID,codigo_cliente):
    if assistantID is None:
        assistant = CrearAsistente()
        assistant_id = assistant.id  # Asigna el ID del asistente creado
    else:
        assistant_id=assistantID
    #print("el asistente es ="+assistant_id)
    # Verificar si threadID no es None
    if threadID is None:
        #thread = CrearHilo()
        try:
            thread=crear_theath_inicial(ThreadOriginal)
        except:
            thread=crear_hilo_desde_archivo()#crear_theath_inicial(ThreadOriginal)
        print(thread.id )
        thread_id = thread.id  # Asigna el ID del hilo creado
        update_user_assistant_and_thread(codigo_cliente,assistant_id,thread_id)
        #Mongodb.agregar_item(codigo_emp,codigo_cliente,thread_id,assistant_id)
    else:
        thread_id=threadID
    return assistant_id,thread_id

###################################################
client = OpenAI()
def mainIAPrincipal(Input,codigo_cliente,modulos,canal,id_padre,fecha,assistantID=None,threadID=None):
    id_pregunta=None
    resp_con_modulo=False
    Financiero=False
    if modulos is not None:
        for modulo in modulos:
            if modulo==1:
                Financiero=True
    #print("el hilo es="+thread_id)
    #Financiero=True
    consulta=Input
    assistant_id,thread_id=crear_asistente_hilo( assistantID,threadID,codigo_cliente)
    try:
        CrearMensaje(thread_id,consulta,fecha)
    except Exception as e:
        error_message = str(e)
        print(error_message)
        Delete_assitent_OpenAI(assistant_id)
        Delete_thread_OpenAI(threadID)
        assistant_and_thread_to_null(codigo_cliente)
        print("se borro el asistente  en open ai hola")
        return "lamento no poderte ayudar tuvimos que reiniciar tu conversacion ,por favor vuelve a realizar tu consulta",id_pregunta,False
   
        # Aquí puedes decidir qué acción tomar, si es necesaria

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
                    print(f"{each.content[0].text.value}")
                    return f"{each.content[0].text.value}",id_pregunta,resp_con_modulo
                    # Si quieres detener el bucle tras encontrar el primer resultado:
                    break  # Sale del bucle después del primer 'assistant'"""
    

        
    else:
        print("El estatus es:")
        print(run.status)
        print(run.last_error)
        messages = client.beta.threads.messages.list(
        thread_id
        )
        #for each in messages:
           # print(each)

    
    # Define the list to store tool outputs
    tool_outputs = []
    # Loop through each tool in the required action section
    if run.required_action and run.required_action.submit_tool_outputs:
        for tool in run.required_action.submit_tool_outputs.tool_calls:
            print(tool.function.name)
            #print(tool.function.arguments)#asi puedo obtener los argumentos
            if tool.function.name == "Financiero":
                if Financiero==True:
                    print("entro a finacieroAI")
                    resp_con_modulo=True
                    data=tool.function.arguments
                    # Convertir el string a un diccionario usando json.loads()
                    data_dict = json.loads(data)
                    # Acceder al valor de la clave 'Query'
                    query_text = data_dict['Query']
                    print(data_dict['Date'])
                    #print(data_dict['value_type'])
                    #print(query_text)
                    if query_text =="":
                        tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": "Para poderte ayudar y obtener tu informacion  por favor clarifica mejor tu consulta. "
                        })
                    else:
                        respuesta,id_pregunta=consultar_Financiero(query_text,canal,codigo_cliente,id_padre)
                        id_pregunta=str(id_pregunta)
                        print("ID respuesta en funcion:"+id_pregunta)
                        #data = json.loads(respuesta)
                        # Obtener el valor del campo 'response'
                        #if isinstance(respuesta, dict):
                            #response_text = respuesta['response']
                            #print(response_text)
                        #else:
                        response_text = respuesta
                        print(response_text)
                        tool_outputs.append({
                            "tool_call_id": tool.id,
                            "output": response_text
                            })
                       
                else:
                    response_text = " informa que No le puedes brindar  esta información porque esta restigida para su usuario. "
                    tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": response_text
                        })
            if tool.function.name == "IndicadoresFinancieros":
                if Financiero==True:
                    print("entro a finacieroKPIAI")
                    resp_con_modulo=True
                    data=tool.function.arguments
                    # Convertir el string a un diccionario usando json.loads()
                    data_dict = json.loads(data)
                    # Acceder al valor de la clave 'Query'
                    query_text = data_dict['Query']
                    print(data_dict['Date'])
                    #print(data_dict['value_type'])
                    #print(query_text)
                    if query_text =="":
                        tool_outputs.append({
                        "tool_call_id": tool.id,
                        "output": "Para poderte ayudar y obtener tu informacion  por favor clarifica mejor tu consulta. "
                        })
                    else:
                        respuesta,id_pregunta=consultar_Financiero_KPI(query_text,canal,codigo_cliente,id_padre)
                        id_pregunta=str(id_pregunta)
                        print("ID respuesta en funcion:"+id_pregunta)
                        #data = json.loads(respuesta)
                        # Obtener el valor del campo 'response'
                        #if isinstance(respuesta, dict):
                            #response_text = respuesta['response']
                            #print(response_text)
                        #else:
                        response_text = respuesta
                        print(response_text)
                        tool_outputs.append({
                            "tool_call_id": tool.id,
                            "output": response_text
                            })
                        
                else:
                    response_text = " informa que No le puedes brindar  esta información porque esta restigida para su usuario. "
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
                print(f"{each.content[0].text.value}")
                return f"{each.content[0].text.value}",id_pregunta,resp_con_modulo
                # Si quieres detener el bucle tras encontrar el primer resultado:
                break  # Sale del bucle después del primer 'assistant'"""
    else:
        print("El estatus es:")
        print(run.status)
        print(run.last_error)

#(mainIAPrincipal("cual es el valor de ventas netas para enero 2024  de ktm ","1","1","1"))
#Delete_assitent_OpenAI("asst_KVbca3zzHI8vJfGhV2q7S3V5")
def borrar2():
    for i in range(101):
        try:
            my_assistants = client.beta.assistants.list(
                order="desc",
                limit="10",
            )
            response=my_assistants.data
            #ids = [item['id'] for item in response]
            for a in response:
                Delete_assitent_OpenAI(a.id)
        except:
            break
def crear_theath_inicial(threadI):
    current_thread_messages = client.beta.threads.messages.list(threadI, limit=80)
    current_messages = []

    for message in current_thread_messages.data:
        current_messages.append(
            {
                "role": message.role,
                "content": message.content[0].text.value
            }
        )

    current_messages.reverse()
    print(len(current_messages))
    InicialMessages=current_messages[0:32]
    print("filas"+str(len(InicialMessages)))
    #print(InicialMessages)
    print(current_messages[32])
    duplicate_thread = client.beta.threads.create(messages=InicialMessages)
    for a in range(32,len(current_messages)):
        b=current_messages[a]
        # Obtener el valor de 'role'
        rol = b['role']
        contenido = b['content']
        message = client.beta.threads.messages.create(
            thread_id=duplicate_thread.id,
            role=rol,
            content=contenido
        )
    return duplicate_thread
# Escribir la lista en un archivo manteniendo su formato
def ExtraerChat_txt(threadI):
    current_thread_messages = client.beta.threads.messages.list(threadI, limit=80)
    current_messages = []

    for message in current_thread_messages.data:
        current_messages.append(
            {
                "role": message.role,
                "content": message.content[0].text.value
            }
        )

    current_messages.reverse()
    with open("lista_guardada1.txt", "w", encoding="utf-8") as archivo:
        archivo.write(str(current_messages))

def crear_hilo_desde_archivo():
    ruta_archivo=rutaMesajes
    # Inicializar la lista de mensajes
    InicialMessages = []

    # Leer el archivo de texto
    with open(ruta_archivo, 'r') as archivo:
        contenido = archivo.read()

        # Reemplazar las comillas simples por comillas dobles
        contenido = contenido.replace("'", '"')

        # Convertir el contenido modificado en una lista de diccionarios
        try:
            mensajes = json.loads(contenido)
        except json.JSONDecodeError as e:
            print(f"Error al leer el archivo JSON: {e}")
            print(f"Descripción del error: {e.msg}")
            print(f"Posición del error: Línea {e.lineno}, Columna {e.colno}")
    
            print("Error: el archivo no tiene el formato JSON adecuado.")
            return

    # Convertir cada mensaje y agregarlo a la lista InicialMessages
    for mensaje in mensajes:
        InicialMessages.append({
            "role": mensaje["role"],
            "content": mensaje["content"].strip()
        })
    current_messages=InicialMessages
    InicialMessages=current_messages[0:32]
    print("filas"+str(len(InicialMessages)))
    #print(InicialMessages)
    print(current_messages[32])
    duplicate_thread = client.beta.threads.create(messages=InicialMessages)
    for a in range(32,len(current_messages)):
        b=current_messages[a]
        # Obtener el valor de 'role'
        rol = b['role']
        contenido = b['content']
        message = client.beta.threads.messages.create(
            thread_id=duplicate_thread.id,
            role=rol,
            content=contenido
        )
    return duplicate_thread
    # Crear el hilo usando el cliente de la API
    duplicate_thread = client.beta.threads.create(messages=InicialMessages)
    
    return duplicate_thread
#crear_theath_inicial("thread_dFFLRYOl8lYHhXht7G0rBFMa")
#############################################################33
# el hilo original es thread_f3Y6uVVZjnDoyINiCrZbI1L8
##############################################
#crear_theath_inicial("thread_f3Y6uVVZjnDoyINiCrZbI1L8")
#ExtraerChat_txt("thread_MMfEceq5N2u3s3CWpjYH8XVK")
#crear_hilo_desde_archivo()