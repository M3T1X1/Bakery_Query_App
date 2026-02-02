import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from sqlalchemy import create_engine, text


class BakeryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bakery ERP System - Full OLAP & CRUD (Add/Delete Only)")
        self.root.geometry("1300x950")

        # Konfiguracja połączenia
        self.db_url = "postgresql://postgres:postgres@localhost:5432/Bakery_Query_App"
        self.engine = create_engine(self.db_url)

        # Mapa relacji dla kluczy obcych
        self.fk_map = {
            "id_adresu": ("Adresy", "id_adresu", "wojewodztwo || ' - ' || miasto || ' ' || ulica"),
            "id_sklepu": ("Sklepy", "id_sklepu", "nazwa"),
            "id_dostawcy": ("Dostawcy", "id_dostawcy", "nazwa"),
            "id_produktu": ("Produkty", "id_produktu", "nazwa"),
            "id_wypieku": ("Wypieki", "id_wypieku", "nazwa")
        }

        # Definicja kolumn unikalnych
        self.unique_fields = {
            "Sklepy": "nazwa",
            "Dostawcy": "nazwa",
            "Produkty": "nazwa",
            "Wypieki": "nazwa",
            "Pracownicy": "nazwisko"
        }

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True)

        self.tab_olap = ttk.Frame(self.notebook)
        self.tab_crud = ttk.Frame(self.notebook)

        self.notebook.add(self.tab_olap, text="📊 Analiza OLAP")
        self.notebook.add(self.tab_crud, text="⚙️ Zarządzanie Danymi")

        self.setup_olap_ui()
        self.setup_crud_ui()
        self.refresh_filters()
        self.load_data()

    # --- POMOCNICZE ---
    def get_distinct_values(self, table, column):
        try:
            query = f"SELECT DISTINCT {column} FROM {table} ORDER BY {column}"
            with self.engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            return ["Wszystkie"] + df[column].astype(str).tolist()
        except:
            return ["Wszystkie"]

    def get_fk_options(self, fk_col):
        if fk_col not in self.fk_map: return []
        table, pk, display = self.fk_map[fk_col]
        query = f"SELECT {pk}, ({display}) as label FROM {table} ORDER BY label"
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql_query(text(query), conn)
            return df.values.tolist()
        except:
            return []

    # --- OLAP ---
    def setup_olap_ui(self):
        filter_frame = ttk.LabelFrame(self.tab_olap, text="Slice & Dice (Filtrowanie)")
        filter_frame.pack(fill="x", padx=10, pady=5)

        # Filtry wymiarów
        ttk.Label(filter_frame, text="Sklep:").grid(row=0, column=0, padx=5)
        self.sklep_cb = ttk.Combobox(filter_frame, state="readonly");
        self.sklep_cb.grid(row=0, column=1)

        ttk.Label(filter_frame, text="Województwo:").grid(row=0, column=2, padx=5)
        self.woj_cb = ttk.Combobox(filter_frame, state="readonly");
        self.woj_cb.grid(row=0, column=3)

        ttk.Label(filter_frame, text="Wypiek:").grid(row=1, column=0, padx=5)
        self.wypiek_cb = ttk.Combobox(filter_frame, state="readonly");
        self.wypiek_cb.grid(row=1, column=1)

        ttk.Label(filter_frame, text="Produkt:").grid(row=1, column=2, padx=5)
        self.prod_cb = ttk.Combobox(filter_frame, state="readonly");
        self.prod_cb.grid(row=1, column=3)

        # Filtry miar (Cena i Suma)
        m_frame = ttk.Frame(filter_frame)
        m_frame.grid(row=2, column=0, columnspan=4, sticky="w", pady=5)

        ttk.Label(m_frame, text="Cena min/max:").pack(side="left", padx=5)
        self.min_price = ttk.Entry(m_frame, width=8);
        self.min_price.insert(0, "0");
        self.min_price.pack(side="left")
        self.max_price = ttk.Entry(m_frame, width=8);
        self.max_price.insert(0, "9999");
        self.max_price.pack(side="left")

        ttk.Label(m_frame, text="Suma min/max:").pack(side="left", padx=20)
        self.min_total = ttk.Entry(m_frame, width=8);
        self.min_total.insert(0, "0");
        self.min_total.pack(side="left")
        self.max_total = ttk.Entry(m_frame, width=8);
        self.max_total.insert(0, "99999");
        self.max_total.pack(side="left")

        btn_frame = ttk.Frame(self.tab_olap)
        btn_frame.pack(fill="x", padx=10)
        ttk.Button(btn_frame, text="Filtruj", command=self.load_data).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Roll-up", command=self.roll_up).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Pivot", command=self.pivot_data).pack(side="left", padx=2)
        ttk.Button(btn_frame, text="Export", command=self.export_to_excel).pack(side="left", padx=2)

        self.tree_olap = ttk.Treeview(self.tab_olap, show="headings")
        self.tree_olap.pack(fill="both", expand=True, padx=10, pady=10)
        self.tree_olap.bind("<Double-1>", self.on_double_click)

    def fetch_from_db(self):
        query = text("""SELECT s.Nazwa            as sklep,
                               a.Wojewodztwo      as wojewodztwo,
                               w.Nazwa            as wypiek,
                               p.Nazwa            as produkt,
                               t.Ilosc            as ilosc,
                               t.Cena             as cena,
                               (t.Ilosc * t.Cena) as suma
                        FROM Transakcje t
                                 JOIN Sklepy s ON t.ID_sklepu = s.ID_sklepu
                                 JOIN Adresy a ON s.ID_adresu = a.ID_adresu
                                 JOIN Wypieki w ON t.ID_wypieku = w.ID_wypieku
                                 JOIN Produkty p ON w.ID_produktu = p.ID_produktu
                        WHERE t.Cena >= :min_p
                          AND t.Cena <= :max_p""")
        try:
            with self.engine.connect() as conn:
                df = pd.read_sql_query(query, conn, params={
                    "min_p": float(self.min_price.get()),
                    "max_p": float(self.max_price.get())
                })

            # Filtry wymiarów
            if self.sklep_cb.get() != "Wszystkie": df = df[df['sklep'] == self.sklep_cb.get()]
            if self.woj_cb.get() != "Wszystkie": df = df[df['wojewodztwo'] == self.woj_cb.get()]
            if self.wypiek_cb.get() != "Wszystkie": df = df[df['wypiek'] == self.wypiek_cb.get()]
            if self.prod_cb.get() != "Wszystkie": df = df[df['produkt'] == self.prod_cb.get()]

            # FILTROWANIE PO SUMIE
            df = df[(df['suma'] >= float(self.min_total.get())) & (df['suma'] <= float(self.max_total.get()))]

            return df
        except Exception as e:
            print(f"Błąd OLAP: {e}")
            return pd.DataFrame()

    def load_data(self):
        self.current_df = self.fetch_from_db()
        self.display_df(self.tree_olap, self.current_df)

    def roll_up(self):
        if not self.current_df.empty:
            summary = self.current_df.groupby('wojewodztwo').agg({'ilosc': 'sum', 'suma': 'sum'}).reset_index()
            # Po Roll-upie też możemy chcieć filtrować po nowej sumie zagregowanej
            summary = summary[
                (summary['suma'] >= float(self.min_total.get())) & (summary['suma'] <= float(self.max_total.get()))]
            self.display_df(self.tree_olap, summary)

    def pivot_data(self):
        if not self.current_df.empty:
            pivot = self.current_df.pivot_table(index='sklep', columns='wypiek', values='suma', aggfunc='sum').fillna(
                0).reset_index()
            self.display_df(self.tree_olap, pivot)

    def on_double_click(self, event):
        item = self.tree_olap.selection()[0]
        values = self.tree_olap.item(item, "values")
        if "wojewodztwo" in self.tree_olap["columns"]:
            idx = list(self.tree_olap["columns"]).index("wojewodztwo")
            self.woj_cb.set(values[idx]);
            self.load_data()

    # --- CRUD (ADD & DELETE ONLY) ---
    def setup_crud_ui(self):
        ctrl_frame = ttk.Frame(self.tab_crud)
        ctrl_frame.pack(fill="x", padx=10, pady=10)
        self.table_selector = ttk.Combobox(ctrl_frame,
                                           values=["Adresy", "Sklepy", "Pracownicy", "Dostawcy", "Produkty", "Wypieki",
                                                   "Transakcje"], state="readonly")
        self.table_selector.pack(side="left", padx=5)
        self.table_selector.bind("<<ComboboxSelected>>", lambda e: self.load_crud_data())

        ttk.Button(ctrl_frame, text="➕ Dodaj", command=self.open_add_window).pack(side="left", padx=2)
        ttk.Button(ctrl_frame, text="🗑️ Usuń", command=self.delete_record).pack(side="left", padx=2)

        self.tree_crud = ttk.Treeview(self.tab_crud, show="headings")
        self.tree_crud.pack(fill="both", expand=True, padx=10, pady=5)

    def load_crud_data(self):
        table = self.table_selector.get()
        if not table: return
        with self.engine.connect() as conn:
            df = pd.read_sql_query(text(f"SELECT * FROM {table} ORDER BY 1 ASC"), conn)
        self.display_df(self.tree_crud, df)

    def delete_record(self):
        table = self.table_selector.get()
        selected = self.tree_crud.selection()
        if not selected: return
        pk_col, pk_val = self.tree_crud["columns"][0], self.tree_crud.item(selected[0])["values"][0]
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno usunąć?"):
            try:
                with self.engine.begin() as conn:
                    conn.execute(text(f"DELETE FROM {table} WHERE {pk_col} = :id"), {"id": pk_val})
                self.load_crud_data();
                self.refresh_filters()
            except:
                messagebox.showerror("Błąd", "Rekord jest powiązany z innymi danymi.")

    def open_add_window(self):
        table = self.table_selector.get()
        if not table: return
        win = tk.Toplevel(self.root)
        win.title(f"Dodawanie: {table}")
        cols = self.tree_crud["columns"]
        entries = {}
        for i in range(1, len(cols)):
            col = cols[i]
            low_col = col.lower()
            ttk.Label(win, text=f"{col}:").grid(row=i, column=0, padx=10, pady=5, sticky="w")
            if low_col in self.fk_map:
                opts = self.get_fk_options(low_col)
                labels = [o[1] for o in opts];
                ids = [o[0] for o in opts]
                cb = ttk.Combobox(win, values=labels, width=33, state="readonly")
                cb.grid(row=i, column=1, padx=10, pady=5)
                entries[col] = (cb, ids, "fk")
            elif "wlasnosciowy" in low_col:
                cb = ttk.Combobox(win, values=["Tak", "Nie"], width=33, state="readonly")
                cb.grid(row=i, column=1, padx=10, pady=5);
                cb.set("Tak")
                entries[col] = (cb, None, "bool")
            else:
                ent = ttk.Entry(win, width=35);
                ent.grid(row=i, column=1, padx=10, pady=5)
                entries[col] = ent

        def save():
            try:
                data = {}
                v_rules = {
                    "imie": "alpha", "nazwisko": "alpha", "stanowisko": "alpha",
                    "zarobki": "float", "pensja": "float", "cena_produkcji": "float",
                    "gramatura": "float", "czas_wypieku": "float", "cena": "float",
                    "data_zatrudnienia": "datetime", "data_transakcji": "datetime"
                }
                for c, obj in entries.items():
                    col_key = c.lower()
                    if isinstance(obj, tuple):
                        widget, extra, mode = obj
                        if mode == "fk":
                            if widget.current() == -1:
                                messagebox.showwarning("Uwaga", f"Wybierz wartość dla: {c}");
                                return
                            data[col_key] = extra[widget.current()]
                        else:
                            data[col_key] = True if widget.get() == "Tak" else False
                    else:
                        val = obj.get().strip()
                        if val == "":
                            messagebox.showwarning("Uwaga", f"Pole {c} jest puste!");
                            return
                        rule = v_rules.get(col_key)
                        if rule == "alpha":
                            if not val.replace(" ", "").isalpha():
                                messagebox.showwarning("Błąd", f"Pole {c} może zawierać tylko litery!");
                                return
                            data[col_key] = val
                        elif rule == "float":
                            try:
                                data[col_key] = float(val.replace(",", "."))
                            except:
                                messagebox.showwarning("Błąd", f"Pole {c} musi być liczbą!"); return
                        elif rule == "datetime":
                            try:
                                data[col_key] = pd.to_datetime(val, dayfirst=True)
                            except:
                                messagebox.showwarning("Błąd", f"Pole {c}: wymagany format DD.MM.RRRR"); return
                        else:
                            data[col_key] = val
                if table in self.unique_fields:
                    u_col = self.unique_fields[table].lower()
                    u_val = data.get(u_col)
                    with self.engine.connect() as conn:
                        exists = conn.execute(text(f"SELECT COUNT(*) FROM {table} WHERE LOWER({u_col}) = LOWER(:v)"),
                                              {"v": str(u_val)}).scalar()
                        if exists > 0:
                            messagebox.showerror("Błąd", f"Wartość '{u_val}' już istnieje w {table}!");
                            return
                with self.engine.begin() as conn:
                    fields = list(data.keys())
                    placeholders = ", ".join([f":{f}" for f in fields])
                    sql = f"INSERT INTO {table} ({', '.join(fields)}) VALUES ({placeholders})"
                    conn.execute(text(sql), data)
                win.destroy();
                self.load_crud_data();
                self.refresh_filters()
                messagebox.showinfo("Sukces", "Pomyślnie dodano rekord!")
            except Exception as e:
                messagebox.showerror("Błąd Krytyczny", f"Nie udało się zapisać:\n{str(e)}")

        ttk.Button(win, text="Zapisz", command=save).grid(row=len(cols) + 1, columnspan=2, pady=15)

    # --- WSPÓLNE ---
    def display_df(self, tree, df):
        tree.delete(*tree.get_children())
        if df.empty: return
        tree["columns"] = list(df.columns)
        for col in df.columns: tree.heading(col, text=col.upper()); tree.column(col, width=110, anchor="center")
        for _, row in df.iterrows(): tree.insert("", "end", values=list(row))

    def refresh_filters(self):
        self.sklep_cb['values'] = self.get_distinct_values("Sklepy", "nazwa");
        self.sklep_cb.set("Wszystkie")
        self.woj_cb['values'] = self.get_distinct_values("Adresy", "wojewodztwo");
        self.woj_cb.set("Wszystkie")
        self.wypiek_cb['values'] = self.get_distinct_values("Wypieki", "nazwa");
        self.wypiek_cb.set("Wszystkie")
        self.prod_cb['values'] = self.get_distinct_values("Produkty", "nazwa");
        self.prod_cb.set("Wszystkie")

    def export_to_excel(self):
        if hasattr(self, 'current_df') and not self.current_df.empty:
            path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])
            if path: self.current_df.to_excel(path, index=False); messagebox.showinfo("Sukces", "Eksport OK!")


if __name__ == "__main__":
    root = tk.Tk()
    ttk.Style().theme_use('clam')
    app = BakeryApp(root)
    root.mainloop()