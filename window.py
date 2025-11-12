import sys, random, json
from PySide6 import QtCore, QtGui, QtWidgets
from models import Star
import api,settings


SCALE = 100 # times x y vales by to get to screen size


# === Star-related classes ===

class StarItem(QtWidgets.QGraphicsEllipseItem):
	def __init__(self, star: Star):

		# Size
		size = 10
		x = star.x * SCALE
		y = star.y * SCALE

		# Star details
		name = star.name
		owning_player = star.owning_player()

		# Creating UI item
		super().__init__(-size / 2, -size / 2, size, size)
		self.setPos(x, y)
		self.name = name

		# Colour
		if owning_player is None:
			colour = settings.colour_key[0]
		else:
			colour = settings.colour_key[owning_player.colour + 1] # dont know if +1 is good or if its silly and i messued up the colour key
		self.setBrush(QtGui.QBrush(QtGui.QColor(*colour)))
		self.setPen(QtCore.Qt.PenStyle.NoPen)

		# Label
		self.label = QtWidgets.QGraphicsSimpleTextItem(name, self)
		self.label.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))
		self.label.setPos(0, size/2)
		self.label.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations)
		self.setFlag(QtWidgets.QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
		
		# Cutout
		s = size/3
		self.cutout = QtWidgets.QGraphicsEllipseItem(-s,-s,s*2,s*2, self)  # child item
		self.cutout.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.black))
		self.cutout.setPen(QtCore.Qt.PenStyle.NoPen)
		self.cutout.setPos(0, 0)

		# Dot
		s = size/6
		self.dot = QtWidgets.QGraphicsEllipseItem(-s,-s,s*2,s*2, self)  # child item
		self.dot.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))
		self.dot.setPen(QtCore.Qt.PenStyle.NoPen)
		self.dot.setPos(0, 0)

	def mousePressEvent(self, event):
		print(f"Clicked {self.name}")
		super().mousePressEvent(event)


class StarMapScene(QtWidgets.QGraphicsScene):
	def __init__(self):
		super().__init__()
		self.setSceneRect(-1000, -1000, 2000, 2000)
		# set visual border raround viwe
		border = QtWidgets.QGraphicsRectItem(self.sceneRect())
		border.setPen(QtGui.QPen(QtCore.Qt.GlobalColor.green, 2))
		self.addItem(border)

		self.area = QtWidgets.QGraphicsRectItem(-40,-40,80,80)
		self.area.setBrush(QtGui.QBrush(QtCore.Qt.GlobalColor.white))
		self.area.setPen(QtCore.Qt.PenStyle.NoPen)
		self.area.setPos(0,0)
		self.stars = []

	def update_stars(self, stars : dict[Star]):
		"""Generic update method: clears and adds new stars"""

		# Removes all stars from view
		for star in self.stars:
			self.removeItem(star)

		# Clears stars record
		self.stars.clear()

		# Replaces stars into view
		for _, star in stars.items():
			star_item = StarItem(star)
			self.addItem(star_item)
			self.stars.append(star_item)


class StarMapView(QtWidgets.QGraphicsView):
	def __init__(self):
		super().__init__()
		self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
		self.setBackgroundBrush(QtCore.Qt.GlobalColor.black)
		self.setDragMode(QtWidgets.QGraphicsView.DragMode.ScrollHandDrag)
		self.scale_factor = 1.0
		self.max_scale = 200
		self.is_labels_showing = None

	def wheelEvent(self, event):
		zoom = 1.15 if event.angleDelta().y() > 0 else (1/1.15)

		# current transform scale
		current_scale = self.transform().m11()
		new_scale = current_scale * zoom

		# optional: max zoom in limit
		if zoom > 1 and new_scale > self.max_scale:
			return

		# ==== Predict the visible scene rect after zoom ====
		visible_before = self.mapToScene(self.viewport().rect()).boundingRect()
		predicted_width = visible_before.width() / zoom
		predicted_height = visible_before.height() / zoom

		scene_full = self.scene().sceneRect()

		# ==== Check if the predicted zoom-out would exceed scene ====
		if zoom < 1:	# zooming OUT
			if predicted_width >= scene_full.width() and predicted_height >= scene_full.height(): # TODO decide {and} or, {or}
				return	# do NOT apply zoom (block it cleanly)

		# Apply zoom (safe)
		self.scale(zoom, zoom)
		self.scale_factor = new_scale

		self.update_labels_visibility()

	# Toggles labels based on zoom level
	def update_labels_visibility(self):
		# Determines whether star labels should be shown
		show = self.scale_factor >= SCALE/40
		# Cancels if there is no scene
		if self.scene() is None:
			return

		if self.is_labels_showing == show:
			return

		for star in self.scene().stars:
			# Checks object is a StarItem
			if not isinstance(star, StarItem):
				continue

			# Updates visibility
			star.label.setVisible(show)

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
		left_panel.setMaximumWidth(250)
		left_panel.setMinimumWidth(200)
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

		self.scene = StarMapScene()
		self.starmap = StarMapView()
		self.starmap.setScene(self.scene)
		map_layout.addWidget(self.starmap)

		# Add panels to layout
		layout.addWidget(left_panel)
		layout.addWidget(map_frame, 1)

	def load_map(self, stars : dict[Star]):
		"""Update the starmap with new star positions"""
		self.scene.update_stars(stars)


# === Window manager ===

class WindowManager:
	def __init__(self):
		self.app = QtWidgets.QApplication(sys.argv)
		self.window = CanvasWindow()

	def load(self):
		self.window.show()

	def update_map(self, stars : dict[Star]):
		self.window.load_map(stars)

	def app_exec(self):
		self.app.exec()

	def app_exit(self):
		sys.exit()
