from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

model = YOLO("yolov8n.pt")
tracker = DeepSort(max_age=30)

video = cv2.VideoCapture("videos/store.mp4")

unique_customers = set()

while True:

    success, frame = video.read()

    if not success:
        break

    results = model(frame)

    detections = []

    for box in results[0].boxes:

        if int(box.cls) == 0:

            x1, y1, x2, y2 = box.xyxy[0]

            detections.append(
                (
                    [float(x1), float(y1),
                     float(x2 - x1),
                     float(y2 - y1)],
                    float(box.conf),
                    "person"
                )
            )

    tracks = tracker.update_tracks(detections, frame=frame)

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id

        unique_customers.add(track_id)

        l, t, r, b = track.to_ltrb()

        cv2.rectangle(
            frame,
            (int(l), int(t)),
            (int(r), int(b)),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"ID:{track_id}",
            (int(l), int(t)-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2
        )

    occupancy = len(unique_customers)

    cv2.putText(
        frame,
        f"Occupancy: {occupancy}",
        (20,50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,0,255),
        2
    )

    cv2.imshow("Store Analytics", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()