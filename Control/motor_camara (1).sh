#!/bin/bash

FOLDER="$HOME/fotos_camara_lic"
PORT="/dev/ttyACM0"
STEPS=8333  # 45 grados (ajústalo si es necesario)
TIMEOUT_CAPTURE=3  # Tiempo máximo de espera (segundos)

mkdir -p "$FOLDER"

# --- Inicializa motor ---
echo "Inicializando motor en $PORT ..."
sudo stty -F "$PORT" 9600 cs8 -cstopb -parenb
echo -e "ECHO1\rERRLVL0\rMA0\rDRES25000\rDRIVE1\rPSET0\r" | sudo tee "$PORT" > /dev/null

echo "📸 Capturando fotos y girando motor 45° después de cada toma."
echo "⛔ Presiona Ctrl+C para detener."

while true; do
    TIMESTAMP=$(date +"%Y%m%d-%H%M%S")
    FILENAME="photo-${TIMESTAMP}.raw"
    FULLPATH="$FOLDER/$FILENAME"

    echo "→ Capturando imagen..."

    # --- Captura con límite de tiempo controlado ---
    gphoto2 --capture-image-and-download --keep --filename "$FULLPATH" > /tmp/gphoto_log.txt 2>&1 &
    PID=$!

    # Esperar hasta TIMEOUT_CAPTURE segundos
    sleep $TIMEOUT_CAPTURE

    # Si sigue ejecutándose, finalizarlo
    if ps -p $PID > /dev/null 2>&1; then
        echo "⚠️ gphoto2 tardó demasiado, finalizando proceso..."
        kill -TERM $PID 2>/dev/null || true
        sleep 1
        kill -KILL $PID 2>/dev/null || true
    fi

    # Esperar a que el proceso termine completamente
    wait $PID 2>/dev/null || true

    # --- Pequeña espera para liberar el bus ---
    sleep 1
    killall gvfs-gphoto2-volume-monitor gvfsd-gphoto2 2>/dev/null

    # --- Validar captura antes de girar ---
    if grep -q "New file is in location" /tmp/gphoto_log.txt && [[ -f "$FULLPATH" ]]; then
        FILESIZE=$(stat -c%s "$FULLPATH")
        if [[ $FILESIZE -ge 5000 ]]; then
            echo "✅ Foto capturada correctamente: $FILENAME"

            sync
            sleep 1

            echo "↻ Girando motor 45°..."
            echo -e "A10\rV2\rD${STEPS}\rGO1\r" | sudo tee "$PORT" > /dev/null
            sleep 1
        else
            echo "⚠️ Archivo demasiado pequeño — omitiendo giro."
            rm -f "$FULLPATH"
        fi
    else
        echo "❌ Error en la captura — el motor NO girará."
        echo "🔍 Log de gphoto2:"
        tail -n 5 /tmp/gphoto_log.txt
    fi

    sleep 2.5
done
