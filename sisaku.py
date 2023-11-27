from google.cloud import vision
import io
import pyttsx3
import cv2  # OpenCVライブラリ

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def detect_objects(content):
    """画像データから物体を検出します。"""
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    result = []
    for object_ in objects:
        result.append(object_.name)

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))
    
    return result

def capture_image():
    """カメラを使用して画像をキャプチャします。"""
    cap = cv2.VideoCapture(0)  # 0はデフォルトのカメラを指します

    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        return None
    cap.release()

    # OpenCVの画像をJPEG形式のバイトデータに変換
    ret, buffer = cv2.imencode('.jpg', frame)
    if not ret:
        print("Failed to encode image")
        return None

    return buffer.tobytes()

def sensor_and_camera():
    detected = True  # センサーが物体を検出したか
    long = 5  # 物体までの距離
    image_data = capture_image()  # カメラの画像データ
    return detected, long, image_data

if __name__ == "__main__":
    engine = pyttsx3.init()  # 音声エンジンを初期化

    detected, long, image_data = sensor_and_camera()
    if detected and image_data is not None:
        speak(engine, f"{long}メートル")
        recognized_objects = detect_objects(image_data)
        for name in recognized_objects:
            speak(engine, name)
