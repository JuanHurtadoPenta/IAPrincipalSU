from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from IAprincipal import mainIAPrincipal
import ConsumirServiciosExt
from teams import Obtener_historial
from PosgressJega import assistant_and_thread_to_null,get_user_id_by_channel,get_modulos_ids_by_user_id,get_user_assistant_and_thread,agregar_rank,add_question,add_response_id
app = FastAPI()

class Query(BaseModel):
    query: str
    value: str# correo o telefono
    canal: str
class rank(BaseModel):
    rank: str
    res_id: int

class historial(BaseModel):
    value: str# correo o telefono
    canal: str
@app.post("/agrank")
def agregar_rank_endpoint(rank_request: rank):
    try:
        id_pregunta = rank_request.res_id
        valor = str(rank_request.rank).lower()  # Convertir a minúsculas para evitar problemas con mayúsculas
        booleano = valor == "true" 
        agregar_rank(id_pregunta,booleano)  # Llama a la función para agregar el rank
        return JSONResponse(status_code=200, content={"message": "Rank agregado con éxito"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.post("/historial")
def historial_endpoint(historial: historial):
    try:
        canal=int(historial.canal)
        print(canal)
        codigo_cliente=get_user_id_by_channel(canal, historial.value)
        usuario_id= codigo_cliente
        historial= Obtener_historial(usuario_id)
        return JSONResponse(status_code=200, content={"message": historial})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
@app.post("/consultar")
def consultar(query: Query):
    try:
        canal=int(query.canal)
        print(canal)
        codigo_cliente=get_user_id_by_channel(canal, query.value)
        print(codigo_cliente)
        if codigo_cliente is not None:
            modulos=get_modulos_ids_by_user_id(codigo_cliente)
            assitente,hilo=get_user_assistant_and_thread(codigo_cliente)
            #print(modulos)
            print(assitente)
            print(hilo)
            # Realiza las acciones que necesitas con la consulta
            pregunta_id =add_question(canal, codigo_cliente, query.query)
            from datetime import datetime
            # Obtener la fecha actual
            fecha_actual = datetime.now()
            fecha_actual=str(fecha_actual.day)+"-"+str(fecha_actual.month)+"-"+str(fecha_actual.year)
            response,id_respuesta,resp_con_modulo = mainIAPrincipal(query.query,codigo_cliente,modulos,canal,pregunta_id,fecha_actual,assitente,hilo)
            if resp_con_modulo==True:
                add_response_id(response, pregunta_id, 2)# 3 se refierea respuesta final dle modulo
                print("ID respuesta en MAIN:"+id_respuesta)
            #ConsumirServiciosExt.EnviarRespuestaWhats(response, query.codigo_cliente)
            # Devuelve un código de estado 200 sin respuesta específica
                return JSONResponse(status_code=200, content={"message":response,"id":str(id_respuesta)})
            else:
                 print("No uso ningun modulo para responder")
                 id_respuesta=add_response_id( response, pregunta_id, 2)#2 es el modulo sin modulo
            #ConsumirServiciosExt.EnviarRespuestaWhats(response, query.codigo_cliente)
            # Devuelve un código de estado 200 sin respuesta específica
                 return JSONResponse(status_code=200, content={"message":response,"id":str(id_respuesta)})
        else:
            return JSONResponse(status_code=400, content={"detail":"Usuario no registrado"})

    except Exception as e:
        error_message = str(e)
        
        # Verificar si el error contiene el código y mensaje que indicaste
        if "404" in error_message and "No assistant found with id" in error_message:
            print("ERROR: Assistant no encontrado")
            
            assistant_and_thread_to_null(codigo_cliente)
            
            # Lanzar una excepción HTTP con un mensaje adecuado
            raise HTTPException(status_code=400, detail="No tuvimos acceso a tu historial del chat, intentalo nuevamente")
        
        # Para otros tipos de errores
        print("ERROR: " + error_message)
        raise HTTPException(status_code=400, detail="Ocurrió un error inesperado, intentalo nuevamente más tarde")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9292)
