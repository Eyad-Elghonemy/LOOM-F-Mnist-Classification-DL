import tensorflow as tf
from dotenv import load_dotenv
import os

load_dotenv(override=True)

# Get THe Variables
APP_NAME = os.getenv("APP_NAME")
VERSION = os.getenv("VERSION")
API_SECRET_KEY = os.getenv("API_SECRET_KEY")

# Parent Folder Path
SRC_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Model
MODEL = tf.keras.models.load_model(os.path.join(SRC_FOLDER, 'artifacts', 'model.keras'))

# Class Names
CLASS_NAMES = ['T_shirt', 'Trouser', 'Pullover', 'Dress', 'Coat',
               'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle_Boot']

