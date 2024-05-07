from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QIcon, QPixmap
import sys


class Window(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(400, 400, 700, 1000)
        self.setWindowTitle("LIKE OR FUCK")
        self.setWindowIcon(QIcon('pq.png'))

        self.image_index = 0
        self.images = ["picture.jpg"]

        layout = QGridLayout(self)
        self.setLayout(layout)

        label = QLabel(self)
        pixmap = QPixmap('picture.jpg')
        label.setPixmap(pixmap)

        layout.addWidget(label, 2, 0, 1, 2)

        noBtn = QPushButton("👎🏻", self)
        noBtn.setFixedSize(100, 60)
        layout.addWidget(noBtn, 1, 0)

        coolBtn = QPushButton("👍🏻", self)
        coolBtn.setFixedSize(100, 60)
        layout.addWidget(coolBtn, 1, 1)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
