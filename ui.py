from tkinter import Tk, filedialog, Canvas, PhotoImage, Label, ttk, Button, IntVar, Radiobutton, Scale
from tkinter import messagebox
from image_processing import ImageProcess
from data import DataManager
from PIL import Image, ImageTk

FONT1 = ("Arial", 20, "italic")
FONT2 = ("Arial", 12, "bold")
THEME_COLOR = ["#C3F8FF", "#ABD9FF", "#FFF6BF", "#FFEBAD"]


class AppInterface:

    def __init__(self, image_process: ImageProcess, data: DataManager):
        self.window = Tk()
        self.window.geometry("1366x768")
        self.window.title("H2OMark 💧")
        self.window.config(padx=20, pady=20, bg=THEME_COLOR[0])
        self.image_process = image_process
        self.data = data

        self.canvas = Canvas(self.window, height=150, width=120, bg=THEME_COLOR[0], highlightthickness=0)

        self.logo = PhotoImage(file="images/H2O-MARK-LOGO.png")
        self.canvas.create_image(60, 80, image=self.logo)
        self.canvas.grid(column=2, row=0, columnspan=3, pady=50)

        self.load_images = Button(text="Load Images       💧", bd=0, activebackground=THEME_COLOR[1],
                                  highlightthickness=0, command=self.load_images)
        self.load_images.grid(column=0, row=1, padx=50)

        self.load_water = Button(text="Load Watermark 💧", bd=0, activebackground=THEME_COLOR[0],
                                 highlightthickness=0, command=self.load_watermark)
        self.load_water.grid(column=0, row=2, padx=50)

        self.watermark_canvas = Canvas(self.window, height=100, width=100, bg=THEME_COLOR[0], highlightthickness=0)
        self.watermark_canvas.grid(column=0, row=3, pady=10)
        try:
            watermark = self.data.reading_data("watermark")
            pil_image = Image.open(watermark).resize((100, 100))
            watermark = ImageTk.PhotoImage(pil_image)
            self.watermark_canvas.create_image(50, 50, image=watermark)
        except AttributeError:
            pass

        self.image_canvas = Canvas(self.window, height=330, width=450, bg=THEME_COLOR[0], highlightthickness=0)
        self.image_canvas.grid(column=1, row=1,columnspan=5, rowspan=3, pady=20, padx=20)
        try:
            image = self.data.reading_data("images")[0]
            pil_image = Image.open(image).resize((330, 450))
            image = ImageTk.PhotoImage(pil_image)
            self.image_canvas.create_image(225, 165, image=image)
        except IndexError:
            pass
        except AttributeError:
            pass

        self.position = IntVar()
        self.top_left = Radiobutton(text="Top Left Corner", bd=0, activebackground=THEME_COLOR[0], value=1,
                                    highlightthickness=0, command=self.set_position, variable=self.position)
        self.top_right = Radiobutton(text="Top Right Corner", bd=0, activebackground=THEME_COLOR[0], value=2,
                                     highlightthickness=0, command=self.set_position, variable=self.position)
        self.center = Radiobutton(text="Center", bd=0, activebackground=THEME_COLOR[0], value=3,
                                  highlightthickness=0, command=self.set_position, variable=self.position)
        self.bot_left = Radiobutton(text="Bottom Left Corner", bd=0, activebackground=THEME_COLOR[0], value=4,
                                    highlightthickness=0, command=self.set_position, variable=self.position)
        self.bot_right = Radiobutton(text="Bottom Right Corner", bd=0, activebackground=THEME_COLOR[0], value=5,
                                     highlightthickness=0, command=self.set_position, variable=self.position)
        self.top_left.grid(column=1, row=4, padx=10, pady=10)
        self.top_right.grid(column=2, row=4, padx=10, pady=10)
        self.center.grid(column=3, row=4, padx=10, pady=10)
        self.bot_left.grid(column=4, row=4, padx=10, pady=10)
        self.bot_right.grid(column=5, row=4, padx=10, pady=10)

        self.opacity = Scale(from_=100, to=0, command=self.set_opacity, label="Opacity")
        self.opacity.grid(column=0, row=4, padx=50, pady=10)

        self.insert_water = Button(text="Insert watermark 💧", bd=0, activebackground=THEME_COLOR[0],
                                   highlightthickness=0, command=self.insert_water_button)
        self.insert_water.grid(column=6, row=1, padx=20, pady=20)

        self.window.mainloop()

    def load_images(self):
        """Load images to watermark into a list and saves it into .json file."""

        files_path = filedialog.askopenfiles(title="Select your images to watermark")
        images = self.image_process.process_images(files_path)
        print(images)
        if not images:
            messagebox.showerror(title="Error", message="You must select at least one image to insert a watermark to.")
        else:
            self.preview_image()

    def load_watermark(self):
        """Loads watermark and returns a path location string."""

        file_path = filedialog.askopenfile(title="Select your watermark")
        if not file_path and not self.data.reading_data("watermark"):
            messagebox.showerror(title="Error", message="You must select an image file to use as watermark")

        elif not file_path:
            pass

        elif file_path.name[-3:] != "png":
            messagebox.showerror(title="Error", message="Your watermark should be in PNG format in order to work.")
        else:
            save_path = {
                "watermark": file_path.name
            }
            self.data.save_data(save_path)
            self.preview_watermark()
            return file_path.name

    def insert_water_button(self):
        watermark_path = self.data.reading_data("watermark")
        if not watermark_path:
            watermark_path = self.load_watermark()
        elif not watermark_path or not self.data.reading_data("images"):
            messagebox.showerror(title="Error",
                                 message="You must select an image and watermark files to insert a watermark")
        processed = self.image_process.insert_watermark(watermark_path)
        if processed:
            self.preview_image()

    def set_position(self):
        position = {
            "position": self.position.get()
        }

        self.data.save_data(position)

    def set_opacity(self, value):
        opac = int((int(value) / 100) * 255)
        opacity = {
            "opacity": opac
        }
        self.data.save_data(opacity)

    def preview_watermark(self):
        self.watermark_canvas = Canvas(self.window, height=100, width=100, bg=THEME_COLOR[0], highlightthickness=0)
        self.watermark_canvas.grid(column=0, row=3, pady=10)
        watermark = ImageTk.PhotoImage(Image.open(self.data.reading_data("watermark")).resize((100, 100)))
        self.watermark_canvas.create_image(50, 50, image=watermark)
        self.watermark_canvas.mainloop()

    def preview_image(self):
        self.image_canvas = Canvas(self.window, height=330, width=450, bg=THEME_COLOR[0], highlightthickness=0)
        self.image_canvas.grid(column=1, row=1, columnspan=5, rowspan=3, pady=20, padx=20)
        image = self.data.reading_data("images")
        if type(image) == list:
            image = image[0]
        if image:
            pil_image = Image.open(image).resize((330, 450))
            image = ImageTk.PhotoImage(pil_image)
            self.image_canvas.create_image(225, 165, image=image)
            self.image_canvas.mainloop()




