import time
from fastapi import APIRouter

router = APIRouter()

#Otel crea automaticamente span name y span kind
@router.get("/work")
def work():
    time.sleep(0.3)
    return {"message": "Trabajo hecho en Service B"}
