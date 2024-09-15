from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from IAprincipal import mainIAPrincipal
import ConsumirServicios

app = FastAPI()

class Query(BaseModel):
    query: str
    codigo_bod: str
    codigo_cliente: str


@app.post("/consultar")
def consultar(query: Query):
    try:
        # Realiza las acciones que necesitas con la consulta
        response = mainIAPrincipal(query.query, query.codigo_bod, query.codigo_cliente)
        ConsumirServicios.EnviarRespuestaWhats(response, query.codigo_cliente)
        
        # Devuelve un código de estado 200 sin respuesta específica
        return JSONResponse(status_code=200, content={"message": "Operación exitosa"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
