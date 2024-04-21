# consumers.py
import json
import cv2
import numpy as np
import base64
from PIL import Image
import asyncio
import mediapipe as mp
from channels.generic.websocket import AsyncWebsocketConsumer
from .ModelClass import ModelClass
from urllib.parse import parse_qs
from channels.exceptions import StopConsumer

RECTANGLE_SIZE = 30


class VideoStreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        selected_model = self.scope["query_string"].decode("utf-8")
        selected_model = parse_qs(selected_model).get("mode")

        if selected_model:
            selected_model = selected_model[0]
            # print(f"Selected model: {selected_model}")
        self.prev_predicted_label = "Scanning"
        self.count = 0
        self.model = ModelClass(model_name=selected_model)
        self.face = mp.solutions.face_mesh.FaceMesh(
            max_num_faces=1,  # Detect only one face
            refine_landmarks=True,  # Improve landmark accuracy
            min_detection_confidence=0.5,
        )
        self.loop = asyncio.get_running_loop()
        await self.accept()

    async def disconnect(self, close_code):
        self.face.close()
        raise StopConsumer()

    async def receive(self, bytes_data):
        if not bytes_data:
            print("Closed connection")
            await self.close()
            return

        try:
            self.frame = await self.loop.run_in_executor(
                None,
                cv2.imdecode,
                np.frombuffer(bytes_data, dtype=np.uint8),
                cv2.IMREAD_COLOR,
            )
            self.frame = cv2.flip(self.frame, 1)

            h, w, c = self.frame.shape

            result = self.face.process(self.frame)
            face_landmarks = result.multi_face_landmarks

            if face_landmarks:
                for face_landmarks in face_landmarks:
                    x_min, y_min, x_max, y_max = 10000, 10000, -1, -1

                    for landmark in face_landmarks.landmark:
                        x, y = int(landmark.x * w), int(landmark.y * h)
                        x_min = min(x_min, x)
                        y_min = min(y_min, y)
                        x_max = max(x_max, x)
                        y_max = max(y_max, y)

                    cv2.rectangle(
                        self.frame,
                        (x_min - RECTANGLE_SIZE, y_min - RECTANGLE_SIZE),
                        (x_max + RECTANGLE_SIZE, y_max + RECTANGLE_SIZE),
                        (0, 255, 0),
                        2,
                    )

                    if self.count > 10:
                        self.count = 0
                        img_crop = self.frame[
                            y_min - RECTANGLE_SIZE : y_max + RECTANGLE_SIZE,
                            x_min - RECTANGLE_SIZE : x_max + RECTANGLE_SIZE,
                        ]
                        img_crop = Image.fromarray(np.uint8(img_crop))
                        img_crop = img_crop.resize(
                            (self.model.IMAGE_RES, self.model.IMAGE_RES)
                        )
                        img_crop = np.array(img_crop)
                        img_crop = np.fliplr(img_crop)
                        img_crop = np.array(img_crop[:, :, ::-1], dtype="float32")
                        img_crop = img_crop / 255
                        img_crop = img_crop.reshape(
                            (1, self.model.IMAGE_RES, self.model.IMAGE_RES, 3)
                        )

                        predict_test = self.model.model.predict(img_crop)
                        predicted_label = np.argmax(predict_test)
                        self.prev_predicted_label = self.model.lookup[
                            str(predicted_label)
                        ]

                        cv2.putText(
                            self.frame,
                            f"Label: {self.prev_predicted_label}",
                            (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (36, 255, 12),
                            2,
                        )
                    else:
                        cv2.putText(
                            self.frame,
                            f"Label: {self.prev_predicted_label}",
                            (20, 60),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.9,
                            (36, 255, 12),
                            2,
                        )
                        self.count += 1

            self.buffer_img = await self.loop.run_in_executor(
                None, cv2.imencode, ".jpeg", self.frame
            )
            self.b64_img = base64.b64encode(self.buffer_img[1]).decode("utf-8")

            data_to_send = {
                "image": self.b64_img,
            }
            await self.send(json.dumps(data_to_send))

        except Exception as e:
            print(f"Error: {e}")
