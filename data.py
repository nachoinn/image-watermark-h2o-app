import json
import os


default = {
        "images": [],
        "watermark": "",
        "opacity": 50,
        "position": 3,
        "out_folder": "output images",
        "format": "jpeg",
        "size": "100",
        "select": 0,
    }

class DataManager:

    def default_set(self):
        """Creates default settings inside a .json file if they don't exist previously."""
        try:
            with open("data/h2o data.json", "r") as def_:
                json.load(def_)
        except FileNotFoundError:
            if not os.path.exists("data"):
                os.makedirs("data")
            with open("data/h2o data.json", "w") as data_error:
                json.dump(default, data_error, indent=4)

    def save_data(self, data_to_save):
        """Saves input parameters into the .json file as, images, watermark, transparency, position..."""
        try:
            with open("data/h2o data.json", "r") as data:
                data_file = json.load(data)
                data_file.update(data_to_save)
        except FileNotFoundError:
            self.default_set()
        else:
            with open("data/h2o data.json", "w") as data_save:
                json.dump(data_file, data_save, indent=4)

    def del_data(self, data_to_del):
        data_deleting = {
            data_to_del: ""
        }
        try:
            with open("data/h2o data.json", "r") as data:
                data_file = json.load(data)
                data_file.update(data_deleting)
        except FileNotFoundError:
            pass
        else:
            with open("data/h2o data.json", "w") as data_save:
                json.dump(data_file, data_save, indent=4)

    def output_folder(self, out_fol=None):
        if out_fol is None:
            out_fol = self.reading_data("out_folder")

        if not os.path.exists(out_fol):
            os.makedirs(out_fol)
            output_folder = {
                "out_folder": out_fol
            }
            self.save_data(output_folder)

        return self.reading_data("out_folder")

    def reading_data(self, data_to_read):
        with open("data/h2o data.json") as file_read:
            data = json.load(file_read)

            return data[data_to_read]