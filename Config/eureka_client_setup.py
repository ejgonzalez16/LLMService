from py_eureka_client import eureka_client

# Dirección del servidor Eureka
EUREKA_SERVER = "http://eureka:8761/eureka/"

# Registrar el microservicio
eureka_client.init(
    eureka_server=EUREKA_SERVER,
    app_name="llm-service",      # Nombre de tu servicio
    instance_port=8001,        # Puerto de Django
    instance_host="localhost", # Host de la instancia
    renewal_interval_in_secs=10,
    duration_in_secs=30,
)