import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from tkinter import ttk

class ProductManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت محصولات و ماشین‌ها")

        # اتصال به پایگاه داده و ایجاد فایل‌های پایگاه داده در صورت عدم وجود
        self.product_conn = sqlite3.connect('products.db')
        self.truck_conn = sqlite3.connect('trucks.db')

        self.create_product_table()
        self.create_truck_table()

        self.setup_ui()

    def create_product_table(self):
        with self.product_conn:
            self.product_conn.execute('''CREATE TABLE IF NOT EXISTS products
                                         (id INTEGER PRIMARY KEY,
                                          name TEXT NOT NULL,
                                          length REAL NOT NULL,
                                          width REAL NOT NULL,
                                          height REAL NOT NULL,
                                          quantity INTEGER NOT NULL)''')

    def create_truck_table(self):
        with self.truck_conn:
            self.truck_conn.execute('''CREATE TABLE IF NOT EXISTS trucks
                                       (id INTEGER PRIMARY KEY,
                                        name TEXT NOT NULL,
                                        length REAL NOT NULL,
                                        width REAL NOT NULL,
                                        height REAL NOT NULL)''')

    def setup_ui(self):
        Label(self.root, text="محصولات").grid(row=0, column=0)
        Label(self.root, text="نام").grid(row=1, column=0)
        Label(self.root, text="طول").grid(row=1, column=1)
        Label(self.root, text="عرض").grid(row=1, column=2)
        Label(self.root, text="ارتفاع").grid(row=1, column=3)
        Label(self.root, text="تعداد").grid(row=1, column=4)

        self.product_name_entry = Entry(self.root)
        self.product_name_entry.grid(row=2, column=0)
        self.product_length_entry = Entry(self.root)
        self.product_length_entry.grid(row=2, column=1)
        self.product_width_entry = Entry(self.root)
        self.product_width_entry.grid(row=2, column=2)
        self.product_height_entry = Entry(self.root)
        self.product_height_entry.grid(row=2, column=3)
        self.product_quantity_entry = Entry(self.root)
        self.product_quantity_entry.grid(row=2, column=4)

        Button(self.root, text="افزودن محصول", command=self.add_product).grid(row=2, column=5)

        self.product_list_frame = Frame(self.root)
        self.product_list_frame.grid(row=3, column=0, columnspan=6, pady=10)

        self.product_list = ttk.Treeview(self.product_list_frame, columns=("ID", "نام", "طول", "عرض", "ارتفاع", "تعداد"), show="headings")
        self.product_list.heading("ID", text="ID")
        self.product_list.heading("نام", text="نام")
        self.product_list.heading("طول", text="طول")
        self.product_list.heading("عرض", text="عرض")
        self.product_list.heading("ارتفاع", text="ارتفاع")
        self.product_list.heading("تعداد", text="تعداد")
        self.product_list.pack(side="left")

        self.product_list.bind('<Double-1>', self.on_product_select)

        self.product_scrollbar = ttk.Scrollbar(self.product_list_frame, orient="vertical", command=self.product_list.yview)
        self.product_scrollbar.pack(side="right", fill="y")
        self.product_list.configure(yscrollcommand=self.product_scrollbar.set)

        Label(self.root, text="ماشین‌ها").grid(row=4, column=0)
        Label(self.root, text="نام").grid(row=5, column=0)
        Label(self.root, text="طول").grid(row=5, column=1)
        Label(self.root, text="عرض").grid(row=5, column=2)
        Label(self.root, text="ارتفاع").grid(row=5, column=3)

        self.truck_name_entry = Entry(self.root)
        self.truck_name_entry.grid(row=6, column=0)
        self.truck_length_entry = Entry(self.root)
        self.truck_length_entry.grid(row=6, column=1)
        self.truck_width_entry = Entry(self.root)
        self.truck_width_entry.grid(row=6, column=2)
        self.truck_height_entry = Entry(self.root)
        self.truck_height_entry.grid(row=6, column=3)

        Button(self.root, text="افزودن ماشین", command=self.add_truck).grid(row=6, column=4)

        self.truck_list_frame = Frame(self.root)
        self.truck_list_frame.grid(row=7, column=0, columnspan=5, pady=10)

        self.truck_list = ttk.Treeview(self.truck_list_frame, columns=("ID", "نام", "طول", "عرض", "ارتفاع"), show="headings")
        self.truck_list.heading("ID", text="ID")
        self.truck_list.heading("نام", text="نام")
        self.truck_list.heading("طول", text="طول")
        self.truck_list.heading("عرض", text="عرض")
        self.truck_list.heading("ارتفاع", text="ارتفاع")
        self.truck_list.pack(side="left")

        self.truck_list.bind('<Double-1>', self.on_truck_select)

        self.truck_scrollbar = ttk.Scrollbar(self.truck_list_frame, orient="vertical", command=self.truck_list.yview)
        self.truck_scrollbar.pack(side="right", fill="y")
        self.truck_list.configure(yscrollcommand=self.truck_scrollbar.set)

        self.load_products()
        self.load_trucks()

    def add_product(self):
        name = self.product_name_entry.get()
        length = self.product_length_entry.get()
        width = self.product_width_entry.get()
        height = self.product_height_entry.get()
        quantity = self.product_quantity_entry.get()

        try:
            length = float(length)
            width = float(width)
            height = float(height)
            quantity = int(quantity)

            with self.product_conn:
                self.product_conn.execute('INSERT INTO products (name, length, width, height, quantity) VALUES (?, ?, ?, ?, ?)',
                                          (name, length, width, height, quantity))

            messagebox.showinfo("موفقیت", "محصول با موفقیت اضافه شد!")
            self.clear_product_entries()
            self.load_products()
        except ValueError:
            messagebox.showerror("خطا", "لطفاً اطلاعات معتبر وارد کنید")

    def add_truck(self):
        name = self.truck_name_entry.get()
        length = self.truck_length_entry.get()
        width = self.truck_width_entry.get()
        height = self.truck_height_entry.get()

        try:
            length = float(length)
            width = float(width)
            height = float(height)

            with self.truck_conn:
                self.truck_conn.execute('INSERT INTO trucks (name, length, width, height) VALUES (?, ?, ?, ?)',
                                        (name, length, width, height))

            messagebox.showinfo("موفقیت", "ماشین با موفقیت اضافه شد!")
            self.clear_truck_entries()
            self.load_trucks()
        except ValueError:
            messagebox.showerror("خطا", "لطفاً اطلاعات معتبر وارد کنید")

    def load_products(self):
        for row in self.product_list.get_children():
            self.product_list.delete(row)

        cursor = self.product_conn.execute('SELECT id, name, length, width, height, quantity FROM products')
        for row in cursor:
            self.product_list.insert("", "end", values=row)

    def load_trucks(self):
        for row in self.truck_list.get_children():
            self.truck_list.delete(row)

        cursor = self.truck_conn.execute('SELECT id, name, length, width, height FROM trucks')
        for row in cursor:
            self.truck_list.insert("", "end", values=row)

    def on_product_select(self, event):
        selected_item = self.product_list.selection()[0]
        product_id = self.product_list.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("حذف محصول", "آیا مطمئن هستید که می‌خواهید این محصول را حذف کنید؟")
        if confirm:
            self.delete_product(product_id)
            self.load_products()

    def on_truck_select(self, event):
        selected_item = self.truck_list.selection()[0]
        truck_id = self.truck_list.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("حذف ماشین", "آیا مطمئن هستید که می‌خواهید این ماشین را حذف کنید؟")
        if confirm:
            self.delete_truck(truck_id)
            self.load_trucks()

    def delete_product(self, product_id):
        with self.product_conn:
            self.product_conn.execute('DELETE FROM products WHERE id=?', (product_id,))
            messagebox.showinfo("موفقیت", "محصول با موفقیت حذف شد")

    def delete_truck(self, truck_id):
        with self.truck_conn:
            self.truck_conn.execute('DELETE FROM trucks WHERE id=?', (truck_id,))
            messagebox.showinfo("موفقیت", "ماشین با موفقیت حذف شد")

    def clear_product_entries(self):
        self.product_name_entry.delete(0, 'end')
        self.product_length_entry.delete(0, 'end')
        self.product_width_entry.delete(0, 'end')
        self.product_height_entry.delete(0, 'end')
        self.product_quantity_entry.delete(0, 'end')

    def clear_truck_entries(self):
        self.truck_name_entry.delete(0, 'end')
        self.truck_length_entry.delete(0, 'end')
        self.truck_width_entry.delete(0, 'end')
        self.truck_height_entry.delete(0, 'end')

if __name__ == "__main__":
    root = Tk()
    app = ProductManagementApp(root)
    root.mainloop()

