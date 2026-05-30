from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2
import sqlite3
from datetime import datetime

# Load YOLO model
model = YOLO("yolov8n.pt")

# Initialize tracker
tracker = DeepSort(max_age=30)

# Connect database
conn = sqlite3.connect("database/store.db")
cursor = conn.cursor()

# Open video
video = cv2.VideoCapture("videos/store.mp4")

# Store already seen customers
seen_ids = set()

while True:

    success, frame = video.read()

    if not success:
        break

    # YOLO detection
    results = model(frame)

    detections = []

    for box in results[0].boxes:

        cls = int(box.cls)

        # Person class = 0
        if cls == 0:

            x1, y1, x2, y2 = box.xyxy[0]

            detections.append(
                (
                    [
                        float(x1),
                        float(y1),
                        float(x2 - x1),
                        float(y2 - y1)
                    ],
                    float(box.conf),
                    "person"
                )
            )

    # DeepSORT tracking
    tracks = tracker.update_tracks(
        detections,
        frame=frame
    )

    for track in tracks:

        if not track.is_confirmed():
            continue

        track_id = track.track_id

        l, t, r, b = track.to_ltrb()

        # Draw box
        cv2.rectangle(
            frame,
            (int(l), int(t)),
            (int(r), int(b)),
            (0, 255, 0),
            2
        )

        # Draw customer id
        cv2.putText(
            frame,
            f"Customer {track_id}",
            (int(l), int(t) - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

        # Save first appearance
        if track_id not in seen_ids:

            seen_ids.add(track_id)

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            cursor.execute(
                """
                INSERT INTO events
                (customer_id,event_type,timestamp)
                VALUES(?,?,?)
                """,
                (
                    int(track_id),
                    "entered",
                    timestamp
                )
            )

            conn.commit()

            print(
                f"Customer {track_id} Entered at {timestamp}"
            )

    cv2.imshow(
        "Store Intelligence System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

video.release()
conn.close()
cv2.destroyAllWindows()