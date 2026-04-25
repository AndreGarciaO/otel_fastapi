# otel_fastapi

## Prerrequisitos:

* Ambiente de Dynatrace.
* URL de tu ambiente de Dynatrace, considerando el endpoint de Otel (/api/v2/otlp).
* Api Token con permisos de Ingest OpenTelemetry Traces, Ingest logs e Ingest Metrics.

#### Recomendacion de OS y herramientas
* Las instrucciones estan basadas en un sistema operativo basado en linux, asi como tambien contemplan el uso de docker y git.
* La aplicacion esta hecha en python por lo que tambien se recomienda la instalación de python antes de iniciar.

## Instrucciones

1.- Abre una terminal y crea una carpeta dentro de la localidad de tu preferencia. 
```
mkdir ejercicio_otel_python
```
Ya creada entra a esta para trabajar los siguientes pasos en un mismo folder.

2.- Dentro de la carpeta creada en el paso anterior crea un entorno virtual de python.
```
python3 -m venv venv
```
> 2.1.- Si no tienes el paquete venv instalado, puedes instalarlo con el siguiente comando:
	```
	sudo apt-get install python3-virtualenv
	```
> 

3.- Activa tu venv con el siguiente comando:
```
source venv/bin/activate
```

4.- Descarga el repositorio.
```
git clone https://github.com/AndreGarciaO/otel_fastapi.git
```

5.- Accede a la carpeta del repositorio clonado e instala las dependencias del proyecto con el siguiente comando:
```
pip install -r requirements.txt
```

6.- Define la url de tu tenant y tu token como variables de entorno dentro de tu terminal.

```
	export DT_ENDPOINT=<Your-env-url>/api/v2/otlp
	export DT_API_TOKEN=<Your-env-token>
```

7.- Levanta el collector de Dynatrace como un contenedor:
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
> El comando de docker run se debe ejecutar estando dentro de la carpeta del repositorio descargado, ya que este comando depende de la existencia del archivo de configuracion del collector
>

7.- Valida que tu collector esta corriendo de manera exitosa con el siguiente comando:
```
	docker ps
```

8.- Abre una terminal nueva y en esta exporta las variables del nombre del servicio b y la del endpoint del exporter de otel.
```
	export OTEL_SERVICE_NAME=service-b
	export OTEL_EXPORTER_ENDPOINT=http://localhost:4318
```
>El endpoint del exporter es localhost ya que nuestro colector este desplegado dentro de la misma maquina como contenedor.
>
9.- Inicializa el servicio b
```
        uvicorn app.service_b.main:app --port 8001
```
10.- Abre otra terminal y exporta las variables del nombre del servicio a y la del endpoint del exporter de otel.
```
	export OTEL_SERVICE_NAME=service-a
    export OTEL_EXPORTER_ENDPOINT=http://localhost:4318
```

10.- Inicializa el servicio a
```
        uvicorn app.service_a.main:app --port 8000
```
11.- En este punto debes tener abiertas tres terminales:
* Terminal 1 - Donde se desplego el collector.
* Terminal 2 - Donde se inicializo servicio b.
* Terminal 3 - Donde se inicializo servicio a.

12.- En terminal 1 ejecuta el llamado al servicio a utilizando curl:
```
       curl http://localhost:8000/start
```
13.- Al ejecutar el curl, notaras en la terminal 2 y terminal 3 que tanto servicio a como servicio b estan arrojando una excepcion. La excepcion se debe a un error en el archivo de configuración del collector.

14.- Corrige el error del collector.

15.- Una vez corregido el error en el archivo de configuración del collector deten y elimina el contenedor del collector en la terminal 1.
```
	docker rm -f otel-collector
```
16.- Deten el servicio a y el servicio b en sus respectivas terminales (2 y 3) ejecutando el comando:
```
ctrl + c
```
17.- Inicializa un nuevo contenedor del collector usando el comando del paso 7 en la terinal 1.

18.-Inicializa nuevamente los servicios a y b en sus respectivas terminales (2 y 3) ejecutando los siguientes comandos:
```
 uvicorn app.service_b.main:app --port 8001
 uvicorn app.service_a.main:app --port 8000
```

19.- En terminal 1 ejecuta el llamado al servicio a utilizando curl:
```
       curl http://localhost:8000/start
```
>En este punto ya no deberiamos ver excepciones en servicio a y b.
>
20.- Verifica en tu ambiente de Dynatrace que son visibles servicios a y b y sus respectivas trazas.
