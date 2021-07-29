import nltk
from os import system, name
from time import sleep
import time
from termcolor import colored
import tkinter as tk

class Speed_reader:
    def __init__(self, file_name) -> None:
        
        self.file_name = file_name
        self.file_contents = self.read_file()
        
        self.all_sentences = self.file_into_sentences()
        self.list_of_list_of_words = self.sentences_into_list_of_words()

        self.sentence_index = 0
        self.word_index = 0

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
        else: return 

        i = word_index

        if len(sentence) - i > 3:
            content = sentence[i] + " " + sentence[i+1] + " " + sentence[i+2]
            i += 3
            end_of_sentence_flag = 0
        elif len(sentence) - i == 3:
            content = sentence[i] + " " + sentence[i+1] + " " + sentence[i+2]
            sentence_index += 1
            i = 0
            end_of_sentence_flag = 1
        elif len(sentence) - i == 2: 
            content = sentence[i] + " " + sentence[i+1]
            sentence_index += 1
            i = 0
            end_of_sentence_flag = 1
        else:
            content = sentence[i]
            sentence_index += 1
            i = 0
            end_of_sentence_flag = 1
        return content, sentence_index, i, end_of_sentence_flag

    def start_tkinter(self): 
        
        def Draw():
            global text

            frame=tk.Frame(root,width=100,height=100,relief='solid',bd=1)
            frame.place(x=10,y=10)
            text=tk.Label(frame)
            text.pack()

        def Refresher():
            global text 

            content, self.sentence_index, self.word_index, end_of_sentence_flag = self.get_output(self.sentence_index, self.word_index)
            text.configure(text=content, foreground="red") if end_of_sentence_flag  else text.configure(text=content, foreground = "black")
            
            root.after(500, Refresher)


        root = tk.Tk()
        Draw()
        Refresher()
        root.mainloop()
    