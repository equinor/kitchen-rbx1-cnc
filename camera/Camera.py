import cv2
from .BaseCamera import BaseCamera

class Camera(BaseCamera):
    @staticmethod
    def frames():
        camera = cv2.VideoCapture(0)
        params = (int(cv2.IMWRITE_JPEG_QUALITY), 90)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while not Camera.killCamera:
            # read current frame
            _, frame = camera.read()
            _, encoded = cv2.imencode('.jpg', frame, params)
            yield encoded.tobytes()