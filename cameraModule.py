import cv2
import numpy as np
import time

def create_placeholder_frame(text, width=640, height=480):
    # Creates a placeholder frame with a message
    frame = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(frame, text, (50, height // 2), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 255), 2, cv2.LINE_AA)
    return frame

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

    print("Streaming started...")

    cap = cv2.VideoCapture(0)
    placeholder_frame = create_placeholder_frame("Camera not found")

    try:
        while True:
            if not cap.isOpened():
                # Retry every second to see if the camera has been connected
                out.write(placeholder_frame)
                time.sleep(1)
                cap = cv2.VideoCapture(0)
                continue

            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

            ret, frame = cap.read()
            if not ret:
                # Lost connection to camera mid-stream
                cap.release()
                cap = cv2.VideoCapture(0)
                continue
                        
            # OpenCV pipeline goes here
            # Example (grayscale to color conversion to match RGB output):
            # frame = cv2.cvtColor(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)

            out.write(frame)

    except KeyboardInterrupt:
        print("Streaming stopped by user.")

    finally:
        cap.release()
        out.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
