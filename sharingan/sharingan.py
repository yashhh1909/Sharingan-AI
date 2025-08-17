import cv2
import mediapipe as mp
import numpy as np
import math
import time

mp_face = mp.solutions.face_detection
face = mp_face.FaceDetection(0.7)

width, height = 1400, 770
eye_radius_x = 60
eye_radius_y = 30
pupil_radius = 12
sensitivity = 0.07
bg_img = cv2.imread("shh.jpg")
if bg_img is None:
    print(" Error: Background image not found!")
    exit()
bg_img = cv2.resize(bg_img, (width, height))


overlay_png = cv2.imread("top.png", cv2.IMREAD_UNCHANGED)
if overlay_png is None:
    print(" Error: Overlay PNG not found!")
    exit()
cap = cv2.VideoCapture(0)

def draw_sharingan_eye(img, center, dx, dy, slant_direction):
    pupil_center = (center[0] + dx, center[1] + dy)

    for i in range(5, 0, -1):
        glow_radius = pupil_radius + i * 3
        glow_color = (0, 0, 120 + i * 25)
        cv2.circle(img, pupil_center, glow_radius, glow_color, -1)

    cv2.circle(img, pupil_center, pupil_radius + 5, (0, 0, 255), -2)
    cv2.circle(img, pupil_center, pupil_radius - 6, (0, 0, 0), -1)

    angle_offset = time.time() % 6 * math.pi / 3
    for i in range(3):
        angle = i * 2 * math.pi / 3 + angle_offset
        r = pupil_radius + 10
        tx = int(pupil_center[0] + r * math.cos(angle))
        ty = int(pupil_center[1] + r * math.sin(angle))
        cv2.circle(img, (tx, ty), 5, (0, 0, 0), -1)
        cv2.ellipse(img, (tx, ty), (4, 7), math.degrees(angle), 0, 360, (0, 0, 0), -1)

def overlay_image_at_position(background, overlay, x, y, scale=1.0):
    """
    Overlay a transparent PNG image (with alpha) at a specific position (x, y).
    Handles cropping if overlay goes out of bounds.
    """
    if overlay.shape[2] != 4:
        print(" Overlay image must have alpha channel.")
        return background

    overlay_resized = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
    h, w = overlay_resized.shape[:2]


    x1 = max(0, x)
    y1 = max(0, y)
    x2 = min(background.shape[1], x + w)
    y2 = min(background.shape[0], y + h)

    overlay_x1 = max(0, -x) 
    overlay_y1 = max(0, -y)

    overlay_crop = overlay_resized[overlay_y1:overlay_y1 + (y2 - y1), overlay_x1:overlay_x1 + (x2 - x1)]

    if overlay_crop.shape[0] == 0 or overlay_crop.shape[1] == 0:
        return background

    overlay_img = overlay_crop[:, :, :3]
    mask = overlay_crop[:, :, 3:] / 255.0

    roi = background[y1:y2, x1:x2]
    blended = roi * (1 - mask) + overlay_img * mask
    background[y1:y2, x1:x2] = blended.astype(np.uint8)
    return background


while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face.process(rgb)

    eye_img = bg_img.copy()

    left_center = (width // 2 - 155, height // 2)
    right_center = (width // 2 + 155, height // 2)
    screen_center = (width // 2, height // 2)

    dx, dy = 0, 0

    if results.detections:
        for detection in results.detections:
            bbox = detection.location_data.relative_bounding_box
            face_x = int((bbox.xmin + bbox.width / 2) * width)
            face_y = int((bbox.ymin + bbox.height / 3) * height)

            dx = int((face_x - screen_center[0]) * sensitivity)
            dy = int((face_y - screen_center[1]) * sensitivity)

            dist = np.hypot(dx, dy)
            max_move = eye_radius_x - pupil_radius
            if dist > max_move:
                scale = max_move / dist
                dx = int(dx * scale)
                dy = int(dy * scale)
            break

    draw_sharingan_eye(eye_img, left_center, dx, dy, slant_direction=-1)
    draw_sharingan_eye(eye_img, right_center, dx, dy, slant_direction=1)

    eye_img = overlay_image_at_position(eye_img, overlay_png, x=223, y=60, scale=1.6)

    cv2.imshow("SHARINGAN AI 👁️👁️", eye_img)

    if cv2.waitKey(1) & 0xFF == 27 or cv2.getWindowProperty("SHARINGAN AI 👁️👁️", cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
