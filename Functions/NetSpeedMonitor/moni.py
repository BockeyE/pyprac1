from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QColor, QFont, QPalette
from PyQt5.QtCore import Qt, QThread
import sys, psutil, time


class SystemInfoThread(QThread):

    def __init__(self, window):
        super(SystemInfoThread, self).__init__()
        self.__win = window

    def run(self):
        old_net_speed = psutil.net_io_counters().bytes_recv
        while True:
            new_net_speed = psutil.net_io_counters().bytes_recv
            time.sleep(1)
            self.__win.net_label.setText("%.2fK/s" % ((new_net_speed - old_net_speed) / 1024))
            old_net_speed = new_net_speed


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAutoFillBackground(False)

        layout = QHBoxLayout(self)
        self.setLayout(layout)

        self.mem_label = QLabel()
        self.net_label = QLabel()

        layout.addWidget(self.mem_label)
        layout.addWidget(self.net_label)

        layout.setSpacing(0)

        pal = QPalette()
        pal.setColor(QPalette.WindowText, Qt.white)

        self.mem_label.setMinimumWidth(60)
        self.mem_label.setAlignment(Qt.AlignHCenter)

        pal.setColor(QPalette.Window, Qt.green)
        self.mem_label.setAutoFillBackground(True)
        self.mem_label.setPalette(pal)

        self.net_label.setMinimumWidth(100)
        self.net_label.setAlignment(Qt.AlignHCenter)
        pal.setColor(QPalette.Window, Qt.red)
        self.net_label.setAutoFillBackground(True)
        self.net_label.setPalette(pal)

        font = QFont("微软雅黑", 10)
        self.mem_label.setFont(font)
        self.net_label.setFont(font)

        self.mem_label.setText("0%")
        self.net_label.setText("0K/s")

        self.__x_offset = 0
        self.__y_offset = 0

    def mousePressEvent(self, event):
        self.__x_offset = event.globalX() - self.pos().x()
        self.__y_offset = event.globalY() - self.pos().y()

    def mouseMoveEvent(self, event):
        self.move(event.globalX() - self.__x_offset, event.globalY() - self.__y_offset)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys_info_thread = SystemInfoThread(win)
    sys_info_thread.start()
    sys.exit(app.exec())