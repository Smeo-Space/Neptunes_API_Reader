import sys, random
from PySide6 import QtCore, QtGui, QtWidgets

# === Star-related classes ===

class StarItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, x, y, size, name):
        super().__init__(-size / 2, -size / 2, size, size)
        self.setPos(x, y)
        self.name = name

        color = QtGui.QColor.fromHsv(
            200 + random.randint(-20, 20),
            30 + random.randint(0, 60),
            255 - random.randint(0, 60),
        )
        self.setBrush(QtGui.QBrush(color))
        self.setPen(QtCore.Qt.PenStyle.NoPen)

        # Label
        self.label = QtWidgets.QGraphicsSimpleTextItem(name, self)
        self.label.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))
        self.label.setPos(size, -size)
        self.label.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)
        self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)

    def mousePressEvent(self, event):
        print(f"Clicked {self.name}")
        super().mousePressEvent(event)


class StarMapScene(QtWidgets.QGraphicsScene):
    def __init__(self, star_count=500):
        super().__init__()
        self.setSceneRect(-2000, -2000, 4000, 4000)
        self.stars = []
        self.load_stars(star_count)

    def load_stars(self, star_count):
        for i in range(star_count):
            x, y = random.uniform(-1800, 1800), random.uniform(-1800, 1800)
            size = random.uniform(1.0, 3.0)
            star = StarItem(x, y, size, f"Star {i}")
            self.addItem(star)
            self.stars.append(star)

    def update_stars(self, star_data):
        """Generic update method: clears and adds new stars"""
        for star in self.stars:
            self.removeItem(star)
        self.stars.clear()
        for i, (x, y, size, name) in enumerate(star_data):
            star = StarItem(x, y, size, name)
            self.addItem(star)
            self.stars.append(star)


class StarMapView(QtWidgets.QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        self.setBackgroundBrush(QtCore.Qt.GlobalColor.black)
        self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
        self.scale_factor = 1.0

    def wheelEvent(self, event):
        zoom_in = 1.15
        zoom_out = 1 / zoom_in
        zoom = zoom_in if event.angleDelta().y() > 0 else zoom_out
        self.scale(zoom, zoom)
        self.scale_factor *= zoom


# === Main window ===

class CanvasWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Star Map Manager")
        self.resize(1200, 800)

        # Central widget + layout
        central = QtWidgets.QWidget()
        self.setCentralWidget(central)
        layout = QtWidgets.QHBoxLayout(central)

        # Left panel
        left_panel = QtWidgets.QFrame()
        left_panel.setFixedWidth(250)
        left_panel.setStyleSheet("background-color: #202020; color: white;")
        left_layout = QtWidgets.QVBoxLayout(left_panel)

        title = QtWidgets.QLabel("Controls")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        left_layout.addWidget(title)
        self.zoom_btn = QtWidgets.QPushButton("Zoom to center")
        self.grid_btn = QtWidgets.QPushButton("Toggle grid")
        left_layout.addWidget(self.zoom_btn)
        left_layout.addWidget(self.grid_btn)
        left_layout.addStretch()

        # Right panel: starmap
        map_frame = QtWidgets.QFrame()
        map_frame.setFrameShape(QtWidgets.QFrame.Shape.Box)
        map_layout = QtWidgets.QVBoxLayout(map_frame)

        self.scene = StarMapScene(1000)
        self.starmap = StarMapView()
        self.starmap.setScene(self.scene)
        map_layout.addWidget(self.starmap)

        # Add panels to layout
        layout.addWidget(left_panel)
        layout.addWidget(map_frame, 1)

    def load_map(self, star_data):
        """Update the starmap with new star positions"""
        self.scene.update_stars(star_data)


# === Window manager ===

class WindowManager:
    def __init__(self):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = CanvasWindow()

    def load(self):
        self.window.show()

    def update_map(self, stars):
        self.window.load_map(stars)

    def app_exec(self):
        self.app.exec()

    def app_exit(self):
        sys.exit()
