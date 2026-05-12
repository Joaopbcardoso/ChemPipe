import pandas as pd
import tkinter as tk
from tkinter import ttk

# --- Carregar dados (limitando linhas para não travar) ---
df_abund = pd.read_excel("xlsx/ABUND.xlsx", nrows=200)
df_compostos = pd.read_excel("xlsx/Compostos_final.xlsx", nrows=200)
df_identificacao = pd.read_excel("xlsx/IDENTIFICACAO.xlsx", nrows=200)

df_total = pd.concat([df_abund, df_compostos, df_identificacao], ignore_index=True)

# --- Funções ---
def carregar_dados(dataframe):
    for item in tree.get_children():
        tree.delete(item)
    for _, row in dataframe.iterrows():
        tree.insert("", "end", values=list(row))

def aplicar_filtro():
    coluna = coluna_combo.get()
    termo = filtro_entry.get().lower()
    if coluna and termo:
        filtrado = df_total[df_total[coluna].astype(str).str.lower().str.contains(termo)]
        carregar_dados(filtrado)

def limpar_filtro():
    filtro_entry.delete(0, tk.END)
    carregar_dados(df_total)

# --- Interface ---
root = tk.Tk()
root.title("Visualizador de Dados Químicos")
root.geometry("1200x600")
root.configure(bg="#e6f2ff")

style = ttk.Style(root)
style.theme_use("clam")
style.configure("Treeview.Heading", font=("Arial", 11, "bold"), background="#004080", foreground="white")
style.configure("Treeview", font=("Arial", 10), rowheight=25)

# Frame superior
top_frame = ttk.Frame(root, padding=10)
top_frame.pack(fill="x")

coluna_label = ttk.Label(top_frame, text="Coluna:", font=("Arial", 11))
coluna_label.pack(side="left")

coluna_combo = ttk.Combobox(top_frame, values=list(df_total.columns), width=30)
coluna_combo.pack(side="left", padx=5)

filtro_label = ttk.Label(top_frame, text="Filtro:", font=("Arial", 11))
filtro_label.pack(side="left")

filtro_entry = ttk.Entry(top_frame, width=30)
filtro_entry.pack(side="left", padx=5)

btn_filtrar = ttk.Button(top_frame, text="Aplicar Filtro", command=aplicar_filtro)
btn_filtrar.pack(side="left", padx=5)

btn_limpar = ttk.Button(top_frame, text="Limpar", command=limpar_filtro)
btn_limpar.pack(side="left", padx=5)

# Frame da tabela
frame = ttk.Frame(root)
frame.pack(fill="both", expand=True)

tree = ttk.Treeview(frame, columns=list(df_total.columns), show="headings")

for col in df_total.columns:
    tree.heading(col, text=col)
    tree.column(col, width=150)

scroll_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
scroll_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)

scroll_y.pack(side="right", fill="y")
scroll_x.pack(side="bottom", fill="x")
tree.pack(fill="both", expand=True)

# Carregar dados iniciais
carregar_dados(df_total)

root.mainloop()
