import os
from Detector import main_app
from create_classifier import train_classifer
from create_dataset import start_capture
import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox,PhotoImage
names = set()
names.add('')

# ---------------

# Definiuje ilość zdjęć zbieranych do trenowania klasyfikatora.
#   Wartość domyślna: 300
images_to_capture = 300

# Definiuje poziom pewności dzięki któremu program rozpozna twarz.
#   Wartość jest procentem (0 - 100).
#   Wartość domyślna: 50
confidence_threshold = 50

# ---------------

data_dir = 'data'
userlist_file = 'userlist.txt'
userlist_path = os.path.join(data_dir, userlist_file)

capture_dir = os.path.join(data_dir, 'capture')
classifiers_dir = os.path.join(data_dir, 'classifiers')

class MainUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        global names
        
        try:
            os.makedirs(data_dir)
            os.makedirs(capture_dir)
            os.makedirs(classifiers_dir)
        except FileExistsError:
            pass
        
        try:
            with open(userlist_path, "r+") as f:
                x = f.read()
                z = x.rstrip().split(",")
                z = {el for el in z if el != ""}
                for i in z:
                    names.add(i)
        except FileNotFoundError:           
            with open(userlist_path, "w"):
                pass
        
        self.title_font = tkfont.Font(family='Helvetica', size=16, weight="bold")
        self.title("System rozpoznawania twarzy")
        self.resizable(False, False)
        self.geometry("600x250")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.active_name = None
        container = tk.Frame(self)
        container.grid(sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (StartPage, PageOne, PageTwo, PageThree, PageFour):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno?"):
            global names
            f =  open(userlist_path, "a+")
            for i in names:
                f.write("," + i)
            self.destroy()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="        Strona główna        ", font=self.controller.title_font,fg="#1c3621")
        label.grid(row=0, sticky="ew")
        button1 = tk.Button(self, text="   Utwórz użytkownika  ", fg="#ffffff", bg="#1c3621",command=lambda: self.controller.show_frame("PageOne"))
        button2 = tk.Button(self, text="   Rozpoznaj użytkownika  ", fg="#ffffff", bg="#1c3621",command=lambda: self.controller.show_frame("PageTwo"))
        button3 = tk.Button(self, text="Wyjście", fg="#1c3621", bg="#ffffff", command=self.on_closing)
        button1.grid(row=1, column=0, ipady=3, ipadx=20)
        button2.grid(row=2, column=0, ipady=3, ipadx=20)
        button3.grid(row=3, column=0, ipady=3, ipadx=20)

    def on_closing(self):
        if messagebox.askokcancel("Wyjście", "Czy na pewno?"):
            global names
            with open(userlist_path, "w") as f:
                for i in names:
                    f.write("," + i)
            self.controller.destroy()


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Wprowadź swoje imię", fg="#1c3621", font='Helvetica 12 bold').grid(row=0, column=0, pady=10, padx=5)
        tk.Label(self, text="Bez polskich znaków!", fg="#1c3621", font='Helvetica 9 bold').grid(row=0, column=2, pady=10, padx=5)
        self.user_name = tk.Entry(self, borderwidth=3, bg="lightgrey", font='Helvetica 11')
        self.user_name.grid(row=0, column=1, pady=10, padx=10)
        self.buttoncanc = tk.Button(self, text="Anuluj", bg="#ffffff", fg="#1c3621", command=lambda: controller.show_frame("StartPage"))
        self.buttonext = tk.Button(self, text="Dalej", fg="#ffffff", bg="#1c3621", command=self.start_training)
        self.buttoncanc.grid(row=1, column=0, pady=10, ipadx=5, ipady=4)
        self.buttonext.grid(row=1, column=1, pady=10, ipadx=5, ipady=4)
    
    def start_training(self):
        global names
        if self.user_name.get() == "None":
            messagebox.showerror("Error", "Imię nie może być 'None'")
            return
        elif self.user_name.get() in names:
            messagebox.showerror("Error", "Użytkownik już istnieje!")
            return
        elif len(self.user_name.get()) == 0:
            messagebox.showerror("Error", "Imię nie może być puste!")
            return
        name = self.user_name.get()
        names.add(name)
        self.controller.active_name = name
        self.controller.frames["PageTwo"].refresh_names()
        self.controller.show_frame("PageThree")
        
    def clear(self):
        self.user_name.delete(0, 'end')


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global names
        self.controller = controller
        tk.Label(self, text="Wybierz użytkownika", fg="#1c3621", font='Helvetica 12 bold').grid(row=0, column=0, padx=10, pady=10)
        self.buttoncanc = tk.Button(self, text="Anuluj", command=lambda: controller.show_frame("StartPage"), bg="#ffffff", fg="#1c3621")
        self.selected_name = tk.StringVar(self)
        self.dropdown = tk.OptionMenu(self, self.selected_name, *names)
        self.dropdown.config(bg="lightgrey",width=7)
        self.dropdown["menu"].config(bg="lightgrey")
        self.buttonext = tk.Button(self, text="Dalej", command=self.next_foo, fg="#ffffff", bg="#1c3621")
        self.dropdown.grid(row=0, column=1, ipadx=8, padx=10, pady=10)
        self.buttoncanc.grid(row=1, ipadx=5, ipady=4, column=0, pady=10)
        self.buttonext.grid(row=1, ipadx=5, ipady=4, column=1, pady=10)
        
    def next_foo(self):
        if self.selected_name.get() == 'None':
            messagebox.showerror("ERROR", "Imię nie może być puste.")
            return
        self.controller.active_name = self.selected_name.get()
        print(self.controller.active_name)
        self.controller.show_frame("PageFour")  
        
    def clear(self):
        pass
        
    def nextfoo(self):
        if self.selected_name.get() == 'None':
            messagebox.showerror("ERROR", "Imię nie może być puste.")
            return
        self.controller.active_name = self.selected_name.get()
        self.controller.show_frame("PageFour")

    def refresh_names(self):
        global names
        self.dropdown['menu'].delete(0, 'end')
        for name in names:
            self.dropdown['menu'].add_command(label=name)
            
class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.numimglabel = tk.Label(self, text="Zrobione zdjęcia: 0", font='Helvetica 12 bold', fg="#1c3621")
        self.numimglabel.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)
        self.capturebutton = tk.Button(self, text="Utwórz zbiór danych", fg="#ffffff", bg="#1c3621", command=self.capimg)
        self.trainbutton = tk.Button(self, text="Trenuj Model", fg="#ffffff", bg="#1c3621",command=self.trainmodel)
        self.capturebutton.grid(row=1, column=0, ipadx=5, ipady=4, padx=10, pady=20)
        self.trainbutton.grid(row=1, column=1, ipadx=5, ipady=4, padx=10, pady=20)

    def capimg(self):
        self.numimglabel.config(text=str("Zrobione zdjęcia: 0 "))
        messagebox.showinfo("Instrukcja", "Ustaw twarz przed kamerką i program rozpocznie robienie zdjęć do trenowania modelu.")
        x = start_capture(self.controller.active_name, images_to_capture)
        self.controller.num_of_images = x
        self.numimglabel.config(text=str("Zrobione zdjęcia: "+str(x)))

    def trainmodel(self):
        if self.controller.num_of_images < images_to_capture:
            messagebox.showerror("Błąd", "Niewystarczająca ilość danych. Proszę utworzyć conajmniej " + str(images_to_capture) + " zdjęć!")
            return
        train_classifer(self.controller.active_name)
        messagebox.showinfo("Sukces", "Model został wytrenowany pomyślnie!")
        self.controller.show_frame("PageFour")


class PageFour(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        label = tk.Label(self, text="Rozpoznawanie twarzy", font='Helvetica 16 bold')
        label.grid(row=0,column=0, sticky="ew")
        button1 = tk.Button(self, text="Rozpocznij", command=self.openwebcam, fg="#ffffff", bg="#1c3621")
        button4 = tk.Button(self, text="Wróc na stronę główną", command=lambda: self.controller.show_frame("StartPage"), bg="#ffffff", fg="#1c3621")
        button1.grid(row=1,column=0, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)
        button4.grid(row=1,column=1, sticky="ew", ipadx=5, ipady=4, padx=10, pady=10)

    def openwebcam(self):
        main_app(self.controller.active_name, confidence_threshold)


app = MainUI()
app.iconphoto(True, tk.PhotoImage(file='icon.ico'))
app.mainloop()
