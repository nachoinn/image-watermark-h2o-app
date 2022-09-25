from ui import AppInterface
from image_processing import ImageProcess
from data import DataManager


data = DataManager()
data.default_set()
image_process = ImageProcess(data)
app_ui = AppInterface(image_process, data)






