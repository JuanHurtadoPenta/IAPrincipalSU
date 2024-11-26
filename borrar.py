import re
from openai import OpenAI
from openai import  BadRequestError
import os
import json
def extract_json(text):
    # Buscar y eliminar todo lo que está antes de "SQLQuery:", incluyendo la propia frase
    indice = text.find("SQLQuery:")
    
    if indice != -1:
        # Cortar el texto para eliminar lo anterior a "SQLQuery:"
        text = text[indice + len("SQLQuery:"):]
    
    # Verificar si existe la marca ```json en el texto
    if '```json' in text:
        # Usar expresiones regulares para encontrar texto entre ```json y ```
        match = re.search(r'```json\n(.*?)\n```', text, re.DOTALL)
        if match:
            return match.group(1).strip()  # Devolver el contenido sin espacios adicionales
    
    # Si no se encuentra JSON, retornar el texto limpio después de SQLQuery
    return text
os.environ["OPENAI_API_KEY"] = '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'
# Consulta SQL y la consulta del cliente

human_query = "período medio de cobros (días) de la empresa Racing en el año 2023 "

tabla="""
Mes | valor | valor Acumulado
------------------------------
1          | 182.08     | 22.36
------------------------------
2          | 170.48     | 22.03
------------------------------
3          | 174.45     | 21.82
------------------------------
4          | 161.33     | 21.79
------------------------------
5          | 161.62     | 21.84
------------------------------
6          | 159.04     | 22.0
------------------------------
7          | 165.38     | 22.26
------------------------------
8          | 160.95     | 22.8
------------------------------
9          | 153.77     | 23.59
------------------------------
10         | 158.4      | 24.56
------------------------------
11         | 163.49     | 25.54
------------------------------
12         | 164.67     | 22.78
------------------------------"""
def devolver_Analisis(human_query,tabla):
    print(human_query)
    #*Do not mention the SQL query  in your response
    prompt2 = f"""
El cliente ha enviado el siguiente mensaje:
"{human_query}"

A continuación se encuentra una tabla con la información correspondiente. Responde solo con los datos de las columnas correspondientes según la consulta del cliente:

<<BEGIN CONTEXT>>
{tabla}
<<END CONTEXT>>

*** Instrucciones: ***:
1. Si el cliente busca el valor  "acumulado" o "acumulada" en su consulta, **omite** los valores de la columna "valor" y responde con la misma tabla modificada.
2. Si el cliente **no menciona** la palabra "acumulado" o"acumulada" o no busca explicitamente ese valor , **omite** los valores de la columna "valor_acumulado"  y responde con la misma tabla modificada.
3. **No realices cálculos**. Simplemente muestra la información de la tabla según lo solicitado por el cliente.
4. Asegúrate de que la respuesta sea clara y directamente relacionada con la consulta del cliente, sin comentarios adicionales.

Responde solo con los valores de las columnas pertinentes, sin texto adicional.
"""

  
    prompt3="""Your response MUST tu be in SPANISH  .Ensures that your respond be in a one string. For example:  
    ```json
    {
        "query_response": "TU RESPUESTA....."
    }
    """

    promptsystem=f"""Tu objetivo principal es tomar los datos obtenidos de una consulta de tu base de datos y analizarlos para responder la consulta del cliente.
 Usa  la tabla  en fomrato string dada en el contexto  para responder  de acuerdo a la consulta específica del cliente.
    
"""
    
    messages=[
                {"role": "system", "content":promptsystem},
                {"role": "user", "content": prompt2+prompt3}#promptRespuestaFinal}#prompt2}
            ]
    print(messages)
    #messages=VariosMensajes(result,messages)
    try:
        client = OpenAI(
            # This is the default and can be omitted
            #api_key='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'
            api_key=os.environ.get("OPENAI_API_KEY"),
        )
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.2,
        )
        respuesta=chat_completion
        descripcion = respuesta.choices[0].message.content
        #print(descripcion)
        descripcion=extract_json(descripcion)
        #print(descripcion)
        response_json = json.loads(descripcion)
       # print("las condiciones son:"+str(response_json["Condiciones"]))
        Queryresponse= response_json["query_response"]
        #informe= response_json["informe"]
        respuestaT=Queryresponse#+"\n"+informe
        #print(Queryresponse)
    except  BadRequestError as e:
        if "maximum context length" in str(e):
            #Queryresponse=devolver_AnalisisLargo(result,human_query,SQL_query)
            respuestaT="La información que desea consultar es muy extensa como para mostrártela por este medio. Por favor, delimite mejor su consulta."
        else:
            raise  # Puedes seguir manejando otros errores aquí si es necesario
    return respuestaT
def procesar_tabla(pregunta, tabla):
    # Separar las líneas de la tabla
    filas = tabla.strip().split("\n")
    
    # Extraer los encabezados y las filas de datos
    encabezados = filas[0].split("|")
    encabezados = [encabezado.strip() for encabezado in encabezados]  # Limpiar espacios
    
    # Determinar la columna a eliminar
    if "acumulado" in pregunta.lower() or "acumulada" in pregunta.lower():
        columna_a_eliminar = "valor"
    else:
        columna_a_eliminar = "valor Acumulado"
    
    # Verificar que la columna a eliminar exista
    try:
        posicion_columna = encabezados.index(columna_a_eliminar)
    except ValueError:
        raise ValueError(f"La columna '{columna_a_eliminar}' no se encontró en los encabezados de la tabla.")
    
    # Reconstruir la tabla eliminando la columna en esa posición
    nueva_tabla = []
    for fila in filas:
        valores = fila.split("|")
        valores = [valor.strip() for valor in valores]  # Limpiar espacios
        # Eliminar la columna correspondiente
        nueva_fila = [valores[i] for i in range(len(valores)) if i != posicion_columna]
        nueva_tabla.append(" | ".join(nueva_fila))
    
    # Unir las filas modificadas para formar la tabla actualizada
    return "\n".join(nueva_tabla)


# Ejemplo de uso
pregunta_1 = "¿Cuál es el valor acumulado del mes de enero?"
pregunta_2 = "¿Cuál es el valor del mes de enero?"

tabla = """Mes | valor | valor Acumulado
1 | 22.36 | 44.39
2 | 22.03 | 66.42
3 | 21.82 | 88.24
4 | 21.79 | 110.03
5 | 21.84 | 131.87
6 | 22.0 | 153.87
7 | 22.26 | 176.13
8 | 22.8 | 198.93
9 | 23.59 | 222.52
10 | 24.56 | 247.08
11 | 25.54 | 272.62
12 | 22.78 | 295.4"""

nueva_tabla_1 = procesar_tabla(pregunta_1, tabla)
nueva_tabla_2 = procesar_tabla(pregunta_2, tabla)

#print("Tabla eliminando 'valor Acumulado':")
#print(nueva_tabla_1)
#print("\nTabla eliminando 'valor':")
#print(nueva_tabla_2)


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
    client = OpenAI()
    try:
        assistant = client.beta.assistants.create(
        instructions=prompt,
        model="gpt-3.5-turbo",
       temperature=0.2,
        tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "Financiero",
                        "description": "This module provides financial information on various  companies , offering analysis of financial data. It is ideal for answering common queries about a company’s financial health, trends,values acounts  and industry comparisons. It is designed to search the database for the information requested by the user or client and attempt to respond to their query using the data extracted from the database.",
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

CrearAsistente()