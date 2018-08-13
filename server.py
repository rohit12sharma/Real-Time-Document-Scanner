from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera

app = Flask(__name__)

video_camera = None

@app.route('/')
def index():
    return render_template('index.html')

def video_frame():
    global video_camera 

    if video_camera == None:
        video_camera = VideoCamera()
        
    while True:
        frame = video_camera.get_video_frame()

        if frame is not None:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + video_camera.get_cached_frame() + b'\r\n\r\n')

@app.route('/video_viewer')
def video_viewer():
    return Response(video_frame(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)