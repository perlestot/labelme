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
        self.setWindowTitle("Window Level/Window Width")

        self.slider_window_level = self._create_slider_WL()
        self.slider_window_width = self._create_slider_WW()

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Window Level"), self.slider_window_level)
        formLayout.addRow(self.tr("Window Width"), self.slider_window_width)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def onNewValue(self, value):
        window_level = self.slider_window_level.value()
        window_width = self.slider_window_width.value()
        print('Window Level:', window_level)
        print('Window Width:', window_width)

        img = self.img
        img = np.asarray(img)

        low = window_level - window_width/2
        high = window_level + window_width/2
        img = change_window(img, low, high)
        # img = self.img
        # img = PIL.ImageEnhance.Brightness(img).enhance(brightness)
        # img = PIL.ImageEnhance.Contrast(img).enhance(contrast)

        img = Image.fromarray(img)

        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_slider_WL(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, 4000)
        slider.setValue(2000)
        slider.setTickInterval(100)
        slider.setSingleStep(100)
        slider.valueChanged.connect(self.onNewValue)
        return slider

    def _create_slider_WW(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, 2000)
        slider.setValue(1000)
        slider.setTickInterval(100)
        slider.setSingleStep(100)
        slider.valueChanged.connect(self.onNewValue)
        return slider


def change_window(img, low, high):
    img = (img.clip(min=low, max=high) - low) / (high - low) * 255
    return img.astype(np.uint8)