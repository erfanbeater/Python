import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

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
        products = [{"name": row[0], "length": row[1], "width": row[2], "height": row[3], "quantity": row[4]} for row in cursor]
        conn.close()
        return products

    def load_trucks_from_db(self):
        conn = sqlite3.connect('trucks.db')
        cursor = conn.execute('SELECT name, length, width, height FROM trucks')
        trucks = [{"name": row[0], "length": row[1], "width": row[2], "height": row[3]} for row in cursor]
        conn.close()
        return trucks

    def setup_ui(self):
        self.product_list_frame = tk.Frame(self.root)
        self.product_list_frame.pack(pady=10)

        self.product_list = ttk.Treeview(self.product_list_frame, columns=("نام", "طول", "عرض", "ارتفاع", "تعداد"), show="headings")
        self.product_list.heading("نام", text="نام")
        self.product_list.heading("طول", text="طول")
        self.product_list.heading("عرض", text="عرض")
        self.product_list.heading("ارتفاع", text="ارتفاع")
        self.product_list.heading("تعداد", text="تعداد")
        self.product_list.pack()

        for product in self.products:
            self.product_list.insert("", "end", values=(product["name"], product["length"], product["width"], product["height"], product["quantity"]))

        self.truck_list_frame = tk.Frame(self.root)
        self.truck_list_frame.pack(pady=10)

        self.truck_list = ttk.Treeview(self.truck_list_frame, columns=("نام", "طول", "عرض", "ارتفاع"), show="headings")
        self.truck_list.heading("نام", text="نام")
        self.truck_list.heading("طول", text="طول")
        self.truck_list.heading("عرض", text="عرض")
        self.truck_list.heading("ارتفاع", text="ارتفاع")
        self.truck_list.pack()

        for truck in self.trucks:
            self.truck_list.insert("", "end", values=(truck["name"], truck["length"], truck["width"], truck["height"]))

        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(pady=10)

        tk.Button(self.result_frame, text="پیدا کردن ماشین مناسب", command=self.find_suitable_truck).pack()

    def calculate_total_volume(self):
        total_volume = 0
        for product in self.products:
            product_volume = product["length"] * product["width"] * product["height"] * product["quantity"]
            total_volume += product_volume
        return total_volume

    def find_suitable_truck(self):
        total_volume = self.calculate_total_volume() / 100**3  # تبدیل ابعاد به متر مکعب
        suitable_truck = None

        for truck in self.trucks:
            truck_volume = truck["length"] * truck["width"] * truck["height"]
            if truck_volume >= total_volume:
                suitable_truck = truck
                break

        if suitable_truck:
            empty_volume = truck_volume - total_volume
            messagebox.showinfo("نتیجه", f"ماشین مناسب {suitable_truck['name']} است و حجم خالی {empty_volume} متر مکعب است")
        else:
            messagebox.showerror("خطا", "هیچ ماشین مناسبی پیدا نشد")

if __name__ == "__main__":
    root = tk.Tk()
    app = TruckLoadingApp(root)
    root.mainloop()
