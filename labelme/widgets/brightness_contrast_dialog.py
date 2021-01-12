import PIL.Image
import PIL.ImageEnhance
from qtpy.QtCore import Qt
from qtpy import QtGui
from qtpy import QtWidgets, QtCore
from qtpy.QtWidgets import QCheckBox

from .. import utils
import numpy as np
from PIL import Image

n_STEP = 80 # total step interval for slider

class BrightnessContrastDialog(QtWidgets.QDialog):
    def __init__(self, img, callback, parent=None):
        super(BrightnessContrastDialog, self).__init__(parent)
        self.setModal(True)
        self.setWindowTitle("Window Level/Window Width")

        # Assign parameter of slider
        img_array = np.asarray(img)
        self.max_val = int(img_array.max())
        self.step_size_wl = int(self.max_val / n_STEP)
        self.step_size_ww = int(self.max_val / n_STEP)
        self.wl_range = n_STEP #int(max_val / self.step_size_wl)
        self.ww_range = n_STEP #int(max_val / self.step_size_ww)

        # Create slider
        self.slider_window_level = self._create_slider_WL()
        self.slider_window_width = self._create_slider_WW()
        self.box_invert = self._create_box_invert()

        self.box_invert.stateChanged.connect(self.clickBox)

        formLayout = QtWidgets.QFormLayout()
        formLayout.addRow(self.tr("Window Level"), self.slider_window_level)
        formLayout.addRow(self.tr("Window Width"), self.slider_window_width)
        formLayout.addRow(self.tr("Invert"), self.box_invert)
        self.setLayout(formLayout)

        assert isinstance(img, PIL.Image.Image)
        self.img = img
        self.callback = callback

    def onNewValue(self, value):
        window_level = self.slider_window_level.value() * self.step_size_wl # Change to real value
        window_width = self.slider_window_width.value() * self.step_size_ww # Change to real value
        print('Window Level:', window_level)
        print('Window Width:', window_width)

        img = self.img
        img = np.asarray(img)
        
        # https://www.tutorialspoint.com/pyqt/pyqt_qcheckbox_widget.htm
        print('ClickBox', self.box_invert.isChecked())

        low = window_level - window_width/2
        high = window_level + window_width/2
        img = change_window(img, low, high)

        if self.box_invert.isChecked():
            img = np.max(img) - img
            
        # img = self.img
        # img = PIL.ImageEnhance.Brightness(img).enhance(brightness)
        # img = PIL.ImageEnhance.Contrast(img).enhance(contrast)

        img = Image.fromarray(img)

        img_data = utils.img_pil_to_data(img)
        qimage = QtGui.QImage.fromData(img_data)
        self.callback(qimage)

    def _create_slider_WL(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, self.wl_range)
        slider.setValue(int(self.max_val/2)/self.step_size_wl) # default value
        # https://www.tutorialspoint.com/pyqt/pyqt_qslider_widget_signal.htm
        # slider.setTickInterval(15)
        # slider.setSingleStep(1) # arrow-key step-size
        # slider.setPageStep(1) # mouse-wheel/page-key step-size  
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow) 
        slider.valueChanged.connect(self.onNewValue)
        return slider

    def _create_slider_WW(self):
        slider = QtWidgets.QSlider(Qt.Horizontal)
        slider.setRange(0, self.ww_range)
        slider.setValue(int(self.max_val/self.step_size_ww)) # default value
        # slider.setTickInterval(15)
        # slider.setSingleStep(1) # arrow-key step-size
        # slider.setPageStep(1) # mouse-wheel/page-key step-size  
        slider.setTickPosition(QtWidgets.QSlider.TicksBelow)    
        slider.valueChanged.connect(self.onNewValue)
        return slider

    def _create_box_invert(self):
        # https://pythonprogramminglanguage.com/pyqt-checkbox/
        box = QCheckBox("",self)
        return box

    def clickBox(self, state):

        if state == QtCore.Qt.Checked:
            print('Invert Checked')
            return True
        else:
            print('Invert Unchecked')
            return False


def change_window(img, low, high):
    img = (img.clip(min=low, max=high) - low) / (high - low) * 255
    return img.astype(np.uint8)

def change_window_from_bytes(img, low=None, high=None, invert=False):
    img = utils.img_data_to_pil(img)
    return change_window_from_pil(img, low, high, invert)

def change_window_from_pil(img, low, high, invert):
    img = np.asarray(img)

    if low is None:
        low = img.min()
    if high is None:
        high = img.max()
    img = change_window(img, low, high)

    if invert:
        img = np.max(img) - img

    img = Image.fromarray(img)
    img = utils.img_pil_to_data(img)
    return img