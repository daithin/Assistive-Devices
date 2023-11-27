import cv2

# カメラデバイスのインデックスを指定
# これは 'device003' に対応するインデックス番号に置き換える必要があります
camera_index = 0
print(cv2.__version__)

# カメラキャプチャの初期化
cap = cv2.VideoCapture(camera_index)

# カメラがオープンしているか確認
if not cap.isOpened():
    print("カメラを開けませんでした。")
    exit()

try:
    while True:
        # フレームをキャプチャする
        ret, frame = cap.read()

        # フレームが正しくキャプチャされたか確認
        if not ret:
            print("フレームを取得できませんでした。終了します。")
            break

        # 画像をグレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 画像を画面に表示
        # cv2.imshow('Camera Frame', gray)

        # 'q'を押したらループから抜ける
        if cv2.waitKey(1) == ord('q'):
            break
except KeyboardInterrupt:
    # Ctrl+Cが押された場合の処理
    print("プログラムを中断しました。")

# キャプチャをリリースし、ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
