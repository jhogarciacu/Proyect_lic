import serial
import time
import platform
from pathlib import Path
import requests
import os
import requests


class ControladorHardware:
    def __init__(self, puerto="/dev/ttyACM0", pasos=8333):
        self.puerto = puerto
        self.pasos = pasos
        self.ser = None
        self.sistema_operativo = platform.system()

        self.camera_ip = "172.20.10.2:8080"
        self.base_url = f"http://{self.camera_ip}/ccapi"

        # Carpeta raíz del proyecto
        base_dir = Path(__file__).resolve().parents[1]
        self.carpeta_imagenes = base_dir / "image_capture"
        self.carpeta_imagenes.mkdir(exist_ok=True)

    def conectar(self):
        if self.sistema_operativo == "Windows":
            print("⚠️ MODO SIMULACIÓN: Detectado Windows.")
            return True

        try:
            self.ser = serial.Serial(
                port=self.puerto,
                baudrate=9600,
                timeout=1
            )

            comando_init = "ECHO1\rERRLVL0\rMA0\rDRES25000\rDRIVE1\rPSET0\r"
            self.ser.write(comando_init.encode())
            print(f"✅ Motor conectado en {self.puerto}")
            return True

        except Exception as e:
            print(f"❌ Error al conectar motor: {e}")
            return False

    def girar_45_grados(self):
        comando = f"A10\rV2\rD{self.pasos}\rGO1\r"

        if self.ser and self.ser.is_open:
            self.ser.write(comando.encode())
            time.sleep(1.2)
        else:
            print("⚠️ SIMULACIÓN: giro motor")

    

    def capturar_foto(self):
        try:
            # Disparar
            url_shutter = f"{self.base_url}/ver100/shooting/control/shutterbutton"

            payload = {"af": True}

            r = requests.post(url_shutter, json=payload)
            print("SHUTTER STATUS:", r.status_code)

            if r.status_code != 200:
                print("Error al disparar")
                return None

            # Obtener lista de contenidos
            url_contents = f"{self.base_url}/ver100/contents"

            r = requests.get(url_contents)
            data = r.json()

            # Obtener último archivo
            last_file = data["contents"][-1]["url"]

            print("Último archivo:", last_file)

            # Descargar imagen
            r = requests.get(last_file)

            # Crear carpeta si no existe
            save_path = r"C:\Proyects\Proyect_lic\image capture"
            os.makedirs(save_path, exist_ok=True)

            filename = os.path.join(save_path, last_file.split("/")[-1])

            with open(filename, "wb") as f:
                f.write(r.content)

            print("📸 Imagen guardada en:", filename)

            return filename

        except Exception as e:
            print("ERROR:", e)
            return None

    def cerrar(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Puerto serial cerrado")