import sys
from PySide6 import QtCore, QtWidgets, QtGui


class CanvasWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("2D Canvas Example")
        self.setGeometry(100, 100, 600, 400)

        # Create a QGraphicsScene (the drawing area)
        self.scene = QtWidgets.QGraphicsScene()
        self.scene.setSceneRect(0, 0, 600, 400)

        # Create a QGraphicsView to display the scene
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Add some test items
        self.add_example_items()

    def add_example_items(self):
        # Create a red circle
        pen = QtGui.QPen(QtCore.Qt.GlobalColor.black)
        brush = QtGui.QBrush(QtCore.Qt.GlobalColor.red)
        circle = QtWidgets.QGraphicsEllipseItem(100, 100, 80, 80)
        circle.setPen(pen)
        circle.setBrush(brush)
        self.scene.addItem(circle)

        # Create a blue rectangle
        brush2 = QtGui.QBrush(QtCore.Qt.GlobalColor.blue)
        rect = QtWidgets.QGraphicsRectItem(250, 120, 100, 60)
        rect.setPen(pen)
        rect.setBrush(brush2)
        self.scene.addItem(rect)

class WindowManager:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = CanvasWindow()
        sys.exit(self.app.exec_())
    def load():
        self.window.show()

