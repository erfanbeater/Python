import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk 
from tkinter.simpledialog import askinteger
class TruckLoadingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("برنامه بارگیری ماشین")

        self.products = self.load_products_from_db()
        self.trucks = self.load_trucks_from_db()

        self.setup_ui()

    def load_products_from_db(self):
        conn = sqlite3.connect('products.db')
        cursor = conn.execute('SELECT name, length, width, height, quantity FROM products')
        products = [{"name": row[0], "length": float(row[1]), "width": float(row[2]), "height": float(row[3]), "quantity": int(row[4])} for row in cursor]
        conn.close()
        return products

    def load_trucks_from_db(self):
        conn = sqlite3.connect('trucks.db')
        cursor = conn.execute('SELECT name, length, width, height FROM trucks')
        trucks = [{"name": row[0], "length": float(row[1]), "width": float(row[2]), "height": float(row[3])} for row in cursor]
        conn.close()
        return trucks

    def setup_ui(self):
        self.product_list_frame = tk.Frame(self.root)
        self.product_list_frame.pack(pady=10)

        self.product_list = ttk.Treeview(self.product_list_frame, columns=("نام", "طول", "عرض", "ارتفاع", "تعداد"), show="headings", selectmode="extended")
        self.product_list.heading("نام", text="نام")
        self.product_list.heading("طول", text="طول")
        self.product_list.heading("عرض", text="عرض")
        self.product_list.heading("ارتفاع", text="ارتفاع")
        self.product_list.heading("تعداد", text="تعداد")
        self.product_list.pack()

        for product in self.products:
            self.product_list.insert("", "end", values=(product["name"], product["length"], product["width"], product["height"], product["quantity"]))

        self.product_list.bind("<Double-1>", self.edit_quantity)

        self.truck_list_frame = tk.Frame(self.root)
        self.truck_list_frame.pack(pady=10)

        truck_label_text = "\n\n".join([f"{truck['name']}" for truck in self.trucks])
        self.truck_list_label = tk.Label(self.truck_list_frame, text=truck_label_text)
        self.truck_list_label.pack()

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

        tk.Button(self.result_frame, text="پیدا کردن ماشین مناسب", command=self.find_suitable_truck).pack()


    def calculate_total_volume(self, selected_products):
        total_volume = 0
        for product in selected_products:
            product_volume = product["length"] * product["width"] * product["height"] * product["quantity"]
            total_volume += product_volume
        return total_volume

    def edit_quantity(self, event):
        selected_item = self.product_list.selection()[0]
        item_values = self.product_list.item(selected_item, "values")
        quantity = item_values[4]

        new_quantity = askinteger("ویرایش تعداد", f"تعداد فعلی: {quantity}\nتعداد جدید:")
        if new_quantity is not None:
            self.product_list.item(selected_item, values=(item_values[0], item_values[1], item_values[2], item_values[3], new_quantity))

    def find_suitable_truck(self):
        selected_items = self.product_list.selection()
        if not selected_items:
            messagebox.showwarning("هشدار", "لطفاً حداقل یک محصول را انتخاب کنید")
            return

        selected_products = []
        for item in selected_items:
            item_values = self.product_list.item(item, "values")
            product = {
                "name": item_values[0],
                "length": float(item_values[1]),
                "width": float(item_values[2]),
                "height": float(item_values[3]),
                "quantity": int(item_values[4])
            }
            selected_products.append(product)

        total_volume = self.calculate_total_volume(selected_products) / 100**3  # تبدیل ابعاد به متر مکعب
        suitable_truck = None
        min_remaining_volume = float('inf')  # حجم باقی‌مانده را برابر بی‌نهایت مقداردهی اولیه می‌کنیم

        for truck in self.trucks:
            truck_volume = truck["length"] * truck["width"] * truck["height"]
            remaining_volume = truck_volume - total_volume
            if remaining_volume >= 0 and remaining_volume < min_remaining_volume:  # فقط ماشین‌هایی را در نظر بگیرید که حجم باقی‌مانده مثبت باشد
                suitable_truck = truck
                min_remaining_volume = remaining_volume

        if suitable_truck:
            empty_volume = min_remaining_volume
            empty_volume_cm3 = empty_volume * 100**3  # تبدیل به سانتی‌متر مکعب
            messagebox.showinfo("نتیجه", f"ماشین مناسب {suitable_truck['name']} است و حجم خالی {empty_volume:.2f} متر مکعب است")
        else:
            messagebox.showerror("خطا", "هیچ ماشین مناسبی پیدا نشد")

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckLoadingApp(root)
    root.mainloop()
