import tkinter as tk
import json
import csv
import yaml
import os
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
from tkinter import filedialog, messagebox

def read_file(file_path):
    _, extension = os.path.splitext(file_path)
    extension = extension.lower()

    if extension == '.json':
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    elif extension == '.csv':
        with open(file_path, 'r', encoding='utf-8') as file:
            return list(csv.DictReader(file))
    elif extension == '.yaml' or extension == '.yml':
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    elif extension == '.xml':
        tree = ET.parse(file_path)
        root = tree.getroot()
        data = []
        for element in root:
            item = {}
            for child in element:
                item[child.tag] = child.text
            data.append(item)
        return data
    else:
        return None

def write_file(file_path, format, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        if format == 'json':
            json.dump(data, file, indent=4)
        elif format == 'csv':
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        elif format == 'yaml':
            yaml.dump(data, file)
        elif format == 'xml':
            root = ET.Element('root')
            for entry in data:
                item = ET.SubElement(root, 'item')
                for key, value in entry.items():
                    child = ET.SubElement(item, key)
                    child.text = str(value)
            tree = ET.ElementTree(root)
            tree.write(file_path, xml_declaration=True, encoding='utf-8', method='xml')
            
            # Indentation du fichier XML
            xml_string = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
            file.seek(0)
            file.truncate()
            file.write(xml_string)
        else:
            return "Format non supporté"

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=(
        ("Fichiers csv", "*.csv"),
        ("Fichiers xml", "*.xml"),
        ("Fichiers json", "*.json"),
        ("Fichiers yaml", "*.yaml"),
        ("Tous les fichiers", "*.*")
    ))
    if file_path:
        entry_path.delete(0, tk.END)
        entry_path.insert(0, file_path)
        _, extension = os.path.splitext(file_path)
        extension = extension[1:].lower()
        label_format.config(text=f"Format détecté : {extension}",bg='red',font=('verdana',10,'italic bold'))

def on_submit():
    file_path = entry_path.get()
    format = var_format.get()
    data = read_file(file_path)
    if data is None:
        messagebox.showerror("Erreur", "Format de fichier non supporté.")
        return

    output_file_path = filedialog.asksaveasfilename(defaultextension=f".{format}", filetypes=[(f"{format.upper()} files", f"*.{format}")])
    if not output_file_path:
        return

    write_file(output_file_path, format, data)
    messagebox.showinfo("Succès", f"Fichier écrit avec succès en format {format}.")

root = tk.Tk()
root.geometry('500x500')
root.title("Conversion de fichiers")
root['bg'] = 'orange'


entry_path = tk.Entry(root, width=70)
entry_path.pack()

button_select = tk.Button(root,width=20, text="Choisir Fichier",bg='green',fg='white',font=('verdana',15,'normal bold'), command=choose_file)
button_select.pack(padx=20, pady=20)

label_format = tk.Label(root, text="format détecté va afficher ici")
label_format.pack(padx=20, pady=20)

label= tk.Label(root,width=40, text='Choisir un format différent du format détecter',bg='orange' , font=('verdana',8,'normal bold' ))
label.pack()

formats_supportes = ['json', 'csv', 'yaml','xml']
var_format = tk.StringVar()
var_format.set(formats_supportes[0])

for format_supporte in formats_supportes:
    radio_button = tk.Radiobutton(root,width=6,bg='yellow',font=('verdana',15,'italic'), text=format_supporte, variable=var_format, value=format_supporte)
    radio_button.pack(padx=20, pady=6)

button_submit = tk.Button(root,width=20,bg='green',fg='white', text="Convertir",font=('verdana',15,'normal bold'), command=on_submit)
button_submit.pack(padx=20, pady=40)

root.mainloop()
