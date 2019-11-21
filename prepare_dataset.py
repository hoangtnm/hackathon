from utils import split_image_folder
# Import PyDrive and associated libraries.
# This only needs to be done once per notebook.
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials
#
# # Authenticate and create the PyDrive client.
# # This only needs to be done once per notebook.
# auth.authenticate_user()
# gauth = GoogleAuth()
# gauth.credentials = GoogleCredentials.get_application_default()
# drive = GoogleDrive(gauth)
#
# # Download a file based on its file ID.
# #
# # A file ID looks like: laggVyWshwcyP6kEI-y_W3P8D26sz
# file_id = 'REPLACE_WITH_YOUR_FILE_ID'
# downloaded = drive.CreateFile({'id': file_id})
# print('Downloaded content "{}"'.format(downloaded.GetContentString()))

# Google Colab Training
# from google.colab import drive
# drive.mount('/gdrive')
# !mkdir data
# !cp /gdrive/Shared\ drives/AI\ Training/datasets/Cyclone_Wildfire_Flood_Earthquake_Database.zip data/
# !unzip Cyclone_Wildfire_Flood_Earthquake_Database.zip -d Cyclone_Wildfire_Flood_Earthquake_Database

split_image_folder('Cyclone_Wildfire_Flood_Earthquake_Database', 'dataset')
