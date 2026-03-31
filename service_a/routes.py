import requests
from fastapi import APIRouter
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry import trace

router = APIRouter()
RequestsInstrumentor().instrument()

tracer = trace.get_tracer(__name__)

@router.get("/start")
def start():
    with tracer.start_as_current_span("custom-business-logic") as span:
        span.set_attribute("demo.attribute", "valor-personalizado")

        response = requests.get("http://localhost:8001/work")

        return {
            "fromA": "Respuesta desde Service A",
            "fromB": response.json()
        }
