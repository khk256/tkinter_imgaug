from tkinter import filedialog
from cv2 import imread
from cv2 import cvtColor
from cv2 import COLOR_BGR2RGB
import imgaug.augmenters as iaa
from matplotlib.pyplot import figure
from numpy import array
from tkinter import Frame
from tkinter import Button
from tkinter import Tk
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from zipfile import ZipFile
from io import BytesIO
from PIL.Image import fromarray

class Application(Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.select_image = Button(self)
        self.select_image["text"] = "이미지 선택"
        self.select_image["command"] = self.image_canvas
        self.select_image.pack(side = "bottom", fill = "both", expand = "yes", padx = "10", pady = "10")

        # self.image_download = Button(self)
        # self.image_download["text"] = "압축 다운로드"
        # self.image_download["command"] = self.image_zip
        # self.image_download.pack(side = "right", fill = "both", expand = "yes", padx = "10", pady = "10")

    def image_canvas(self):
        path = filedialog.askopenfilename()

        if len(path) > 0:
            # image = cv2.imread(path)
            image = imread(path)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cvtColor(image, COLOR_BGR2RGB)
            image = array([image])

            seq = iaa.Sequential([
                        iaa.Sometimes(
                            0.5,
                            iaa.GaussianBlur(sigma=(0, 0.5)),
                            iaa.Multiply((0.5, 1.5))
                        ),
                        iaa.Affine(
                        rotate=(0, 180)
                    )], random_order=True)

            fig = figure(figsize = (20., 20.), dpi = 50)

            grid = ImageGrid(fig, 111, nrows_ncols= (10, 3), axes_pad = 0.1)

            im_list = []

            for i in range(30):
                image = seq(images = image)
                im_list.append(image[0])
            for ax, im in zip(grid, im_list):
                ax.imshow(im)

            canvas = FigureCanvasTkAgg(fig, master = self)
            canvas.draw()
            canvas.get_tk_widget().pack()

    def image_zip(self, im_list):

        images = []
        for i, im in enumerate(im_list):
            im = fromarray(im)
            file_object = BytesIO()
            im.save(file_object, "PNG")
            im.close()
            # images[i].append(file_object)

        zip_file_bytes_io = BytesIO()

        with ZipFile(zip_file_bytes_io, 'w') as zip_file:
            for image_name, bytes_stream in images:
                zip_file.writestr(image_name + ".png", bytes_stream.getvalue())

        file_path = filedialog.asksaveasfilename()
        with open(file_path, 'wb') as file:
            file.write(ZipFile)

root = Tk()
app = Application(master = root)
app.mainloop()