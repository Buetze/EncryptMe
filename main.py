""" 
source code: main.py
date: 23.10.2019
author: Pascal Duschen
description:
This program will Encrypt a given .txt file and decrypt it with the corresponding password.
the password can be set by the user.
"""
import pyAesCrypt
from os import stat, remove

class Encrypter:
    
    def __init__(self):   
        self.selection = 0          #variable to select from the different actions
        self.switcher = {           #dictionary for the main menu switch
            1: "Encrypt",       
            2: "Decrypt", 
            3: "Write to txt", 
            4: "Exit program"
            }
        self.write_txt_menu = {     #dictionary for the write_txt_menu
            1: "Add line",
            2: "Delete line",
            3: "go back"          
            }
        self.end = "n"              #Flag, Variable to end the Program
        self.filewrite = []         #variable to save the input for the txt file
        self.txt_list = []
        self.file = "test.txt"
        self.buffersize = 64 * 1024
        #title
        print ("--------------------\nWelcome to EncryptMe\n--------------------\n")
        
        #Mainmenu
        while self.end == "n":   
            self.selection = self.select(self.switcher)
            
            if self.selection == 1:
                self.encrypt()               
            elif self.selection == 2:
                self.decrypt()
            elif self.selection == 3:
                self.write_txt()
            elif self.selection == 4:
                print ("bye")
                exit()
            else:
                print("please enter an valid choice")        
    
    
    def select(self, toc): #prints the table of content and gets user input to proceed in program
            for i in toc:
                print (str(i) + ": " + toc[i]) # prints toc based on dictionary defined at the start of the program
            entry = True
            while entry == True:    #check if the entry is of int type
                try:
                    selection = int(input("\nenter: ")) #user input as int
                    entry = False
                except:
                    print ("entry not available")
            
            return selection
        
    def encrypt(self):
        password = input("password: ")
        with open(self.file, "rb") as fIn:
            with open("test.txt.aes", "wb") as fOut:
                pyAesCrypt.encryptStream(fIn, fOut, password, self.buffersize)
                print("done")
        remove(self.file)
                
    def decrypt(self):
        password = input("password: ")
        with open("test.txt.aes", "rb") as fIn:
            with open("test.txt", "wb")as fOut:
                encFileSize = stat("test.txt.aes").st_size
                try:
                    pyAesCrypt.decryptStream(fIn, fOut, password, self.buffersize, encFileSize)
                except ValueError:
                    remove(self.file)
                    
    def write_txt(self):
        while self.end == "n":            
            with open(self.file, "r+") as content:                     #input("enter file name: " )// enter this line to select different files
                data = content.readlines()
                print("\nContent:\n") 
                content.seek(0)   
                for cnt, line in enumerate(content):
                    print("{}: {}".format(cnt +1, line), end='')               
                print("\nwhat would you like to do?")
                  
                self.selection = self.select(self.write_txt_menu)
                if self.selection == 1:                                    #append a line on the end of the file
                    self.filewrite = input("Add an entry ")
                    self.filewrite += "\n"
                    content.write(self.filewrite)    
                elif self.selection == 2:                               #deletes a line based on the number an use inputs
                    to_delete = int(input("Which line should be deleted?: "))
                    content.seek(0)
                    content.truncate()
                    for count, line in enumerate(data):
                        if count+1 != to_delete:
                            content.write(line)

                else:    
                    return
        
     
Encrypter ()