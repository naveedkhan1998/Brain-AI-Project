import os
import json
from django.conf import settings
from tensorflow.keras import layers, models


class ModelClass:
    def __init__(self, model_name="CustomCNN"):
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

    def load_custom_cnn_model(self, weights_file):
        self.IMAGE_RES = 100
        model = models.Sequential(
            [
                layers.Conv2D(
                    32,
                    (3, 3),
                    activation="relu",
                    input_shape=(self.IMAGE_RES, self.IMAGE_RES, 3),
                ),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(64, (3, 3), activation="relu"),
                layers.MaxPooling2D((2, 2)),
                layers.Conv2D(64, (3, 3), activation="relu"),
                layers.Flatten(),
                layers.Dense(64, activation="relu"),
                layers.Dense(self.num_classes, activation="softmax"),
            ]
        )

        model.load_weights(weights_file)

        return model

    def load_resnet50_model(self, weights_file): ...

    def load_model(self, model_name, weights_file):
        if model_name == "CustomCNN":
            self.IMAGE_RES = 100
            return self.load_custom_cnn_model(weights_file)
        elif model_name == "ResNet50":
            return self.load_resnet50_model(weights_file)
        # Add more models here as needed
        else:
            raise ValueError(
                "Invalid model name. Supported models are 'CustomCNN' and 'ResNet50'."
            )

        return None
