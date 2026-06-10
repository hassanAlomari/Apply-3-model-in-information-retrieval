import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List, Dict
import PyPDF2

from pooleanModel import boolean_model
from VSM import vectorSpaceModel
from BM25_Model import BM25
from update import vectorSpaceModelUpdate


def pdfs_to_dict(paths: List[str]) -> Dict[str, str]:
    dic: Dict[str, str] = {}
    for idx, path in enumerate(paths, start=1):
        reader = PyPDF2.PdfReader(path)
        full_text = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"
        dic[f"d{idx}"] = full_text.strip()
    return dic


root = tk.Tk()
root.title("Information retrieval system")
root.geometry("700x600")  
root.resizable(False, False)
root.configure(bg="#f5f7fa")

style = ttk.Style(root)
style.theme_use('clam')
style.configure('TFrame', background='#f5f7fa')
style.configure('TLabel', background='#f5f7fa', font=('Helvetica', 12))
style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=8)
style.map('TButton', background=[('active', '#1976d2')], foreground=[('!disabled', '#ffffff')])
style.configure('TEntry', padding=6)
style.configure('TCombobox', padding=6)


pdf_dict: Dict[str, str] = {}
selected_paths: List[str] = []
model_var = tk.StringVar(value="Boolean Model")
k1_var = tk.DoubleVar(value=1.5)  


def upload_pdfs():
    global pdf_dict, selected_paths
    paths = filedialog.askopenfilenames(
        title="Choos PDF",
        filetypes=[("PDF Files", "*.pdf")],
        defaultextension=".pdf"
    )
    if not paths:
        return
    try:
        selected_paths = list(paths)
        pdf_dict = pdfs_to_dict(selected_paths)
        content_listbox.delete(0, tk.END)
        for idx in range(1, len(selected_paths) + 1):
            key = f"d{idx}"
            snippet = pdf_dict[key][:100].replace("\n", " ")
            content_listbox.insert(tk.END, f"{key}: {snippet}...")
    except Exception as e:
        messagebox.showerror("Error PDF", str(e))
        return
    messagebox.showinfo("success", f"Loaded{len(pdf_dict)} Convert PDF file to dictionary.")


def on_model_change(event=None):
    if model_var.get() == "BM25":
        k1_label.grid(row=5, column=0, pady=(10,5), sticky='w')
        k1_entry.grid(row=6, column=0, sticky='w')
    else:
        k1_label.grid_remove()
        k1_entry.grid_remove()


def search():
    query = query_entry.get().strip()
    if not query:
        messagebox.showwarning("warning", "Please enter your search query!")
        return
    if not pdf_dict:
        messagebox.showwarning("warning", "Please upload PDF files first!")
        return

    model = model_var.get()
   
    if model == "BM25":
        k1 = k1_var.get()
        if not (1.2 <= k1 <= 2.0):
            messagebox.showwarning("warning", "The value of k1 should be between 1.2 and 2.0.")
            return
    try:
        if model == "Boolean Model":
            results = boolean_model(query, pdf_dict)
        elif model == "Vector Space Model":
            results = vectorSpaceModel(query, pdf_dict)
        elif model == "Update Vector Space Model":
            results = vectorSpaceModelUpdate(query, pdf_dict)    
        else:
            results = BM25(query, pdf_dict, k1)
    except Exception as e:
        messagebox.showerror("Error while searching", str(e))
        return

    result_box.delete(0, tk.END)
    if results:
        for item in results:
            result_box.insert(tk.END, item)
    else:
        result_box.insert(tk.END, "No matching results found")


main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill='both', expand=True)


upload_btn = ttk.Button(main_frame, text="📌 Attach PDF files", command=upload_pdfs)
upload_btn.grid(row=0, column=0, sticky='w')


content_listbox = tk.Listbox(
    main_frame,
    height=10,
    width=40,
    bd=0,
    highlightthickness=1,
    highlightbackground='#ccc'
)
content_listbox.grid(row=1, column=0, rowspan=4, padx=(0,20), sticky='nsew')


ttk.Label(main_frame, text="Enter your search query :").grid(row=1, column=1, pady=(0,5), sticky='w')
query_entry = ttk.Entry(main_frame, width=40)
query_entry.grid(row=2, column=1, sticky='w')

ttk.Label(main_frame, text="Select your recovery model:").grid(row=3, column=1, pady=(10,5), sticky='w')
model_combo = ttk.Combobox(main_frame, textvariable=model_var, state='readonly', width=38)
model_combo['values'] = ("Boolean Model", "Vector Space Model","Update Vector Space Model", "BM25")
model_combo.grid(row=4, column=1, sticky='w')
model_combo.bind('<<ComboboxSelected>>', on_model_change)


k1_label = ttk.Label(main_frame, text="Enter the value of k1 (1.2–2.0):")
k1_entry = ttk.Entry(main_frame, textvariable=k1_var, width=10)


search_btn = ttk.Button(main_frame, text="🔍 Search", command=search)
search_btn.grid(row=7, column=1, pady=20, sticky='w')


ttk.Label(main_frame, text="Results:").grid(row=8, column=0, columnspan=2, pady=(10,5), sticky='w')
result_box = tk.Listbox(main_frame, height=8, bd=0, highlightthickness=1, highlightbackground='#ccc')
result_box.grid(row=9, column=0, columnspan=2, sticky='nsew')

scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=result_box.yview)
scrollbar.grid(row=9, column=2, sticky='ns')
result_box.configure(yscrollcommand=scrollbar.set)


main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.rowconfigure(9, weight=1)

root.mainloop()
