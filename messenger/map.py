import os
import sys
import requests
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 450

class MapViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.coordinates = [37.618423, 55.751244]  # Москва
        self.scale = 10
        self.map_style = 'map'
        self.marker_coordinates = self.coordinates.copy()
        self.found_address = ""
        self.setup_ui()
        self.update_map_image()

    def fetch_map_image(self):
        map_url = (f"http://static-maps.yandex.ru/1.x/?ll={self.coordinates[0]},{self.coordinates[1]}&z={self.scale}"
                   f"&size={SCREEN_WIDTH},{SCREEN_HEIGHT}&l={self.map_style}&pt={self.marker_coordinates[0]},{self.marker_coordinates[1]},pm2rdm")
        print("Fetching map image from:", map_url)
        response = requests.get(map_url)

        if not response.ok:
            print('Error fetching map image:')
            print("HTTP status:", response.status_code, "(", response.reason, ")")
            return None

        self.map_file = "map.png"
        with open(self.map_file, "wb") as file:
            file.write(response.content)
        print("Map image saved as:", self.map_file)
        return self.map_file

    def setup_ui(self):
        self.setGeometry(100, 100, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.setWindowTitle('Map Viewer')

        self.image_label = QLabel(self)
        self.pixmap = QPixmap()
        self.image_label.setPixmap(self.pixmap)

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter search query...")

        self.search_button = QPushButton("Search", self)
        self.search_button.clicked.connect(self.search_object)

        self.reset_button = QPushButton("Reset Search Result", self)
        self.reset_button.clicked.connect(self.reset_search_result)

        self.address_label = QLabel(self)
        self.address_label.setText("Address: ")

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.search_input)
        layout.addWidget(self.search_button)
        layout.addWidget(self.reset_button)
        layout.addWidget(self.address_label)
        self.setLayout(layout)

    def search_object(self):
        query = self.search_input.text()
        if not query:
            print("Search query cannot be empty.")
            return

        search_url = f"https://geocode-maps.yandex.ru/1.x/?apikey=8013b162-6b42-4997-9691-77b7074026e0&geocode={query}&format=json"
        response = requests.get(search_url)

        if response.ok:
            json_response = response.json()
            try:
                coords = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split()
                self.marker_coordinates = [float(coords[0]), float(coords[1])]
                self.coordinates = self.marker_coordinates.copy()

                self.found_address = json_response['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['name']
                self.address_label.setText(f"Address: {self.found_address}")

                self.update_map_image()
            except IndexError:
                print("Object not found.")
                self.address_label.setText("Address: Object not found.")
        else:
            print("Error performing search request.")
            print("HTTP status:", response.status_code)

    def update_map_image(self):
        if self.fetch_map_image() is not None:
            self.pixmap = QPixmap(self.map_file)
            self.image_label.setPixmap(self.pixmap)

    def reset_search_result(self):
        self.coordinates = [37.618423, 55.751244]  
        self.marker_coordinates = self.coordinates.copy()
        self.found_address = ""
        self.address_label.setText("Address: ")
        self.update_map_image() 
        self.search_input.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    viewer = MapViewer()
    viewer.show()
    sys.exit(app.exec())
