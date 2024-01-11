from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
import requests

apiURI = "http://localhost:8000/"


def convert_to_tuple(lst):
    return tuple(lst)


class DBConnect:
    def __init__(self, suffix):
        self.suffix = suffix

    def getData(self):
        print(requests.get(apiURI + self.suffix).json())
        return requests.get(apiURI + self.suffix).json()


class ItemsTable(Screen):
    def load_table(self):
        itemCon = DBConnect("items")
        itemData = itemCon.getData()
        itemData = itemData.get("items", [])

        itemData = [convert_to_tuple(item) for item in itemData]

        print(itemData)

        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("ID", dp(30)),
                ("Name", dp(30)),
                ("Supplier ID", dp(30)),
                ("Shelf ID", dp(30)),
                ("Buying Price", dp(30)),
                ("Selling Price", dp(30)),
            ],
            row_data=itemData,
        )
        self.add_widget(self.data_tables)
        return layout

    def switch_home(self):
        self.manager.current = "HomePage"

    def reload(self):
        self.load_table()

    def on_enter(self):
        self.load_table()


class ShelvesTable(Screen):
    def load_table(self):
        shelvesCon = DBConnect("shelves")
        shelveData = shelvesCon.getData()
        shelveData = shelveData.get("shelves", [])

        shelveData = [convert_to_tuple(shelve) for shelve in shelveData]
        print(shelveData)

        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("ID", dp(70)),
                ("Location Code", dp(70)),
                ("Location ID", dp(70)),
            ],
            row_data=shelveData,
        )
        self.add_widget(self.data_tables)
        return layout

    def switch_home(self):
        self.manager.current = "HomePage"

    def reload(self):
        self.load_table()

    def on_enter(self):
        self.load_table()


class SuppliersTable(Screen):
    def load_table(self):
        suppliersCon = DBConnect("suppliers")
        suppliersData = suppliersCon.getData()
        suppliersData = suppliersData.get("suppliers", [])

        suppliersData = [convert_to_tuple(supplier) for supplier in suppliersData]

        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("ID", dp(70)),
                ("name", dp(70)),
                ("city", dp(70)),
            ],
            row_data=suppliersData,
        )
        self.add_widget(self.data_tables)
        return layout

    def switch_home(self):
        self.manager.current = "HomePage"

    def reload(self):
        self.load_table()

    def on_enter(self):
        self.load_table()


class WarehousesTable(Screen):
    def load_table(self):
        warehousesCon = DBConnect("warehouses")
        warehousesData = warehousesCon.getData()
        warehousesData = warehousesData.get("warehouses", [])

        warehousesData = [convert_to_tuple(warehouse) for warehouse in warehousesData]

        layout = AnchorLayout()
        self.data_tables = MDDataTable(
            pos_hint={'center_y': 0.5, 'center_x': 0.5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("ID", dp(70)),
                ("ZIP Code", dp(70)),
                ("Address", dp(70)),
            ],
            row_data=warehousesData,
        )
        self.add_widget(self.data_tables)
        return layout

    def switch_home(self):
        self.manager.current = "HomePage"

    def reload(self):
        self.load_table()

    def on_enter(self):
        self.load_table()


sm = ScreenManager()


class HomePage(Screen):

    def switch_items(self):
        self.manager.current = "ItemsTable"

    def switch_shelves(self):
        self.manager.current = "ShelvesTable"

    def switch_suppliers(self):
        self.manager.current = "SuppliersTable"

    def switch_warehouses(self):
        self.manager.current = "WarehousesTable"


class MainWindow(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.title = "Warehouse"
        Window.size = (1065, 670)
        return Builder.load_file("warehouse.kv")


if __name__ == "__main__":
    MainWindow().run()
