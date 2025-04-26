import pandas as pd

class Laptops:
    def __init__(self, RAM:int, CPU_model:str, screen:str, brand:str, HDS:str, model_name:str, model_year:str, processor:str, graphic:str, price:str, condition:str, seller:str, graphic_card: str):
        self.RAM = RAM
        self.CPU_model = CPU_model
        self.screen = screen
        self.brand = brand
        self.HDS = HDS
        self.model_name = model_name
        self.model_year = model_year
        self.processor = processor
        self.graphics = graphic
        self.price = price
        self.condition = condition
        self.seller = seller
        self.graphic_card = graphic_card

    def __str__(self):
        return f"Laptops(RAM='{self.RAM}', CPU_model = '{self.CPU_model}', screen = '{self.screen}', brand = '{self.brand}', HDS= '{self.HDS}', model_name = '{self.model_name}', model_year = '{self.model_year}', processor = '{self.processor}', graphics = '{self.graphics}', price = '{self.price}', condition = '{self.condition}', seller = '{self.seller}', graphic_card = '{self.graphic_card}')"


lap_tops = [
    Laptops(16, "intel", "15.6", "Dell", "512", "inspiron 15", "None", "Intel i5, 4.6G Hz", "Intel® Iris® Xe Graphics", "609,00", "New", "Dell", "Integrated"),
    Laptops(32, "Intel I7", "16", "Apple", "512", "MacBook Pro", "2019", "Intel I7, 2.6 GHz", "‎AMD Radeon Pro 5300M", "531,89", "Refurbished", "Amazon", "None"),
    Laptops(16, "intel I5", "14", "Dell", "512", "Inspiron 14", "None", "Intel I5 4.6 GHz","Intel® Iris® Xe Graphics", "647,77", "New", "Dell", "None"),
    Laptops(6, "Intel I5", "14", "Dell", "None", "Vostro 3460", "2010", "Itel I5, 3.2 GHz", "nVidia GeForce GT630M", "None", "None", "Dell", "Discrete"),
    Laptops(16, "Intel I5", "15.6", "Dell", "512", "Dell G Series 15 5530 Laptop", "None", "Intel I5, 2.4 GHz","NVIDIA GeForce RTX 3050", "822,25", "New", "Amazon", "Discrete")
]

import pandas as pd

# Your Laptops class and lap_tops list here...

data = {}
for laptop in lap_tops:
    data[laptop.model_name] = {
        "RAM": laptop.RAM,
        "CPU_model": laptop.CPU_model,
        "screen": laptop.screen,
        "brand": laptop.brand,
        "HDS": laptop.HDS,
        "model_year": laptop.model_year,
        "processor": laptop.processor,
        "graphics": laptop.graphics,
        "price": laptop.price,
        "condition": laptop.condition,
        "seller": laptop.seller,
        "graphic_card": laptop.graphic_card
    }

df = pd.DataFrame(data).T
df.index.name = 'name_model'

# Select specific columns to display
columns_to_show = ['brand', 'model_name', 'RAM', 'CPU_model', 'price']
print(df[columns_to_show])



