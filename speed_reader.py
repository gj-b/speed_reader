import nltk
from os import system, name
from time import sleep
import time
from termcolor import colored
import tkinter as tk

class Speed_reader:
    def __init__(self, file_name, text_speed=500) -> None:
        
        self.file_name = file_name
        self.file_contents = self.read_file()
        
        self.all_sentences = self.file_into_sentences()
        self.list_of_list_of_words = self.sentences_into_list_of_words()

        self.sentence_index = 0
        self.word_index = 0
        self.content = ""
        self.end_of_sentence_flag = 0

        self.text_speed = text_speed
        self.pause_flag = 0

    def read_file(self): 
        with open(self.file_name) as f: 
            return f.read()
    
    def file_into_sentences(self):
        return nltk.sent_tokenize(self.file_contents)

    def sentence_into_words(self, sentence):
        return nltk.word_tokenize(sentence)

    def sentences_into_list_of_words(self):
        word_list = []
        for sentence in self.all_sentences : 
            word_list.append( self.sentence_into_words(sentence) )
        return word_list

    def get_output(self, sentence_index, word_index):
        if sentence_index < len(self.list_of_list_of_words):
            sentence = self.list_of_list_of_words[sentence_index]
        else: 
            sentence = []

        num_words_left = len(sentence) - word_index
        i = word_index

        if num_words_left >= 3:
            content = sentence[i] + " " + sentence[i+1] + " " + sentence[i+2]
        elif num_words_left == 2: 
            content = sentence[i] + " " + sentence[i+1]
        elif num_words_left == 1: 
            content = sentence[i]
        else: 
            content = ""

        if num_words_left > 3:
            i +=3
            end_of_sentence_flag = 0
            sentence_index += 0
        else: 
            i = 0
            end_of_sentence_flag = 1
            sentence_index += 1

        return content, sentence_index, i, end_of_sentence_flag

    def change_text_speed(self, speed_change):
        if self.text_speed + speed_change > 0:
            self.text_speed = self.text_speed + speed_change

    def change_pause_flag(self):
        self.pause_flag = not self.pause_flag

    def go_back_x_sentences(self, num_sentences=10):
        if self.sentence_index - num_sentences > 0: 
            self.sentence_index = self.sentence_index - num_sentences
            self.word_index = 0

    def start_tkinter(self): 
        
        def Speed_up():
            speed_up_button = tk.Button(root, text="Speed Up", command= lambda: self.change_text_speed(-25))
            speed_up_button.pack()

        def Speed_down():
            speed_down_button = tk.Button(root, text="Speed Down", command= lambda: self.change_text_speed(25))
            speed_down_button.pack()

        def Pause():
            pause_button = tk.Button(root, text="Pause", command= lambda:self.change_pause_flag())
            pause_button.pack()

        def Go_back_ten_sentences():
            go_back_button = tk.Button(root, text = "Go Back", command= lambda: self.go_back_x_sentences(10))
            go_back_button.pack()

        def Draw():
            global text
            
            Speed_down()
            Pause()
            Speed_up()
            
            Go_back_ten_sentences()

            frame=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
            frame.place(x=200,y=200)
            text=tk.Label(frame)
            text.pack()

            

        def Refresher():
            global text 
            if not self.pause_flag:
                self.content, self.sentence_index, self.word_index, self.end_of_sentence_flag = self.get_output(self.sentence_index, self.word_index)
                
            text.configure(text=self.content, foreground="red") if self.end_of_sentence_flag  else text.configure(text=self.content, foreground = "black")
            
            root.after(self.text_speed, Refresher)


        root = tk.Tk()
        root.geometry("500x500")
        Draw()
        Refresher()
        root.mainloop()