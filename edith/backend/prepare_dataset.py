# Google Colab Training
# from google.colab import drive
# drive.mount('/gdrive')
# !mkdir data
# !cp /gdrive/Shared\ drives/AI\ Training/datasets/disaster_dataset.zip .
# !unzip disaster_dataset.zip && rm disaster_dataset.zip

from utils import split_image_folder

split_image_folder('disaster_dataset', 'dataset')
