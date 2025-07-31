import cv2
import numpy as np

def main():
    # Define GStreamer pipeline to stream over UDP with low latency
    gst_pipeline = (
        'appsrc ! videoconvert ! '
        'x264enc tune=zerolatency speed-preset=ultrafast bitrate=500 key-int-max=15 ! '
        'rtph264pay config-interval=1 pt=96 ! '
        'udpsink host=192.168.4.174 port=5000'
    )

    # Set up OpenCV VideoWriter with GStreamer pipeline
    out = cv2.VideoWriter(
        gst_pipeline,
        cv2.CAP_GSTREAMER,
        0,  # fourcc (not used here)
        30.0,  # FPS
        (640, 480),  # frame size
        True
    )

    if not out.isOpened():
        print("Failed to open video writer")
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Failed to open camera")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Streaming started...")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # OpenCV pipeline goes here
        # Example (grayscale to color conversion to match RGB output):
        # frame = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

        out.write(frame)
    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
