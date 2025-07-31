import gi
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt5.QtCore import QTimer

gi.require_version('Gst', '1.0')
gi.require_version('GstVideo', '1.0')
from gi.repository import Gst, GstVideo

Gst.init(None)

class VideoReceiver(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GStreamer Receiver")
        self.setMinimumSize(640, 480)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.video_frame = QFrame(self)
        self.video_frame.setStyleSheet("background-color: black;")
        layout.addWidget(self.video_frame)

        pipeline_desc = (
            'udpsrc port=5000 caps="application/x-rtp, media=video, encoding-name=H264, payload=96" ! '
            'rtph264depay ! avdec_h264 ! videoconvert ! glimagesink name=vsync sync=false'
        )
        self.pipeline = Gst.parse_launch(pipeline_desc)

        self.videosink = self.pipeline.get_by_name("vsync")

        self.embed_video_sink()

        self.bus = self.pipeline.get_bus()
        self.bus.add_signal_watch()
        self.bus.connect("message", self.on_gst_message)

        self.pipeline.set_state(Gst.State.PLAYING)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: None)
        self.timer.start(100)

    def embed_video_sink(self):
        window_id = int(self.video_frame.winId())
        if window_id:
            self.videosink.set_window_handle(window_id)

    def on_gst_message(self, bus, message):
        t = message.type
        if t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            print("GStreamer Erro:", err, debug)
            self.pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.EOS:
            print("End of Stream")
            self.pipeline.set_state(Gst.State.NULL)

    def closeEvent(self, event):
        self.pipeline.set_state(Gst.State.NULL)
        self.bus.remove_signal_watch()
        self.timer.stop()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoReceiver()
    window.show()
    sys.exit(app.exec_())