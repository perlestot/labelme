import PIL.Image
import PIL.ImageEnhance
from qtpy.QtCore import Qt
from qtpy import QtGui
from qtpy import QtWidgets

from .. import utils
import numpy as np
from PIL import Image


class BrightnessContrastDialog(QtWidgets.QDialog):
    def __init__(self, img, callback, parent=None):
        super(BrightnessContrastDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Window_Level/Window_Width")

        self.slider_window = self._create_slider()
        self.slider_window_size = self._create_slider()

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Window"), self.slider_window)
        formLayout.addRow(self.tr("Window size"), self.slider_window_size)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def onNewValue(self, value):
        window = self.slider_window.value() / 50.0
        window_size = self.slider_window_size.value() / 50.0
        print('window:', window)
        print('window size:', window_size)

        img = self.img
        img = np.asarray(img)

        low = (window - window_size/2) * 1000
        high = (window + window_size/2 * 1000
        img = change_window(img, low, high)
        # img = self.img
        # img = PIL.ImageEnhance.Brightness(img).enhance(brightness)
        # img = PIL.ImageEnhance.Contrast(img).enhance(contrast)

        img = Image.fromarray(img)

        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_slider(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, 150)
        slider.setValue(50)
        slider.valueChanged.connect(self.onNewValue)
        return slider


def change_window(img, low, high):
    MAX = 2**16 - 1
    low = 1000
    high = 3000
    img = (img.clip(min=low, max=high) - low) / (high - low) * MAX
    return img.astype(np.uint16)
