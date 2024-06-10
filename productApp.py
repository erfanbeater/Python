import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, Frame
from tkinter import ttk

class ProductDBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("مدیریت پایگاه داده محصولات")

        # اتصال به پایگاه داده و ایجاد فایل پایگاه داده در صورت عدم وجود
        self.conn = sqlite3.connect('products.db')
        self.create_table()

        self.setup_ui()
        self.load_products()

    def create_table(self):
        with self.conn:
            self.conn.execute('''CREATE TABLE IF NOT EXISTS products
                                 (id INTEGER PRIMARY KEY,
                                  name TEXT NOT NULL,
                                  length REAL NOT NULL,
                                  width REAL NOT NULL,
                                  height REAL NOT NULL,
                                  quantity INTEGER NOT NULL)''')

    def setup_ui(self):
        Label(self.root, text="نام محصول").grid(row=0, column=0)
        Label(self.root, text="طول").grid(row=0, column=1)
        Label(self.root, text="عرض").grid(row=0, column=2)
        Label(self.root, text="ارتفاع").grid(row=0, column=3)
        Label(self.root, text="تعداد").grid(row=0, column=4)

        self.name_entry = Entry(self.root)
        self.name_entry.grid(row=1, column=0)
        self.length_entry = Entry(self.root)
        self.length_entry.grid(row=1, column=1)
        self.width_entry = Entry(self.root)
        self.width_entry.grid(row=1, column=2)
        self.height_entry = Entry(self.root)
        self.height_entry.grid(row=1, column=3)
        self.quantity_entry = Entry(self.root)
        self.quantity_entry.grid(row=1, column=4)

        Button(self.root, text="افزودن محصول", command=self.add_product).grid(row=1, column=5)

        self.product_list_frame = Frame(self.root)
        self.product_list_frame.grid(row=2, column=0, columnspan=6, pady=10)

        self.product_list = ttk.Treeview(self.product_list_frame, columns=("ID", "نام", "طول", "عرض", "ارتفاع", "تعداد"), show="headings")
        self.product_list.heading("ID", text="ID")
        self.product_list.heading("نام", text="نام")
        self.product_list.heading("طول", text="طول")
        self.product_list.heading("عرض", text="عرض")
        self.product_list.heading("ارتفاع", text="ارتفاع")
        self.product_list.heading("تعداد", text="تعداد")
        self.product_list.pack(side="left")

        self.product_list.bind('<Double-1>', self.on_product_select)

        self.scrollbar = ttk.Scrollbar(self.product_list_frame, orient="vertical", command=self.product_list.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.product_list.configure(yscrollcommand=self.scrollbar.set)

    def add_product(self):
        name = self.name_entry.get()
        length = self.length_entry.get()
        width = self.width_entry.get()
        height = self.height_entry.get()
        quantity = self.quantity_entry.get()

        try:
            length = float(length)
            width = float(width)
            height = float(height)
            quantity = int(quantity)

            with self.conn:
                self.conn.execute('INSERT INTO products (name, length, width, height, quantity) VALUES (?, ?, ?, ?, ?)',
                                  (name, length, width, height, quantity))

            messagebox.showinfo("موفقیت", "محصول با موفقیت اضافه شد!")
            self.clear_entries()
            self.load_products()
        except ValueError:
            messagebox.showerror("خطا", "لطفاً اطلاعات معتبر وارد کنید")

    def load_products(self):
        for row in self.product_list.get_children():
            self.product_list.delete(row)

        cursor = self.conn.execute('SELECT id, name, length, width, height, quantity FROM products')
        for row in cursor:
            self.product_list.insert("", "end", values=row)

    def on_product_select(self, event):
        selected_item = self.product_list.selection()[0]
        product_id = self.product_list.item(selected_item, 'values')[0]

        confirm = messagebox.askyesno("حذف محصول", "آیا مطمئن هستید که می‌خواهید این محصول را حذف کنید؟")
        if confirm:
            self.delete_product(product_id)
            self.load_products()

    def delete_product(self, product_id):
        with self.conn:
            self.conn.execute('DELETE FROM products WHERE id=?', (product_id,))
            messagebox.showinfo("موفقیت", "محصول با موفقیت حذف شد")

    def clear_entries(self):
        self.name_entry.delete(0, 'end')
        self.length_entry.delete(0, 'end')
        self.width_entry.delete(0, 'end')
        self.height_entry.delete(0, 'end')
        self.quantity_entry.delete(0, 'end')

if __name__ == "__main__":
    root = Tk()
    app = ProductDBApp(root)
    root.mainloop()
