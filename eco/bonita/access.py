import requests
from http.cookiejar import CookieJar

class Access:
    bonita_url = 'http://localhost:8080/bonita'
    bonita_token = ''
    
    def __init__(self, username):
        self.username = username
        self.password = username
        # Crear un objeto CookieJar para almacenar las cookies
        self.cookie_jar = CookieJar()
        # Crear una sesión de requests y asignarle el CookieJar
        self.session = requests.Session()
        self.session.cookies = self.cookie_jar

    def login(self):        
        response = self.session.post(f'{self.bonita_url}/loginservice', data={
            "username": self.username,
            "password": self.password,
            "redirect": False
        })

        # Extraer el token de la cookie
        if response.status_code == 204:  # Verificar que el inicio de sesión fue exitoso
            self.bonita_token = self.get_cookie_by_name("X-Bonita-API-Token")
            if self.bonita_token:
                # Automatically add the token to the session headers
                self.session.headers.update({"X-Bonita-API-Token": self.bonita_token})
        else:
            print("Error during login:", response.status_code)

        return response

    def get_cookie_by_name(self, cookie_name):
        """Devuelve el valor de la cookie con el nombre especificado."""
        for cookie in self.cookie_jar:
            if cookie.name == cookie_name:
                return cookie.value
        return None

    def get_token(self):
        return self.bonita_token

    def make_request(self, method, endpoint, **kwargs):
        """
        Make a request (GET, POST, etc.) to the Bonita API.
        Token is automatically included in the headers.
        """
        url = f'{self.bonita_url}/{endpoint}'
        response = self.session.request(method, url, **kwargs)
        return response

    def make_request_list(self, method, endpoint, payload):
            """
            Make a request (GET, POST, etc.) to the Bonita API.
            Token is automatically included in the headers.
            """
            url = f'{self.bonita_url}/{endpoint}'
            # Imprimir la solicitud que se va a enviar para depuración
            print(f"URL: {url}")
            print(f"Payload: {payload}")

            try:
                # Realizar la solicitud usando 'json=' para serializar a JSON
                response = self.session.request(method, url, json=payload)

                # Imprimir detalles de la respuesta para depuración
                print(f"Status Code: {response.status_code}")
                print(f"Response Text: {response.text}")

                return response

            except requests.exceptions.RequestException as e:
                print(f"Error al realizar la solicitud: {e}")
                return None
                
            return response
