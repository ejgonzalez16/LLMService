from py_eureka_client import eureka_client
import psutil

# Dirección del servidor Eureka
EUREKA_SERVER = "http://10.43.102.146:8761/eureka/"
IP_VPN = "10.101.138.234"

# Registrarlo
eureka_client.init(
    eureka_server=EUREKA_SERVER,
    app_name="llm-service",      # Nombre de tu servicio
    instance_port=8001,        # Puerto de Django
    instance_host=IP_VPN, # Host de la instancia
    prefer_ip=True,
    renewal_interval_in_secs=10,
    duration_in_secs=30,
)