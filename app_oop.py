from unicodedata import category
from PIL.ImageOps import expand
import customtkinter
import os
import json
from PIL import Image, ImageDraw, ImageOps
from phone_tree import AVLTree

class Product(customtkinter.CTkFrame):

    def button_purchase(self):
        print(f"Mua sản phẩm {self.product['name']} giá: ${self.product['price']}")
    
    def add_border_radius(self, image_path, radius):
        image = Image.open(image_path)
        mask = Image.new('L', image.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
        mask_draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
        result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
        result.putalpha(mask)
        return result

    def __init__(self, master, product):
        super().__init__(master=master, fg_color="black", corner_radius=10)
        self.product = product

        top_frame = customtkinter.CTkFrame(self, fg_color="black", corner_radius=10)
        top_frame.pack(expand=True, fill="both", pady=(10,0))

        bottom_frame = customtkinter.CTkFrame(self, fg_color="black", corner_radius=10)
        bottom_frame.pack(expand=True, fill="both", pady=(0,10))

        image_path = os.path.join("img", product["image"])
        # image = customtkinter.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(180, 180))
        pil_image = self.add_border_radius(image_path, radius=20)
        image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(180, 180))

        image_frame = customtkinter.CTkLabel(top_frame, image=image, text="")
        image_frame.pack(padx=15)

        info_frame = customtkinter.CTkFrame(bottom_frame, fg_color="black")
        info_frame.pack(pady=10)

        name = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 18, "bold"), text_color="darkorange", text=product["name"])
        name.pack()

        category_frame = customtkinter.CTkFrame(info_frame, fg_color="pink", corner_radius=15)
        category_frame.pack()
        category = customtkinter.CTkLabel(category_frame, font=customtkinter.CTkFont("Helvetica", 13, "bold"), text_color="black", text=product["category"])
        category.pack(anchor="center", padx=10)

        description = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 13, "normal"), text_color="white", text=product["description"])
        description.pack(pady=(5,0))

        price = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 14, "bold"), text_color="yellow", text=f"${product['price']}")
        price.pack()

        button = customtkinter.CTkButton(info_frame, fg_color="darkblue", text="Mua", command=self.button_purchase)
        button.pack(pady=(10,0))

class ScrollView(customtkinter.CTkScrollableFrame):
    def __init__(self, master, products):
        super().__init__(master=master)
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        for i in range(len(products)):
            product_frame = Product(self, products[i])
            product_frame.grid(row=i//4, column=i%4, sticky="nsew", padx=(0, 10) if i%4 != 3 else (0, 0), pady=(0, 10) if i//4 != (len(products)-1)//4 else (0, 0))


class Header(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master=master, fg_color="black", corner_radius=0)
        

        self.entry_min = customtkinter.CTkEntry(self, placeholder_text="Nhập giá thấp nhất")
        self.entry_min.pack(side="left", padx=(10, 0))
        self.entry_max = customtkinter.CTkEntry(self, placeholder_text="Nhập giá cao nhất")
        self.entry_max.pack(side="left", padx=(10, 0))
        
        search_button = customtkinter.CTkButton(self, fg_color="darkblue", text="Tìm", width=200, command=self.master.filter_products)
        search_button.pack(side="left", padx=(25,0))

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("light")

        self.title("Phone App")
        self.geometry("1100x800")
        self.resizable(False, False)

        self.products = self.get_data()

        self.avl_data = AVLTree()
        for product in self.products:
            self.avl_data.insert(product)

        self.header_frame = Header(self)
        self.header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)
        
        self.scrollable_frame = ScrollView(self, self.products)
        self.scrollable_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
    
    def get_data(self):
        products = []
        with open(os.path.join("data", "data.json"), "r", encoding="utf-8") as file:
            products = json.load(file)
        return products
    
    def filter_products(self):
        min_price = int(self.header_frame.entry_min.get())
        max_price = int(self.header_frame.entry_max.get())
        
        filtered_products = self.avl_data.find_phones(self.avl_data.root, min_price, max_price)
        self.scrollable_frame.destroy()
        self.scrollable_frame = ScrollView(self, filtered_products)
        self.scrollable_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)

app = App()
app.mainloop()