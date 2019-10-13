"""
source code: main.py
date: 13.10.2019
author: Pascal Duschen
description:
This program takes input of two given argument, stores them and creates or loads an encrypted file.
"""
import pyAesCrypt
import tkinter as tk
from os import stat, remove

class EncryptMe:

    def __init__(self, parent):
        self.root = parent
        self.password_list = {}
        self.password_labels = {}
        self.index_labels = []
        self.header_buttons = []
        self.file = ""
        self.password = ""
        self.new_file = ""
        self.filewrite = []
        self.txt_list = []
        self.buffersize = 64 * 1024

        self.title = parent.title("encryptme")
        self.top_frame = tk.Frame(root, width=400, height=50)
        self.center_frame = tk.Frame(root, width=400, height=350, bg="white")
        self.bottom_frame = tk.Frame(root, width=400, height=50)
        self.top_frame.grid(row=0, sticky="ew")
        self.center_frame.grid(row=1, sticky="nsew")
        self.bottom_frame.grid(row=3, sticky="ew")
        self.center_frame.grid_columnconfigure(12, minsize=10)
        self.bottom_frame.grid_columnconfigure(2, minsize=400)

        self.header(self.top_frame)
        self.bottom(self.bottom_frame)
        self.create_design(self.center_frame)


    def create_Test_File(self):
        for i in range(0, 20):
            self.password_list.append(["arg" + str(i), "pw" + str(i)])
        f = open("test.txt", "w+")
        for list in self.password_list:
            for element in list:
                f.write("{0!s}\n".format(element))
        print("file created")

    def load_file(self, frame):
        window = tk.Toplevel(frame)
        tk.Label(window, text="enter file name: ").grid(row=0)
        tk.Label(window, text="enter password: ").grid(row=1)
        tk.Button(window, text="load file", command=lambda: load_me()).grid(row=3)
        tk.Button(window, text="exit", command=lambda: window.destroy()).grid(row=3, column=1)
        in1 = tk.Entry(window)
        in2 = tk.Entry(window)
        in1.grid(row=0, column=1)
        in2.grid(row=1, column=1)


        def load_me():
            self.password_list = {}
            self.file = in1.get()
            self.password = in2.get()
            minor_list = []
            number = 1
            for i in self.password_labels:
                lab = self.password_labels[i]
                lab[0].destroy()
                lab[1].destroy()
            for i in self.index_labels:
                i.destroy()
            self.decrypt()
            with open(self.file + ".txt", "r+") as content:
                for line in content.readlines():
                    minor_list.append(line[:-1])
                while len(minor_list) > 0:
                    for i in minor_list:
                        entry = minor_list[0:2]
                        self.password_list.update({ number : [entry[0], entry[1]]})
                        number += 1
                        del minor_list[:2]
            remove(self.file + ".txt")
            self.create_design(self.center_frame)
            window.destroy()

    def save_file(self, frame):
        window = tk.Toplevel(frame)
        tk.Label(window, text="enter file name: ").grid(row=0)
        tk.Label(window, text="enter password: ").grid(row=1)
        tk.Button(window, text="save file", command=lambda: save_me()).grid(row=3)
        tk.Button(window, text="exit", command=lambda: window.destroy()).grid(row=3, column=1)
        in1 = tk.Entry(window)
        in2 = tk.Entry(window)
        in1.grid(row=0, column=1)
        in2.grid(row=1, column=1)

        def save_me():
            self.new_file = in1.get()
            self.password = in2.get()
            with open(self.new_file, "w") as file:
                for i in self.password_list:
                    for a in self.password_list[i]:
                        write = a + "\n"
                        file.writelines(write)
                        write = ""
            self.encrypt()

    def encrypt(self):
        password = self.password
        with open(self.new_file, "rb") as fIn:
            with open(self.new_file+".txt.aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, password, self.buffersize)
                print("done")
        remove(self.new_file)

    def decrypt(self):
        password = self.password
        with open(self.file+ ".txt.aes", "rb") as fIn:
            with open(self.file + ".txt", "wb")as fOut:
                encFileSize = stat(self.file + ".txt.aes").st_size
                try:
                    pyAesCrypt.decryptStream(fIn, fOut, password, self.buffersize, encFileSize)
                except ValueError:
                    remove(self.file)

    def add_entry(self, frame):
        window = tk.Toplevel(frame)
        tk.Label(window, text="Site: ").grid(row=0)
        tk.Label(window, text="Password: ").grid(row=1)
        tk.Button(window, text="add",command=lambda:adding()).grid(row=3)
        tk.Button(window, text="exit",command=lambda:window.destroy()).grid(row=3, column=1)
        in1 = tk.Entry(window)
        in2 = tk.Entry(window)
        in1.grid(row=0,column=1)
        in2.grid(row=1,column=1)

        def adding():
            position = len(self.password_list) + 1
            self.password_list.update({position : [in1.get(), in2.get()]})
            self.create_design(self.center_frame)

    def delete(self, frame):
        window = tk.Toplevel(frame)
        tk.Label(window, text="line: ").grid(row=0)
        tk.Button(window, text="delete", command=lambda: delete_me()).grid(row=2)
        tk.Button(window, text="exit", command=lambda: window.destroy()).grid(row=2, column=1)
        in1 = tk.Entry(window)
        in1.grid(row=0, column=1)

        def delete_me():
            num = int(in1.get())
            self.password_list.pop(int(in1.get()))
            in_lab = self.index_labels.pop(num-1)
            in_lab.destroy()
            lab = self.password_labels.pop(num)
            lab[0].destroy()
            lab[1].destroy()
            self.create_design(self.center_frame)

    def bottom(self, frame):

        self.open_button = tk.Button(frame, text="load file", command=lambda: self.load_file(self.center_frame))
        self.save_button = tk.Button(frame, text="save file", command=lambda: self.save_file(self.center_frame))
        self.close = tk.Button(frame, text="exit program", command=lambda: exit())
        self.open_button.grid(row=0, column=0, padx=10, pady=10)
        self.save_button.grid(row=0, column=1, padx=10, pady=10)
        self.close.grid(row=0, column=3, padx=10, pady=10)

    def header(self, frame):
        auto_column = 0
        head = ["add", "delete"]

        for i in head:
            button = tk.Button(frame, text=i)
            button.grid(row=0, column=auto_column, padx=10, pady=10)
            auto_column += 1
            self.header_buttons.append(button)

        self.header_buttons[0].configure(command=lambda: self.add_entry((self.center_frame)))
        self.header_buttons[1].configure(command=lambda: self.delete((self.center_frame)))

    def create_design(self, frame):
        auto_column = 0     # lay out Labels
        auto_row = 0        # lay out Labels
        sor_list = []       # Used to sort pw list
        num = 1             # Used to sort pw list

        # sort password list for continuing numbers
        for i in self.password_list:
            sor_list.append(self.password_list[i])
        self.password_list.clear()
        for i in sor_list:
            self.password_list.update({num : [i[0], i[1]]})
            num += 1

        # destroy all labels
        for label in self.password_labels:
            for i in self.password_labels[label]:
                i.destroy()
        for index in self.index_labels:
            index.destroy()
        self.password_labels.clear()

        # create labels for index, site and pw
        for i in self.password_list:
            entry = self.password_list[i]
            self.password_labels.update({i:
            [tk.Label(frame, text=entry[0], bg="white"), tk.Label(frame, text=entry[1], bg="white")]})
        for i in (self.password_labels):
            auto_row += 1
            index_nr = tk.Label(frame, text=i, bg="white")
            index_nr.grid(row=auto_row, column=auto_column)
            self.index_labels.append(index_nr)
            entry = self.password_labels[i]
            entry[0].grid(row=auto_row, column=auto_column+1)
            entry[1].grid(row=auto_row, column=auto_column+2)
            if auto_row % 11 == 0:
                auto_column += 4
                auto_row = 0
                frame.grid_columnconfigure(auto_column - 1, minsize=40)



root = tk.Tk()
EncryptMe(root)
root.mainloop()