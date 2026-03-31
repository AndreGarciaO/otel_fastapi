from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.observability import tracing  # importante
from app.service_a.routes import router

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)
app.include_router(router)
