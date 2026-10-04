import cv2
import numpy as np
import time

THRESHOLD = 3.0        # حساسیت (کمتر = حساس‌تر)
COOLDOWN = 0.25        # فاصله بین دو تکون (ثانیه)
SHOW_WINDOW = True     # پنجره دوربین رو نشون بده

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("دوربین پیدا نشد")
    exit()

count = 0
last_hit = 0
prev_gray = None

print("شروع شد... لپ‌تاپ رو تکون بده (خروج: کلید q)")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # کوچیکش کن که سریع‌تر پردازش شه
    small = cv2.resize(frame, (320, 240))
    gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is None:
        prev_gray = gray
        continue

    # اختلاف فریم فعلی با فریم قبلی = میزان حرکت
    diff = cv2.absdiff(prev_gray, gray)
    motion = float(np.mean(diff))

    prev_gray = gray

    now = time.time()
    if motion > THRESHOLD and (now - last_hit) > COOLDOWN:
        last_hit = now
        count += 1
        print(f"\rتکون: {count}  (شدت: {motion:.1f})", end="", flush=True)

    if SHOW_WINDOW:
        # متن شمارنده روی تصویر
        cv2.putText(frame, f"Count: {count}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 200), 3)
        cv2.putText(frame, f"Motion: {motion:.1f}", (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (200, 200, 200), 2)
        # خط آستانه
        color = (0, 0, 255) if motion > THRESHOLD else (0, 255, 200)
        cv2.putText(frame, f"Threshold: {THRESHOLD}", (10, 110),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
        cv2.imshow("Shake Counter", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n\nجمع کل: {count} تکون")