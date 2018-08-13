import cv2
from document import Scanner

class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)
      
        # Initializing video recording environment
        self.is_record = True
        self.out = None
        self.transformed_frame = None

        self.scanner = Scanner()
        self.cached_frame = None
        self.fourcc = "MJPG"
        self.frameSize = (640,480)
        self.fps = 6
        self.video_filename = "./temp_video.avi"
        self.video_writer = cv2.VideoWriter_fourcc(*self.fourcc)
        self.video_out = cv2.VideoWriter(self.video_filename, self.video_writer, self.fps, self.frameSize)
        
    
    def __del__(self):
        self.cap.release()

    def get_video_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame, _ = self.scanner.detect_edge(frame)
            self.cached_frame = frame
            ret, jpeg = cv2.imencode('.jpg', frame)
            self.video_out.write(frame)
            return jpeg.tobytes()
        else:
            return None

    def capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            _, frame = self.scanner.detect_edge(frame, True)
            ret, jpeg = cv2.imencode('.jpg', frame)
            self.transformed_frame = jpeg.tobytes()
        else:
            return None

    def get_cached_frame(self):
        return self.cached_frame

    def get_image_frame(self):
        return self.transformed_frame

