import serial
import time
import platform
from pathlib import Path
import requests
import os
import requests
from serial.tools import list_ports
import cv2
import numpy as np
import requests


class ControladorHardware:
    def __init__(self, puerto=None, pasos=66664):
        self.puerto = puerto
        self.pasos = pasos
        self.ser = None
        self.sistema_operativo = platform.system()

        self.camera_ip = "172.18.226.42:8080"
        self.base_url = f"http://{self.camera_ip}/ccapi"

        # Carpeta raíz del proyecto
        base_dir = Path(__file__).resolve().parents[1]
        self.carpeta_imagenes = base_dir / "image_capture"
        self.carpeta_imagenes.mkdir(exist_ok=True)



    def detectar_puerto(self):

        puertos = list_ports.comports()

        for puerto in puertos:
            print("Detectado:", puerto.device, puerto.description)

            if "USB" in puerto.description:
                return puerto.device

        return None

    def conectar(self):

        if self.puerto is None:
            self.puerto = self.detectar_puerto()

        if self.puerto is None:
            print("❌ No se encontró el motor")
            return False

        try:
            self.ser = serial.Serial(
                port=self.puerto,
                baudrate=9600,
                timeout=1
            )

            time.sleep(2)

            print(f"✅ Motor conectado en {self.puerto}")

            return True

        except Exception as e:
            print(f"❌ Error al abrir puerto: {e}")
            return False

    def girar_n_grados(self,angulo):

        pasos = int((angulo / 360) * self.pasos)

        comando = f"A10\rV2\rD{pasos}\rGO1\r"

        try:
            if self.ser and self.ser.is_open:
                self.ser.write(comando.encode())
                time.sleep(0.5)
                print("🔄 Motor giró")
                return True
            else:
                print("⚠️ SIMULACIÓN: giro motor")
                return True  # simulación exitosa

        except Exception as e:
            print(f"❌ Error en giro: {e}")
            return False

    

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
            url_contents = f"{self.base_url}/ver100/contents/sd/100CANON/IMG_0003.JPG"

            r = requests.get(url_contents)

            print("STATUS CONTENTS:", r.status_code)
            print("BODY:", r.text)

            data = r.json()

            # Obtener último archivo
            last_file = data["contents"][-1]["url"]

            print("Último archivo:", last_file)

            # Descargar imagen
            r = requests.get(last_file)

        except Exception as e:
            print("ERROR:", e)
            return None
        
    def iniciar_liveview(self):

        try:

            # activar liveview
            url_start = f"{self.base_url}/ver100/shooting/liveview/rtp"

            payload = {
                "rtpport": 50000
            }

            r = requests.post(url_start, json=payload)

            print("LIVEVIEW START:", r.status_code)

            if r.status_code != 200:
                print("❌ No se pudo activar LiveView")
                return False

            # abrir stream
            url_stream = f"{self.base_url}/ver100/shooting/liveview/stream"

            self.stream = requests.get(
                url_stream,
                stream=True,
                timeout=5
            )

            self.bytes_data = b''

            print("📡 LiveView iniciado")

            return True

        except Exception as e:

            print("❌ Error iniciando LiveView:", e)

            return False
        

    def obtener_frame_liveview(self):

        try:

            for chunk in self.stream.iter_content(chunk_size=1024):

                self.bytes_data += chunk

                a = self.bytes_data.find(b'\xff\xd8')
                b = self.bytes_data.find(b'\xff\xd9')

                if a != -1 and b != -1:

                    jpg = self.bytes_data[a:b+2]
                    self.bytes_data = self.bytes_data[b+2:]

                    img = cv2.imdecode(
                        np.frombuffer(jpg, dtype=np.uint8),
                        cv2.IMREAD_COLOR
                    )

                    return img

        except:
            return None
    
    def cerrar(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Puerto serial cerrado")