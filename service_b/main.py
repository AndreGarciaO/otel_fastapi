from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.observability import tracing  # importante
from app.service_b.routes import router

app = FastAPI()

#Instrumentacion automatica de la app
FastAPIInstrumentor.instrument_app(app)
app.include_router(router)
