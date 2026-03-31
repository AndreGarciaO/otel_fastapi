# otel_fastapi

## Prerrequisitos

* Ambiente de Dynatrace 
* Endpoint de Otel Ej. /api/v2/otlp
* Api Token con permisos de Ingest OpenTelemetry Traces, Ingest logs e Ingest Metrics

## Instrucciones

1.- Crear un ambiente virtual

    ```
	python3 -m venv venv
    ```

2.- Descarga el repositorio

3.- Instala las dependencias con el siguiente comando:

	  ```
    pip install -r requirements.txt
    ```

4.- Exporta las variables del tenant y su token

```
	export DT_ENDPOINT=
	export DT_API_TOKEN=
```

5.- Levanta tu collector:
```
	docker run -d \
  --name otel-collector \
  -p 4317:4317 \
  -p 4318:4318 \
  -v $(pwd)/otel-collector-config.yaml:/etc/otelcol/config.yaml \
  -e DT_API_TOKEN=$DT_API_TOKEN \
  -e DT_ENDPOINT=$DT_ENDPOINT \
  dynatrace/dynatrace-otel-collector:latest

```

6.- En una consola exporta las variables del nombre del servicio y el endpoint del colector
```
	export OTEL_SERVICE_NAME=service-b
	export OTEL_EXPORTER_ENDPOINT=http://localhost:4318
```
7.- Inicializa el servicio
```
        uvicorn app.service_b.main:app --port 8001
```
8.- Abre otra terminal y haz lo mismo pero cambia el nombre del servicio
```
	export OTEL_SERVICE_NAME=service-a
    export OTEL_EXPORTER_ENDPOINT=http://localhost:4318
	uvicorn app.service_a.main:app --port 8000
```

9.- Corrige el error del collector:

10.- Reinicia el collector:
	docker rm -f otel-collector

11.- Inicia de nuevo

12.- Debes tener dos terminales, una con servicio a corriendo otra con servicio b y en una tercera haz pruebas lanzando un curl
```
	curl http://localhost:8000/start

```
13.- Verifica en tu ambiente de Dynatrace que la telemetria llego
