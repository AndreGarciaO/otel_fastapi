import os
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

#Metadata del servicio
resource = Resource.create({
    "service.name": os.getenv("OTEL_SERVICE_NAME", "demo-service"),
    "service.version": "1.0.0",
    "deployment.environment": "demo"
})


#Creador de spans y traces
provider = TracerProvider(resource=resource)
trace.set_tracer_provider(provider)

#Definicion del export de spans,en esta caso usando HTTP diracto a Dynatrace
otlp_exporter = OTLPSpanExporter()

#Optimizacion de exportacion
span_processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(span_processor)
