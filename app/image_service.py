

from IPython.display import display, Audio, Image

import requests
from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image as PilImage

class ImageService:

    def __init__(self, url):
        self.url = url

    def display_in_colab(self, height=250):
        display(Image(url=self.url, height=height))

    def display(self):
        response = requests.get(self.url)
        image = PilImage.open(BytesIO(response.content))
        plt.imshow(image)
        plt.show()
