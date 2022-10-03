from PIL import Image
from data import DataManager
import json
from tkinter import messagebox


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

    def insert_watermark(self, watermark_path, preview_mode=False):
        preview_list = []
        format_ = self.data.reading_data("format")
        images = self.data.reading_data("images")
        if images:
            with self.image.open(watermark_path) as im2:
                im2 = self.resize_watermark(im2)
                im3 = im2.copy()
                im3.putalpha(self.data.reading_data("opacity"))
                im3.convert("RGBA")
                im2.convert("RGBA")
                try:
                    im2.paste(im3, im2)
                except ValueError:
                    messagebox.showerror(title="Error", message="Your watermark should have transparent background.")
            print("loaded imgs list:", images)
            for im in images:
                im1 = self.image.open(im)
                im1.convert("RGBA")
                try:
                    im1.paste(im2, self.position(im1, im2), mask=im2)
                except ValueError:
                    im1.paste(im2, self.position(im1, im2))

                if not preview_mode:
                    new_name = (im.split("/")[-1].split(".")[0] + " by H2O Mark")
                    im1.save(f'{self.data.output_folder()}/{new_name}.{format_}', format=format_)
                    self.data.del_data("images")
                else:
                    preview_list.append(im1)
            return preview_list

        else:
            return False

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

    def resize_watermark(self, im2):
        size = int(self.data.reading_data("size"))
        if size == 100:
            return im2
        else:
            new_size = tuple(int((size / 100) * item) for item in im2.size)
            new_water = im2.resize(new_size)
            return new_water
