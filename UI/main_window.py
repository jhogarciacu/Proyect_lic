import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, Qt

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

        # HACER QUE LA INTERFAZ SE VEA IGUAL:
        # 1. Establecemos el widget cargado como el centro
        self.setCentralWidget(self.ui)
        
        # 2. Copiamos el tamaño exacto que definiste en Designer
        self.resize(self.ui.size())
        
        # 3. Copiamos el título
        self.setWindowTitle(self.ui.windowTitle())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Cargar el CSS con UTF-8
    css_path = os.path.join(os.path.dirname(__file__), "estilos.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error CSS: {e}")
        
    window = InspectorApp()
    window.show()
    sys.exit(app.exec())