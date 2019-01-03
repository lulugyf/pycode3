#coding=utf8
import random, sys
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import QLabel, QRubberBand, QApplication
from PyQt5.QtGui import QColor, QPixmap, QPainter, QPolygon

# 一个演示区域选择的样例,  准备用于截屏后选择区域

W, H = 800, 600

class Window(QLabel):
    def __init__(self, pixmap, parent=None):
        QLabel.__init__(self, parent)
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.pixmap = pixmap

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.origin = QPoint(event.pos())
            self.rubberBand.setGeometry(QRect(self.origin, QSize()))
            self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.rubberBand.hide()
            print(self.rubberBand.geometry())

    def resizeEvent(self, event):
        self.updateScreenshotLabel()
        # scaledSize = self.pixmap.size()
        # scaledSize.scale(self.screenshotLabel.size(), Qt.KeepAspectRatio)
        # if not self.screenshotLabel.pixmap() or scaledSize != self.screenshotLabel.pixmap().size():
        #     self.updateScreenshotLabel()

    def updateScreenshotLabel(self):
        self.setPixmap(self.pixmap.scaled(
                self.size(), Qt.KeepAspectRatio,
                Qt.SmoothTransformation))

def create_pixmap():
    screen = QApplication.primaryScreen()
    pixmap = screen.grabWindow(0)
    return pixmap

def create_pixmap1():
    def color():
        r = random.randrange(0, 255)
        g = random.randrange(0, 255)
        b = random.randrange(0, 255)
        return QColor(r, g, b)

    def point():
        return QPoint(random.randrange(0, W), random.randrange(0, H))

    pixmap = QPixmap(W, H)
    pixmap.fill(color())
    painter = QPainter()
    painter.begin(pixmap)
    i = 0
    while i < 100:
        painter.setBrush(color())
        painter.drawPolygon(QPolygon([point(), point(), point()]))
        i += 1

    painter.end()
    return pixmap


if __name__ == "__main__":
    app = QApplication(sys.argv)
    random.seed()

    window = Window(create_pixmap())
    #window.setPixmap(create_pixmap())
    window.resize(W, H)
    window.show()

    sys.exit(app.exec_())