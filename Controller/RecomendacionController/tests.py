from sqlite3 import IntegrityError

from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
import json
import requests
from django.db import connection

class recomendacionControllerTest(TestCase):
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

        articulaciones_data = [
            {"id": 7, "nombre": "Oreja"},
            {"id": 11, "nombre": "Hombro"},
            {"id": 13, "nombre": "Codo"},
            {"id": 15, "nombre": "Muñeca"},
            {"id": 23, "nombre": "Cadera"},
            {"id": 25, "nombre": "Rodilla"},
            {"id": 27, "nombre": "Tobillo"},
            {"id": 31, "nombre": "Dedo del pie"}
        ]
        with connection.cursor() as cursor:
            cursor.execute("""
                                       CREATE TABLE IF NOT EXISTS usuarios (
                                           id VARCHAR(200) PRIMARY KEY,
                                           prescripciones VARCHAR(200)
                                       )
                           """)
            cursor.execute("""INSERT IGNORE INTO usuarios (id, prescripciones)
                                VALUES ('d48c2bb2-8943-45fa-87bc-af63129f3bf8', 'dolor de rodilla')
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
            for ejercicio in ejercicios_data:
                cursor.execute("""
                    INSERT IGNORE INTO ejercicios (id, names)
                    VALUES (%s, %s)
                """, [ejercicio["id"], ejercicio ["names"]])

            cursor.execute("""
                                                    CREATE TABLE IF NOT EXISTS articulaciones (
                                                        id INT PRIMARY KEY,
                                                        nombre VARCHAR(100)
                                                    )
                                                """)

            for articulacion in articulaciones_data:
                cursor.execute("""
                    INSERT IGNORE INTO articulaciones (id, nombre)
                    VALUES (%s, %s)
                """, [articulacion["id"], articulacion ["nombre"]])

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

            cursor.execute("""
                            CREATE TABLE IF NOT EXISTS estadisticasejerciciousuario (
                                id INT PRIMARY KEY AUTO_INCREMENT,
                                idUsuario INT,
                                idpreferenciausuario INT,
                                repeticionesrealizadas INT,
                                peso INT,
                                fecha DATETIME
                            )
                        """)

            cursor.execute("""
                                        CREATE TABLE IF NOT EXISTS estadisticasarticulacionusuario (
                                            id INT PRIMARY KEY AUTO_INCREMENT,
                                            idUsuario INT,
                                            idarticulacion INT,
                                            repeticionescorrectas INT,
                                            idestadisticaejercicio INT,
                                            fecha DATETIME
                                        )
                                    """)

    def setUp(self):
        # Crear datos de prueba
        auth_url = "http://10.43.102.146:8080/authservice/user"
        #auth_url = "http://api-gateway:8080/authservice/user"
        self.prescripciones = "Tengo dolor de rodilla"
        correo = "majo"
        contrasenia = "pass123"
        params = {
            "correo": correo,
            "contrasenia": contrasenia
        }
        response = requests.get(auth_url, params=params)
        if response.status_code == 200:
            self.idUsuario = 'd48c2bb2-8943-45fa-87bc-af63129f3bf8'
            self.token = response.json().get("accessToken")  # Ajusta según el JSON que devuelva
            print("Token:", self.token)
        else:
            print("Error:", response.status_code, response.text)

    def testGetRecomendacion(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        url = reverse('recomendacion', args=[self.idUsuario])
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content.decode('utf-8'))
        self.assertIsNotNone(data)

    def testGetRecomendacionInvalidIdUsuario(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        self.idUsuario = "MYID"
        url = reverse('recomendacion', args=[self.idUsuario])
        from rest_framework.test import APIClient
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def testGetRecomendacionWithNoAuth(self):
        # Suponiendo que tu view tiene un nombre en urls.py
        url = reverse('recomendacion', args=[self.idUsuario])
        from rest_framework.test import APIClient
        client = APIClient()
        response = client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 403)
