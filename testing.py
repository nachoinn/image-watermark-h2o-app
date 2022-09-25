# from PIL import Image
#
# im1 = Image.open("images/test.jpg")
#
# with Image.open("images/logo svd.png") as im2:
#     im3 = im2.copy()
#     im3.putalpha(80)
#     im2.paste(im3, im2)
#     im2.save("images/logo svd trans.png")
#
# im2 = Image.open("images/logo svd trans.png")
#
# im1.paste(im2, (im1.width-im2.width, 0), mask=im2)
# im1.save("watermark images/finaltest.jpg")
#
# att = dir(im1)
# print(att)
#
# print(im2.mode)
# print(im1.info)
# ---------------------------------------------------------------
# import json
#
# with open("data.json", "w") as jason:
#     docs = {
#         "images": {
#             "img_list": []
#         },
#         "watermark": "",
#         "transparency": 255,
#         "position": "Center"
#     }
#     json.dump(docs, jason, indent=4)
#


# with open("data.json", "r") as data:
#     pepe = {
#         "watermark": "pepe"
#     }
#     xoxo = json.load(data)
#     print(xoxo)
#     xoxo.update(pepe)
#     print(xoxo)
#
# with open("data.json", "w") as new_json:
#     json.dump(xoxo, new_json, indent=4)

#----------------------------------------------------------
from tkinter import *
from PIL import Image, ImageTk
from data import DataManager
data = DataManager()

root = Tk()
root.geometry('1000x1000')
canvas = Canvas(root,width=999,height=999)
canvas.pack()
pilImage = Image.open(data.reading_data("watermark")).resize((100,100))
image = ImageTk.PhotoImage(pilImage)
imagesprite = canvas.create_image(100,100,image=image)
root.mainloop()