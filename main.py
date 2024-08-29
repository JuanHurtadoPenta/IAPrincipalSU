from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from IAprincipal import mainIAPrincipal

app = FastAPI()

class Query(BaseModel):
    query: str
    asistente: str
    hilo: str

@app.post("/consultar")
def consultar(query: Query):
    try:
        response = mainIAPrincipal(query.query)
        return  response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
