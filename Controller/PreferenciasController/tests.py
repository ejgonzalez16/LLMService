from sqlite3 import IntegrityError

from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
import json
import requests
from django.db import connection

class preferenciasControllerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        ejercicios_data = [
            {"id": 1, "names": "Chest Press"},
            {"id": 2, "names": "Push Ups"},
            {"id": 3, "names": "Squat"},
            {"id": 4, "names": "Lateral Raises"},
            {"id": 5, "names": "Deadlift"},
            {"id": 6, "names": "Biceps Curl"},
            {"id": 7, "names": "Barbell Row"},
            {"id": 8, "names": "Bench Press"},
            {"id": 9, "names": "Pull Ups"},
            {"id": 10, "names": "Dips"},
        ]
        with connection.cursor() as cursor:
            cursor.execute("""
                                       CREATE TABLE IF NOT EXISTS usuarios (
                                           id VARCHAR(200) PRIMARY KEY
                                       )
                           """)
            cursor.execute("""INSERT IGNORE INTO usuarios (id)
                                VALUES ('e8ee7728-7492-4c89-89ad-00af4d879c8b')
                                       """)
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tiposrango (
                        id INT PRIMARY KEY,
                        nombre VARCHAR(100)
                    )
                """)
            cursor.execute("""DELETE FROM tiposrango
                                                    
                                                """)
            cursor.execute("INSERT IGNORE INTO tiposrango (id, nombre) VALUES (1, 'Moderado')")
            cursor.execute("INSERT IGNORE INTO tiposrango (id, nombre) VALUES (2, 'Normal')")
            cursor.execute("INSERT IGNORE INTO tiposrango (id, nombre) VALUES (3, 'Exigente')")
            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS ejercicios (
                                id INT PRIMARY KEY,
                                nombre VARCHAR(100),
                                descripcion VARCHAR(100),
                                modeloAR VARCHAR(100),
                                vista VARCHAR(100),
                                gesto VARCHAR(100),
                                imagen VARCHAR(100),
                                names VARCHAR(100)
                            )
                        """)
            cursor.execute("""DELETE FROM ejercicios
                                        
                                    """)
            with connection.cursor() as cursor:
                for ejercicio in ejercicios_data:
                    cursor.execute("""
                        INSERT IGNORE INTO ejercicios (id, names)
                        VALUES (%s, %s)
                    """, [ejercicio["id"], ejercicio ["names"]])
            with connection.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS preferenciasusuario (
                        id INT PRIMARY KEY AUTO_INCREMENT,
                        idusuario VARCHAR(100),
                        idtiporango INT,
                        fecha DATETIME,
                        esactiva BOOLEAN,
                        idejercicio INT
                    )
                """)

    def setUp(self):
        # Crear datos de prueba
        #auth_url = "http://10.43.102.146:8080/authservice/user"
        auth_url = "http://api-gateway:8080/authservice/user"
        self.idUsuario = "e8ee7728-7492-4c89-89ad-00af4d879c8b"
        self.prescripciones = "Tengo dolor de rodilla"
        correo = "majo"
        contrasenia = "pass123"
        params = {
            "correo": correo,
            "contrasenia": contrasenia
        }
        response = requests.get(auth_url, params=params)
        if response.status_code == 200:
            self.token = response.json().get("accessToken")  # Ajusta según el JSON que devuelva
            print("Token:", self.token)
        else:
            print("Error:", response.status_code, response.text)

    def testInsertarPreferencias(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        url = reverse('insertarPreferencias', args=[self.idUsuario])
        payload = {
            "prescripciones": self.prescripciones
        }
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIsNotNone(data)

    def testInsertarPreferenciasInvalidIdUsuario(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        self.idUsuario = "MYID"
        url = reverse('insertarPreferencias', args=[self.idUsuario])
        payload = {
            "prescripciones": self.prescripciones
        }
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def testInsertarPreferenciasNoPrescripciones(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        url = reverse('insertarPreferencias', args=[self.idUsuario])
        payload = {
        }
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def testInsertarPreferenciasWithNoAuth(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        url = reverse('insertarPreferencias', args=[self.idUsuario])
        payload = {
            "prescripciones": self.prescripciones
        }
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(response.status_code, 403)
