import os
import json
from django.conf import settings
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras.applications import VGG16


class ModelClass:
    def __init__(self, model_name="FERPLUS"):
        lookup_path = os.path.join(
            settings.BASE_DIR, f"main/data/{model_name}/data_lookup_train.json"
        )
        weights_path = os.path.join(
            settings.BASE_DIR, f"main/data/{model_name}/model_weights.h5"
        )

        self.IMAGE_RES = 100
        self.lookup = self.load_lookup(lookup_path)
        self.num_classes = len(self.lookup.keys())
        self.model = self.load_model(model_name, weights_path)

    def load_lookup(self, file_name):
        with open(file_name, "r") as json_file:
            lookup = json.load(json_file)
        return {str(value): key.upper() for key, value in lookup.items()}

    def load_ferplus(self, weights_file):
        # self.IMAGE_RES = 100
        model = Sequential()
        model.add(
            Conv2D(
                32,
                (3, 3),
                activation="relu",
                input_shape=(self.IMAGE_RES, self.IMAGE_RES, 3),
            )
        )
        model.add(MaxPooling2D((2, 2)))
        model.add(Conv2D(64, (3, 3), activation="relu"))
        model.add(MaxPooling2D((2, 2)))
        model.add(Flatten())
        model.add(Dense(64, activation="relu"))
        model.add(Dense(self.num_classes, activation="softmax"))

        model.load_weights(weights_file)

        return model

    def load_resnet50_model(self, weights_file):

        base_model = VGG16(
            weights="imagenet",
            include_top=False,
            input_shape=(self.IMAGE_RES, self.IMAGE_RES, 3),
        )
        for layer in base_model.layers:
            layer.trainable = False
        model = Sequential()
        model.add(base_model)
        model.add(Flatten())
        model.add(Dense(64, activation="relu"))
        model.add(Dense(self.num_classes, activation="softmax"))
        model.load_weights(weights_file)
        return model

    def load_model(self, model_name, weights_file):
        if model_name == "FERPLUS":
            self.IMAGE_RES = 100
            return self.load_ferplus(weights_file)
        elif model_name == "VGG16":
            return self.load_resnet50_model(weights_file)
        # Add more models here as needed
        else:
            raise ValueError(
                "Invalid model name. Supported models are 'FERPLUS' and 'VGG16'."
            )

        return None
