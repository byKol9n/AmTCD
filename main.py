import tkinter as tk
from tkinter import filedialog
import configparser
class Parameters(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Параметры")
        self.geometry("300x150") # Создание элементов интерфейса для ввода зашифрованного текста
        self.key_label = tk.Label(self, text="Личный ключ:")
        self.key_label.pack(side=tk.TOP)
        self.key_entry = tk.Entry(self, show="*")
        self.key_entry.pack(side=tk.TOP)
        self.save_key_button = tk.Button(self, text="Сохранить ключ", command=self.save_key)
        self.save_key_button2 = tk.Button(self, text="Установить ключ", command=self.set_key)
        self.save_key_button.pack(side=tk.TOP, pady=5)
        self.save_key_button2.pack(side=tk.TOP, pady=5)
    def set_key(self):
        AmTCD.key = self.key_entry.get()
        tk.messagebox.showinfo(title="Готово", message="Ключ установлен")
    def save_key(self): # Реализация сохранения личного ключа в конфигурационном файле
        config = configparser.ConfigParser()
        config["main"] = {"keyuser": self.key_entry.get()}
        with open("AmTCD.ini", "w") as f:
            config.write(f)
            tk.messagebox.showinfo(title="Сохранено", message="Ключ сохранён под именем ""AmTCD.ini")
class AmTCD(tk.Frame):
    key = 0
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Блокнот AmTCD")
        self.pack()
        self.create_widgets()
        self.filename = None
    def create_widgets(self): # Создание элементов интерфейса для отображения зашифрованного текста
        self.statusbar = tk.Label(self, text="Ожидаем ввода...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.text_box = tk.Text(self)
        self.text_box.pack(expand=True)
        menubar = tk.Menu(self.master) # Создание элементов меню
        self.master.config(menu=menubar)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Создать файл", command=self.create_file, accelerator="Ctrl+N")
        filemenu.add_command(label="Открыть файл", command=self.open_file, accelerator="Ctrl+O")
        filemenu.add_command(label="Сохранить файл", command=self.save_file, accelerator="Ctrl+S")
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.exit)
        menubar.add_cascade(label="Файл", menu=filemenu)
        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Копировать", command=self.copy, accelerator="Ctrl+C")
        editmenu.add_command(label="Вставить", command=self.paste, accelerator="Ctrl+V")
        editmenu.add_command(label="Вырезать", command=self.cut, accelerator="Ctrl+X")
        editmenu.add_separator()
        editmenu.add_command(label="Параметры...", command=self.open_parameters)
        menubar.add_cascade(label="Правка", menu=editmenu)
        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Справка", command=self.show_help)
        helpmenu.add_separator()
        helpmenu.add_command(label="О программе", command=self.show_about)
        menubar.add_cascade(label="Помощь", menu=helpmenu)
    def exit(self):
        self.master.destroy()
        self.statusbar['text'] = "Выход из приложения"
    def cut(self):
        self.text_box.event_generate('<<Cut>>')
        self.statusbar['text'] = "Вырезано"
    def copy(self):
        self.text_box.event_generate('<<Copy>>')
        self.statusbar['text'] = "Скопировано"
    def paste(self):
        self.text_box.event_generate("<<Paste>>")
        self.statusbar['text'] = "Вставлено"
    def open_parameters(self):
        parameters = Parameters(self)
        parameters.grab_set()
        self.statusbar['text'] = "Открыта вкладка 'Параметры'"
    def create_file(self): # Реализация создания нового зашифрованного файла
        filename = filedialog.asksaveasfilename(defaultextension=".txtx", filetypes=[("Text Files", "*.txtx")])
        if filename:
            config = configparser.ConfigParser()
            config["main"] = {"keyopen": "", "mess": ""}
            with open(filename, "w") as f:
                config.write(f)
                self.statusbar['text'] = "Создан файл " + filename
    def open_file(self): # Реализация открытия зашифрованного файла
        filename = filedialog.askopenfilename(defaultextension=".txtx", filetypes=[("Text Files", "*.txtx")])
        if filename:
            config = configparser.ConfigParser()
            config.read(filename)
            self.text_box.delete("1.0", tk.END)
            self.text_box.insert("1.0", self.xor_encrypt(config["main"]["mess"], self.key))
            self.statusbar['text'] = "Открыт файл " + filename
    def save_file(self): # Реализация сохранения зашифрованного текста в файл
        if not self.filename:
            self.filename = filedialog.asksaveasfilename(defaultextension=".txtx", filetypes=[("Text Files", "*.txtx")])
            if not self.filename: return
        ciphertext = self.xor_encrypt(self.text_box.get("1.0", tk.END), self.key)
        with open(self.filename, "w") as f:
            f.write("[main]\nkeyopen = {}\nmess = {}".format(self.key, ciphertext))
            self.statusbar['text'] = "Сохранён файл " + self.filename
    def show_help(self): # Реализация вывода не модального окна со справкой
        help_text = "Данная программа позволяет создавать, открывать и сохранять файлы с зашифрованным текстом с " \
                    "помощью XOR-шифрования.\n\n" "Чтобы создать новый файл, выберите в меню Файл пункт Создать " \
                    "файл.\n\n" "Чтобы открыть уже существующий файл, выберите в меню Файл пункт Открыть файл и " \
                    "выберите нужный файл в диалоговом окне.\n\n" "Чтобы сохранить изменения в открытом файле, " \
                    "выберите в меню Файл пункт Сохранить файл.\n\n" "Перед использованием программы необходимо " \
                    "ввести личный ключ, который будет использоваться для шифрования и расшифрования текста. Личный " \
                    "ключ можно сохранить, нажав на кнопку Сохранить ключ.\n\n" "Автор: Николай Королёв, БСБО-03-20"
        self.help_window = tk.Toplevel(self.master)
        self.help_window.title("Справка")
        self.help_text_box = tk.Text(self.help_window, wrap=tk.WORD, state=tk.DISABLED)
        self.help_text_box.pack()
        self.help_text_box.configure(state=tk.NORMAL)
        self.help_text_box.insert(tk.END, help_text)
        self.help_text_box.configure(state=tk.DISABLED)
        self.statusbar['text'] = "Открыта вкладка 'Справка'"
    def show_about(self): #Реализация вывода модального окна О программе
        self.statusbar['text'] = "Открыта вкладка 'О программе'"
        about_text = "Блокнот AmTCD\nВерсия: 1.0\n\nАвтор: Николай Королёв"
        tk.messagebox.showinfo(title="О программе", message=about_text)
    def xor_encrypt(self, plaintext, key): # Реализация XOR-шифрования
        ciphertext = ""
        for i in range(len(plaintext)):
            char = plaintext[i]
            key_c = str(key)[i % len(str(key))]
            ciphertext += chr(ord(char) ^ ord(key_c))
        return ciphertext
if __name__ == "__main__":
    root = tk.Tk()
    app = AmTCD(master=root)
    app.mainloop()
