import RPi.GPIO as GPIO
import time
import cv2  # OpenCVライブラリ
from google.cloud import vision
import io
import pyttsx3

# GPIOモードをBCMに設定
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)  # 警告を無視する

# ピンの設定
TRIG_ECHO_PIN = 23
GPIO.setup(TRIG_ECHO_PIN, GPIO.OUT)

# 距離を測定する関数
def measure_distance():
    # トリガーをセット（出力モード）
    GPIO.output(TRIG_ECHO_PIN, False)
    time.sleep(0.5) # 安定化のための待機時間

    GPIO.output(TRIG_ECHO_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_ECHO_PIN, False)

    # エコーピンを入力モードに設定
    GPIO.setup(TRIG_ECHO_PIN, GPIO.IN)

    start_time = time.time()
    stop_time = time.time()

    # エコーがHighになるのを待つ
    while GPIO.input(TRIG_ECHO_PIN) == 0:
        start_time = time.time()

    # エコーがLowになるのを待つ
    while GPIO.input(TRIG_ECHO_PIN) == 1:
        stop_time = time.time()

    # 経過時間を計測
    elapsed_time = stop_time - start_time
    # 距離を計算（音速＝34300cm/秒）
    distance = (elapsed_time * 34300) / 2
    print(distance)

    # トリガーピンを再び出力モードに設定
    GPIO.setup(TRIG_ECHO_PIN, GPIO.OUT)

    return distance

# カメラを使用して画像をキャプチャする関数
def capture_image():
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

# 画像データから物体を検出する関数
def detect_objects(content):
    """画像データから物体を検出します。"""
    client = vision.ImageAnnotatorClient()

    image = vision.Image(content=content)
    response = client.object_localization(image=image)
    objects = response.localized_object_annotations
    print(objects)

    result = []
    for object_ in objects:
        result.append(object_.name)

    if response.error.message:
        raise Exception('{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(response.error.message))
    
    return result

# 音声でテキストを読み上げる関数
def speak(engine, text):
    engine.say(text)
    engine.runAndWait()

# センサーとカメラの処理を組み合わせる関数
def sensor_and_camera():
    dist = measure_distance()  # 超音波センサーで距離を測定
    image_data = capture_image()  # カメラの画像データ
    return dist, image_data

# メインの処理
if __name__ == "__main__":
    engine = pyttsx3.init()  # 音声エンジンを初期化

    try:
        while True:
            dist, image_data = sensor_and_camera()
            if dist is not None and image_data is not None:
                speak(engine, f"{dist:.2f}メートル")
                recognized_objects = detect_objects(image_data)
                for name in recognized_objects:
                    speak(engine, name)
            time.sleep(5)  # 5秒待機

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
