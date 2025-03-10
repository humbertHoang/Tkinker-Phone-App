from unicodedata import category
from PIL.ImageOps import expand
import customtkinter
import os
import json
from PIL import Image, ImageDraw, ImageOps
from phone_tree import AVLTree
app = customtkinter.CTk()

customtkinter.set_default_color_theme("dark-blue")
customtkinter.set_appearance_mode("light")

app.title("Phone App")
app.geometry("1100x800")
app.resizable(False, False)

def button_purchase(product):
    print(f"Mua sản phẩm {product['name']} giá: ${product['price']}")

def add_border_radius(image_path, radius):
    image = Image.open(image_path)
    mask = Image.new('L', image.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle([(0, 0), image.size], radius=radius, fill=255)
    result = ImageOps.fit(image, mask.size, centering=(0.5, 0.5))
    result.putalpha(mask)
    return result

def filter_products():
    min_price = int(entry_min.get())
    max_price = int(entry_max.get())
    
    filtered_products = avl_data.find_phones(avl_data.root, min_price, max_price)
    new_scrollable_frame = customtkinter.CTkScrollableFrame(app)
    new_scrollable_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
    new_scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
    
    for i in range(len(filtered_products)):
        row = i // 4
        col = i % 4
    
        is_last_row = row == (len(filtered_products)-1) // 4
        is_last_col = col == 3
    
        x_padding = (0, 0) if is_last_col else (0, 10)
        y_padding = (0, 0) if is_last_row else (0, 10)
        
        product_frame = customtkinter.CTkFrame(new_scrollable_frame, fg_color="black", corner_radius=10)
        product_frame.grid(row=row, column=col, sticky="nsew", padx=x_padding, pady=y_padding)

        top_frame = customtkinter.CTkFrame(product_frame, fg_color="black", corner_radius=10)
        top_frame.pack(expand=True, fill="both", pady=(10,0))

        bottom_frame = customtkinter.CTkFrame(product_frame, fg_color="black", corner_radius=10)
        bottom_frame.pack(expand=True, fill="both", pady=(0,10))

        image_path = os.path.join("img", products[i]["image"])
        # image = customtkinter.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(180, 180))
        pil_image = add_border_radius(image_path, radius=20)
        image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(180, 180))

        image_frame = customtkinter.CTkLabel(top_frame, image=image, text="")
        image_frame.pack(padx=15)

        info_frame = customtkinter.CTkFrame(bottom_frame, fg_color="black")
        info_frame.pack(pady=10)

        name = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 18, "bold"), text_color="darkorange", text=filtered_products[i]["name"])
        name.pack()

        category_frame = customtkinter.CTkFrame(info_frame, fg_color="pink", corner_radius=15)
        category_frame.pack()
        category = customtkinter.CTkLabel(category_frame, font=customtkinter.CTkFont("Helvetica", 13, "bold"), text_color="black", text=filtered_products[i]["category"])
        category.pack(anchor="center", padx=10)

        description = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 13, "normal"), text_color="white", text=filtered_products[i]["description"])
        description.pack(pady=(5,0))

        price = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 14, "bold"), text_color="yellow", text=f"${filtered_products[i]['price']}")
        price.pack()

        button = customtkinter.CTkButton(info_frame, fg_color="darkblue", text="Mua", command=lambda i=i: button_purchase(filtered_products[i]))
        button.pack(pady=(10,0))

header_frame = customtkinter.CTkFrame(app, fg_color="black", corner_radius=0)
header_frame.place(relx=0, rely=0, relwidth=1, relheight=0.1)

entry_min = customtkinter.CTkEntry(header_frame, placeholder_text="Nhập giá thấp nhất")
entry_min.pack(side="left", padx=(10, 0))
entry_max = customtkinter.CTkEntry(header_frame, placeholder_text="Nhập giá cao nhất")
entry_max.pack(side="left", padx=(10, 0))


search_button = customtkinter.CTkButton(header_frame, fg_color="darkblue", text="Tìm", command=filter_products, width=200)
search_button.pack(side="left", padx=(25,0))

scrollable_frame = customtkinter.CTkScrollableFrame(app, corner_radius=10)
scrollable_frame.place(relx=0, rely=0.1, relwidth=1, relheight=0.9)
scrollable_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

products = []

with open(os.path.join("data", "data.json"), "r", encoding="utf-8") as file:
    products = json.load(file)

avl_data = AVLTree()
for product in products:
    avl_data.insert(product)


for i in range(len(products)):
    
    row = i // 4
    col = i % 4
    
    is_last_row = row == (len(products)-1) // 4
    is_last_col = col == 3
    
    x_padding = (0, 0) if is_last_col else (0, 10)
    y_padding = (0, 0) if is_last_row else (0, 10)
    
    product_frame = customtkinter.CTkFrame(scrollable_frame, fg_color="black", corner_radius=10)
    product_frame.grid(row=row, column=col, sticky="nsew", padx=x_padding, pady=y_padding)

    top_frame = customtkinter.CTkFrame(product_frame, fg_color="black", corner_radius=10)
    top_frame.pack(expand=True, fill="both", pady=(10,0))

    bottom_frame = customtkinter.CTkFrame(product_frame, fg_color="black", corner_radius=10)
    bottom_frame.pack(expand=True, fill="both", pady=(0,10))

    image_path = os.path.join("img", products[i]["image"])
    # image = customtkinter.CTkImage(light_image=Image.open(image_path), dark_image=Image.open(image_path), size=(180, 180))
    pil_image = add_border_radius(image_path, radius=20)
    image = customtkinter.CTkImage(light_image=pil_image, dark_image=pil_image, size=(180, 180))

    image_frame = customtkinter.CTkLabel(top_frame, image=image, text="")
    image_frame.pack(padx=15)

    info_frame = customtkinter.CTkFrame(bottom_frame, fg_color="black")
    info_frame.pack(pady=10)

    name = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 18, "bold"), text_color="darkorange", text=products[i]["name"])
    name.pack()

    category_frame = customtkinter.CTkFrame(info_frame, fg_color="pink", corner_radius=15)
    category_frame.pack()
    category = customtkinter.CTkLabel(category_frame, font=customtkinter.CTkFont("Helvetica", 13, "bold"), text_color="black", text=products[i]["category"])
    category.pack(anchor="center", padx=10)

    description = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 13, "normal"), text_color="white", text=products[i]["description"])
    description.pack(pady=(5,0))

    price = customtkinter.CTkLabel(info_frame, font=customtkinter.CTkFont("Helvetica", 14, "bold"), text_color="yellow", text=f"${products[i]['price']}")
    price.pack()

    button = customtkinter.CTkButton(info_frame, fg_color="darkblue", text="Mua", command=lambda i=i: button_purchase(products[i]))
    button.pack(pady=(10,0))

app.mainloop()