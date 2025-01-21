import asyncio
import io
import sys
import folium
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView
from Model import Model
from Filter import Filter

class CafeFinder:
    def __init__(self):        
        self.app = QtWidgets.QApplication(sys.argv)
        
        self.data = Model()
        self.location = asyncio.run(self.data.get_location())
        
        self.webview = QWebEngineView()
        self.webview.page().setZoomFactor(1.75)
        self.webview.resize(1500, 1000)

        self.type_field = Filter('Gaststätte', ['Cafe', 'Restaurant', 'Fast Food', 'Bar', 'Biergarten'])
        self.diet_field = Filter('Ernährung', ['Halal', "Koscher", 'Vegetarisch', 'Vegan'])
        self.payment_field = Filter('Zahlungsmöglichkeit', ['Bargeld', 'Karte'])
        
        self.control_layout = QtWidgets.QVBoxLayout()
        self.control_widget = QtWidgets.QWidget()
        self.control_widget.setLayout(self.control_layout)
        
        self.control_layout.addWidget(self.type_field)
        self.control_layout.addWidget(self.diet_field)
        self.control_layout.addWidget(self.payment_field)
        
        self.main_layout = QtWidgets.QHBoxLayout()
        self.container = QtWidgets.QWidget()
        self.container.setLayout(self.main_layout)
        
        self.main_layout.addWidget(self.webview)
        self.main_layout.addWidget(self.control_widget)
        
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setCentralWidget(self.container)
        self.main_window.resize(2000, 1000)
        self.main_window.setWindowTitle("Cafe Finder")

        self.type_field.state_changed.connect(self.on_checkbox_state_changed)
        self.diet_field.state_changed.connect(self.on_checkbox_state_changed)
        self.payment_field.state_changed.connect(self.on_checkbox_state_changed)
        
        for checkbox in self.type_field.checkboxes:
            checkbox.setChecked(True)
        self.check_all_checkboxes()
        
    def on_checkbox_state_changed(self, text, checked):
        self.check_all_checkboxes()
        
    def check_all_checkboxes(self):
        type_status = self.type_field.get_checked_status()
        diet_status = self.diet_field.get_checked_status()
        payment_status = self.payment_field.get_checked_status()
        self.data.build_json(self.location, type_status.items(), diet_status.items(), payment_status.items())
        asyncio.run(self.refresh_map())
        
    @staticmethod
    def mark_cafes(cafes, m):
        if (cafes != None):
            for cafe in cafes:
                tags = cafe.get('tags', {})
                name = cafe.get('tags', {}).get('name', 'Unbekannter Name')
                folium.Marker(
                    location=[cafe.get('lat'), cafe.get('lon')],
                    tooltip=name,
                    popup=cafe.get('tags', {}).get('opening_hours', 'keine bekannte Öffnungszeiten')
                ).add_to(m)
            
    async def refresh_map(self):
        self.map = folium.Map(location=self.location, zoom_start=15)
            
        self.cafes = self.data.get_cafes()
        self.mark_cafes(self.cafes, self.map)
        folium.Marker(location=self.location, tooltip="Dein Standort", icon=folium.Icon(color="red")).add_to(self.map)

        self.data = io.BytesIO()
        self.map.save(self.data, close_file=False)
        
        self.webview.setHtml(self.data.getvalue().decode())
        self.webview.show()

        self.data = Model()

if __name__ == "__main__":
    view = CafeFinder()
    view.main_window.show()
    sys.exit(view.app.exec_())