from ultralytics import YOLO
from deep_sort_realtime.deepsort_tracker import DeepSort
import cv2

model = YOLO("yolov8n.pt")

video_files = [
    "CAM 1.mp4",
    "CAM 2.mp4",
    "CAM 3.mp4",
    "CAM 4.mp4",
    "CAM 5.mp4"
]

for video_name in video_files:

    print(f"\nProcessing {video_name}...\n")

    tracker = DeepSort(max_age=30)

    video = cv2.VideoCapture(
        f"videos/{video_name}"
    )

    while True:

        success, frame = video.read()

        if not success:
            break

        results = model(frame)

        detections = []

        for box in results[0].boxes:

            cls = int(box.cls)

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

        tracks = tracker.update_tracks(
            detections,
            frame=frame
        )

        for track in tracks:

            if not track.is_confirmed():
                continue

            track_id = track.track_id

            l, t, r, b = track.to_ltrb()

            cv2.rectangle(
                frame,
                (int(l), int(t)),
                (int(r), int(b)),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                f"ID: {track_id}",
                (int(l), int(t) - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        cv2.imshow(
            f"Customer Tracking - {video_name}",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()

cv2.destroyAllWindows()