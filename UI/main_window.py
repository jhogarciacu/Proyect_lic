import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt
from Control.controlador_hardware import ControladorHardware

class InspectorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Cargar el archivo .ui
        loader = QUiLoader()
        ui_path = os.path.join(os.path.dirname(__file__), "Qt_designer.ui")
        ui_file = QFile(ui_path)
        
        
        if not ui_file.open(QFile.ReadOnly):
            print(f"Error: No se encontró el archivo UI en {ui_path}")
            return

        # Cargamos la interfaz directamente
        self.ui = loader.load(ui_file)
        ui_file.close()

        # Establecemos el widget cargado como el centro
        self.setCentralWidget(self.ui)
        
        # Copiamos el tamaño exacto de Designer
        self.resize(self.ui.size())
        
        # Copiamos el título
        self.setWindowTitle(self.ui.windowTitle())

        #controlador
        self.controlador = ControladorHardware()
        self.controlador.conectar()


        #conexion de boton con acción
        self.ui.btn_capture.clicked.connect(self.on_capturar)

    def on_capturar(self):
        print("🟢 Botón capturar presionado")

        ruta = self.controlador.capturar_foto()

        if ruta:
            print(f"📸 Imagen guardada en: {ruta}")
        else:
            print("❌ Falló la captura")

    def closeEvent(self, event):
        self.controlador.cerrar()
        event.accept()
