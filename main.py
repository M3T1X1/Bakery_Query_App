import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from sqlalchemy import create_engine, text


class BakeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bakery OLAP Tool - Drill-Down Edition")
        self.root.geometry("1200x900")

        self.db_url = "postgresql://postgres:postgres@localhost:5432/Bakery_Query_App"
        self.engine = create_engine(self.db_url)

        self.setup_ui()
        self.refresh_filters()

    def get_distinct_values(self, table, column):
        try:
            query = f"SELECT DISTINCT {column} FROM {table} ORDER BY {column}"
            with self.engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            return ["Wszystkie"] + df[column].astype(str).tolist()
        except Exception as e:
            print(f"Błąd filtrów: {e}")
            return ["Wszystkie"]

    def setup_ui(self):
        filter_frame = ttk.LabelFrame(self.root, text="Filtrowanie i Ograniczanie Wymiarów (Slice & Dice)")
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Rząd 1: Sklep i Województwo
        ttk.Label(filter_frame, text="Sklep:").grid(row=0, column=0, padx=5, pady=5)
        self.sklep_cb = ttk.Combobox(filter_frame, state="readonly")
        self.sklep_cb.grid(row=0, column=1, padx=5)

        ttk.Label(filter_frame, text="Województwo:").grid(row=0, column=2, padx=5)
        self.woj_cb = ttk.Combobox(filter_frame, state="readonly")
        self.woj_cb.grid(row=0, column=3, padx=5)

        # Rząd 2: Wypiek i Produkt
        ttk.Label(filter_frame, text="Wypiek:").grid(row=1, column=0, padx=5, pady=5)
        self.wypiek_cb = ttk.Combobox(filter_frame, state="readonly")
        self.wypiek_cb.grid(row=1, column=1, padx=5)

        ttk.Label(filter_frame, text="Produkt:").grid(row=1, column=2, padx=5)
        self.prod_cb = ttk.Combobox(filter_frame, state="readonly")
        self.prod_cb.grid(row=1, column=3, padx=5)

        # Rząd 3: Dostawca i Cena Jednostkowa
        ttk.Label(filter_frame, text="Dostawca:").grid(row=2, column=0, padx=5, pady=5)
        self.dost_cb = ttk.Combobox(filter_frame, state="readonly")
        self.dost_cb.grid(row=2, column=1, padx=5)

        price_frame = ttk.Frame(filter_frame)
        price_frame.grid(row=2, column=2, columnspan=2, sticky="w")
        ttk.Label(price_frame, text="Cena od:").pack(side="left", padx=5)
        self.min_price = ttk.Entry(price_frame, width=8)
        self.min_price.insert(0, "0")
        self.min_price.pack(side="left")
        ttk.Label(price_frame, text="do:").pack(side="left", padx=5)
        self.max_price = ttk.Entry(price_frame, width=8)
        self.max_price.insert(0, "9999")
        self.max_price.pack(side="left")

        # Rząd 4: Suma Transakcji
        sum_frame = ttk.Frame(filter_frame)
        sum_frame.grid(row=3, column=0, columnspan=2, sticky="w", pady=5)
        ttk.Label(sum_frame, text="Suma od:").pack(side="left", padx=5)
        self.min_sum = ttk.Entry(sum_frame, width=8)
        self.min_sum.insert(0, "0")
        self.min_sum.pack(side="left")
        ttk.Label(sum_frame, text="do:").pack(side="left", padx=5)
        self.max_sum = ttk.Entry(sum_frame, width=8)
        self.max_sum.insert(0, "99999")
        self.max_sum.pack(side="left")

        # Panel Operacji
        olap_frame = ttk.LabelFrame(self.root, text="Operacje OLAP")
        olap_frame.pack(fill="x", padx=10, pady=5)
        ttk.Button(olap_frame, text="Filtruj (Grupowanie)", command=self.load_data).grid(row=0, column=0, padx=5)
        ttk.Button(olap_frame, text="Obróć (Pivot)", command=self.pivot_data).grid(row=0, column=1, padx=5)
        ttk.Button(olap_frame, text="Zwiń (Roll-up)", command=self.roll_up).grid(row=0, column=2, padx=5)
        ttk.Button(olap_frame, text="Eksport Excel", command=self.export_to_excel).grid(row=0, column=3, padx=5)

        # Informacja o Drill-down
        self.status_label = ttk.Label(self.root,
                                      text="Podpowiedź: Użyj Roll-up, a potem kliknij dwukrotnie wiersz, aby wykonać Drill-down",
                                      foreground="blue")
        self.status_label.pack(pady=2)

        # Tabela
        self.tree_frame = ttk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree = ttk.Treeview(self.tree_frame, show="headings")
        self.tree.pack(fill="both", expand=True)

        # Bindowanie podwójnego kliknięcia dla DRILL-DOWN
        self.tree.bind("<Double-1>", self.on_double_click)

    def refresh_filters(self):
        self.sklep_cb['values'] = self.get_distinct_values("Sklepy", "nazwa")
        self.sklep_cb.set("Wszystkie")
        self.wypiek_cb['values'] = self.get_distinct_values("Wypieki", "nazwa")
        self.wypiek_cb.set("Wszystkie")
        self.woj_cb['values'] = self.get_distinct_values("Adresy", "wojewodztwo")
        self.woj_cb.set("Wszystkie")
        self.prod_cb['values'] = self.get_distinct_values("Produkty", "nazwa")
        self.prod_cb.set("Wszystkie")
        self.dost_cb['values'] = self.get_distinct_values("Dostawcy", "nazwa")
        self.dost_cb.set("Wszystkie")

    def fetch_from_db(self):
        query = text("""
                     SELECT s.Nazwa            as sklep,
                            a.Wojewodztwo      as wojewodztwo,
                            w.Nazwa            as wypiek,
                            p.Nazwa            as produkt,
                            d.Nazwa            as dostawca,
                            t.Ilosc,
                            t.Cena,
                            (t.Ilosc * t.Cena) as suma
                     FROM Transakcje t
                              JOIN Sklepy s ON t.ID_sklepu = s.ID_sklepu
                              JOIN Adresy a ON s.ID_adresu = a.ID_adresu
                              JOIN Wypieki w ON t.ID_wypieku = w.ID_wypieku
                              JOIN Produkty p ON w.ID_produktu = p.ID_produktu
                              JOIN Dostawcy d ON p.ID_dostawcy = d.ID_dostawcy
                     WHERE t.Cena >= :min_p
                       AND t.Cena <= :max_p
                     """)
        try:
            p_min, p_max = float(self.min_price.get()), float(self.max_price.get())
            s_min, s_max = float(self.min_sum.get()), float(self.max_sum.get())

            with self.engine.connect() as conn:
                df = pd.read_sql_query(query, conn, params={"min_p": p_min, "max_p": p_max})

            df = df[(df['suma'] >= s_min) & (df['suma'] <= s_max)]

            if self.sklep_cb.get() != "Wszystkie": df = df[df['sklep'] == self.sklep_cb.get()]
            if self.wypiek_cb.get() != "Wszystkie": df = df[df['wypiek'] == self.wypiek_cb.get()]
            if self.woj_cb.get() != "Wszystkie": df = df[df['wojewodztwo'] == self.woj_cb.get()]
            if self.prod_cb.get() != "Wszystkie": df = df[df['produkt'] == self.prod_cb.get()]
            if self.dost_cb.get() != "Wszystkie": df = df[df['dostawca'] == self.dost_cb.get()]

            return df
        except Exception as e:
            messagebox.showerror("Błąd", f"Błąd: {e}")
            return None

    def display_df(self, df):
        self.tree.delete(*self.tree.get_children())
        if df is None or df.empty: return
        self.tree["columns"] = list(df.columns)
        for col in df.columns:
            self.tree.heading(col, text=col.upper())
            self.tree.column(col, width=110)
        for _, row in df.iterrows():
            self.tree.insert("", "end", values=list(row))

    def on_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")

        if len(self.tree["columns"]) == 3 and "wojewodztwo" in self.tree["columns"]:
            chosen_woj = values[0]
            self.woj_cb.set(chosen_woj)
            self.load_data()
            messagebox.showinfo("Drill-down", f"Pokazuję szczegóły dla: {chosen_woj}")

    def load_data(self):
        self.df = self.fetch_from_db()
        self.display_df(self.df)

    def pivot_data(self):
        if hasattr(self, 'df') and not self.df.empty:
            pivot = self.df.pivot_table(index='sklep', columns='wypiek', values='ilosc', aggfunc='sum').fillna(
                0).reset_index()
            self.display_df(pivot)

    def roll_up(self):
        if hasattr(self, 'df') and not self.df.empty:
            summary = self.df.groupby('wojewodztwo').agg({'ilosc': 'sum', 'suma': 'sum'}).reset_index()
            self.display_df(summary)

    def export_to_excel(self):
        if hasattr(self, 'df') and not self.df.empty:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
            if path:
                self.df.to_excel(path, index=False)
                messagebox.showinfo("Sukces", "Dane wyeksportowane!")


if __name__ == "__main__":
    root = tk.Tk()
    app = BakeryApp(root)
    root.mainloop()