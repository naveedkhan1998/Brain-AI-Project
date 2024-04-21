import cv2
import numpy as np
from PIL import Image
from django.http import StreamingHttpResponse
from django.views.decorators.gzip import gzip_page
from django.shortcuts import render
from .ModelClass import ModelClass
import mediapipe as mp
from channels.generic.websocket import AsyncWebsocketConsumer
import base64


IMAGE_RES = 226
RECTANGLE_SIZE = 30


def frame_generator(model: ModelClass):
    video_capture = cv2.VideoCapture(
        0, cv2.CAP_DSHOW
    )  # remove dshow for a linux based server

    # Initialize mediapipe hands
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)

    # Read the first frame to get its dimensionsdeac
    _, frame = video_capture.read()
    h, w, c = frame.shape

    while True:
        success, frame = video_capture.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(framergb)
        hand_landmarks = result.multi_hand_landmarks

        if hand_landmarks:
            for handLMs in hand_landmarks:
                x_max = 0
                y_max = 0
                x_min = w
                y_min = h

                for lm in handLMs.landmark:
                    x, y = int(lm.x * w), int(lm.y * h)

                    if x > x_max:
                        x_max = x
                    if x < x_min:
                        x_min = x
                    if y > y_max:
                        y_max = y
                    if y < y_min:
                        y_min = y

                cv2.rectangle(
                    frame,
                    (x_min - RECTANGLE_SIZE, y_min - RECTANGLE_SIZE),
                    (x_max + RECTANGLE_SIZE, y_max + RECTANGLE_SIZE),
                    (0, 255, 0),
                    2,
                )

                try:
                    img_crop = frame[
                        y_min - RECTANGLE_SIZE : y_max + RECTANGLE_SIZE,
                        x_min - RECTANGLE_SIZE : x_max + RECTANGLE_SIZE,
                    ]
                    img_crop = Image.fromarray(np.uint8(img_crop))
                    img_crop = img_crop.resize((model.IMAGE_RES, model.IMAGE_RES))
                    img_crop = np.array(img_crop)
                    img_crop = np.fliplr(img_crop)
                    img_crop = np.array(img_crop[:, :, ::-1], dtype="float32")
                    img_crop = img_crop / 255
                    img_crop = img_crop.reshape(
                        (1, model.IMAGE_RES, model.IMAGE_RES, 3)
                    )

                    predict_test = model.model.predict(img_crop)
                    predicted_label = np.argmax(predict_test)

                    cv2.putText(
                        frame,
                        f"Label: {model.lookup[str(predicted_label)]}",
                        # f"Label: {model.lookup.values()}",
                        (20, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.9,
                        (36, 255, 12),
                        2,
                    )
                except Exception as e:
                    print(f"Error: {e}")

        _, buffer = cv2.imencode(".jpg", frame)
        frame_bytes = buffer.tobytes()
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n" + frame_bytes + b"\r\n\r\n"
        )

    # Close MediaPipe Hands after using
    hands.close()


@gzip_page
def video_feed(request):
    # Initialize your ModelClass
    model_base = ModelClass()
    # model = model_base.load_model()
    model = model_base
    return StreamingHttpResponse(
        frame_generator(model), content_type="multipart/x-mixed-replace; boundary=frame"
    )


def home(request):
    return render(request, "main/home.html")


def video_page(request):
    return render(request, "main/video_page.html")


def about_us(request):
    return render(request, "main/about_us.html")


def contact(request):
    return render(request, "main/contact.html")
