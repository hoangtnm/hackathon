import os

DATASET_PATH = "dataset"

# initialize the class labels in the dataset
CLASSES = ["Cyclone", "Earthquake", "Flood", "Wildfire"]

TRAIN_SPLIT = 0.75
VAL_SPLIT = 0.25
TEST_SPLIT = 0.1

BATCH_SIZE = 128
EPOCHS = 50

# set the path to the serialized model after training
CHECKPOINT_PATH = os.path.join('checkpoint', 'checkpoint.pth')


class GeoLocations:
    def __init__(self):
        self.name = 'Da Nang'
        self.latitude = 16.047079
        self.longitude = 108.206230
        self.zoom_level = 13
