import RPi.GPIO as GPIO
import time

# GPIOモードをBCMに設定
GPIO.setmode(GPIO.BCM)

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

    # トリガーピンを再び出力モードに設定
    GPIO.setup(TRIG_ECHO_PIN, GPIO.OUT)

    return distance

try:
    while True:
        dist = measure_distance()
        print(f"Measured Distance = {dist:.2f} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()
