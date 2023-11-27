from google.cloud import vision
import io
import pyttsx3

def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

def detect_objects(path):
    """Local image fileで物体検出を行います。"""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations

    result = []
    for object_ in objects:
        result.append((object_.name, object_.score))

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))
    
    return result

def image_recognition(image_path):
    """画像データから物体を認識して結果を返します。"""
    recognized_objects = detect_objects(image_path)
    return recognized_objects

def sensor_and_camera():
    detected = True  # センサーが物体を検出したか
    long = 5  # 物体までの距離
    image_data = r"C:\Users\81802\Desktop\画像自分フォト\ookami.png"  # カメラの画像データ
    return detected, long, image_data

if __name__ == "__main__":
    engine = pyttsx3.init()  # 音声エンジンを初期化

    detected, long, image_data = sensor_and_camera()
    if detected:
        speak(engine, f"{long}メートル")
        recognized_objects = image_recognition(image_data)
        for name, score in recognized_objects:
            speak(engine, f"{name} detected with confidence {score}")
