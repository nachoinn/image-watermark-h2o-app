from PIL import Image
from data import DataManager
import json
import os


class ImageProcess:
    def __init__(self, data: DataManager):
        self.image = Image
        self.data = data

    def process_images(self, img_list):
        """Receives the picture/pictures object names (location), and call a data module function to save it."""
        img_list = [img.name for img in img_list]
        img_dict = {
            "images": img_list

        }
        if img_list:
            self.data.save_data(img_dict)
        with open("data/h2o data.json") as data:
            images = json.load(data)
            return images["images"]

    def insert_watermark(self, watermark_path):
        format_ = self.data.reading_data("format")
        with open("data/h2o data.json") as data:
            data_file = json.load(data)
            if data_file["images"]:
                with self.image.open(watermark_path) as im2:
                    new_temp_path = watermark_path[:-4] + " temp.png"  # temporal modified watermark
                    im3 = im2.copy()
                    im3.putalpha(self.data.reading_data("opacity"))
                    im2.paste(im3, im2)
                    im2.save(new_temp_path)
                    im2 = self.image.open(new_temp_path)
                    im2 = im2.convert("RGBA")

                for im in data_file["images"]:
                    im1 = self.image.open(im)
                    im1.convert("RGBA")
                    im1.paste(im2, self.position(im1,im2), mask=im2)
                    new_name = (im.split("/")[-1].split(".")[0] + " by H2O Mark")
                    im1.save(f'{self.data.output_folder()}/{new_name}.{format_}', format=format_)
                    self.data.del_data("images")
                os.remove(new_temp_path)

            else:
                return "Images"

    def position(self, im1, im2):
        position = self.data.reading_data("position")
        if position == 3:
            width = (im1.width - im2.width) // 2
            height = (im1.height - im2.height) // 2

        elif position == 2:
            width = (im1.width - im2.width)
            height = 0

        elif position == 1:
            width = 0
            height = 0

        elif position == 5:
            width = (im1.width - im2.width)
            height = (im1.height - im2.height)

        elif position == 4:
            width = 0
            height = (im1.height - im2.height)

        return (width, height)