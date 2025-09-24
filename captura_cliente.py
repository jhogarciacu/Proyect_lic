import cv2

# indice, este abre la camara deseada
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

if not cap.isOpened():
    print("No se pudo abrir la cámara. Verifica el índice o si EOS Webcam Utility está activo.")
    exit()

# Configura resolución (opcional)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

while True:
    ret, frame = cap.read()
    if not ret:
        print("No se pudo leer el frame de la cámara.")
        break

    cv2.imshow("Canon EOS 90D (Webcam Mode)", frame)

    # q para salir 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()