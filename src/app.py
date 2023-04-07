import json
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QMainWindow, QTreeView, QVBoxLayout, QWidget, QFileDialog

# Create a PySide6 application and window
app = QApplication([])
window = QMainWindow()
window.setWindowTitle("JSON Viewer")
widget = QWidget()
layout = QVBoxLayout(widget)

# Create a QStandardItemModel and set the column count to 1
model = QStandardItemModel()
model.setColumnCount(1)


# Recursive function to create items from JSON data
def add_items(data, parent):
    for key, value in data.items():
        item = QStandardItem(str(key))
        parent.appendRow(item)
        if isinstance(value, dict):
            add_items(value, item)
        elif isinstance(value, list):
            for item_data in value:
                child_item = QStandardItem()
                add_items(item_data, child_item)
                item.appendRow(child_item)
        else:
            child_item = QStandardItem(str(value))
            item.appendRow(child_item)


# Function to open a JSON file and display its contents
def open_json_file():
    # Show the file dialog and get the selected file path
    file_path, _ = QFileDialog.getOpenFileName(window, "Open JSON File", "", "JSON Files (*.json)")
    if file_path:
        # Load data from JSON file
        with open(file_path, "r") as f:
            data = json.load(f)

        # Clear the existing model and add items to the model
        model.clear()
        add_items(data, model)

        # Expand all items in the tree
        tree_view.expandAll()


# Create a "Open" action in the File menu
file_menu = window.menuBar().addMenu("File")
open_action = file_menu.addAction("Open")
open_action.triggered.connect(open_json_file)

# Create a QTreeView and set the model
tree_view = QTreeView()
tree_view.setModel(model)

# Add the QTreeView to the layout and set the layout for the widget
layout.addWidget(tree_view)
widget.setLayout(layout)

# Set the central widget of the window and show the window
window.setCentralWidget(widget)
window.show()
app.exec_()
