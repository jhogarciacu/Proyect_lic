import sys
import os
from PySide6.QtWidgets import QApplication
from UI.main_window import InspectorApp

if __name__ == "__main__":
    app = QApplication(sys.argv)

    css_path = os.path.join(os.path.dirname(__file__), "UI", "estilos.css")
    try:
        with open(css_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
    except Exception as e:
        print(f"Error CSS: {e}")

    window = InspectorApp()
    window.show()
    sys.exit(app.exec())