from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

video = cv2.VideoCapture("videos/store.mp4")

while True:
    success, frame = video.read()

    if not success:
        break

    results = model(frame)

    person_count = 0

    for box in results[0].boxes:
        cls = int(box.cls)

        if cls == 0:   # person class
            person_count += 1

    annotated_frame = results[0].plot()

    cv2.putText(
        annotated_frame,
        f"People Count: {person_count}",
        (20, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2
    )

    cv2.imshow("Store Intelligence", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()