import nltk
from os import system, name
from time import sleep
import time
from termcolor import colored
import tkinter as tk
import random

class Speed_reader:
    def __init__(self, file_name=None, refresh_rate=750) -> None:
        
        self.waiting_for_file_flag = 1
        self.file_name = file_name

        if self.file_name != None:
            self.waiting_for_file_flag = 0
            self.initialize_word_list()

        #Setting default values for text output
        self.sentence_index, self.word_index = 0, 0
        self.num_words_per_output = 3
        self.content = ""
        self.end_of_sentence_flag = 0 
        self.sentence_counter = 0
        self.num_sentence_before_place_change = 3

        self.refresh_rate = refresh_rate
        self.pause_flag = 0
        self.new_frame_flag = 1
        self.initial_frame_flag = 1

    def initialize_word_list(self):
        self.file_contents = self.read_file()
        self.all_sentences = self.file_into_sentences()
        self.list_of_list_of_words = self.sentences_into_word_lists()

    def read_file(self): 
        with open(self.file_name) as f: 
            return f.read()
    
    def file_into_sentences(self):
        return nltk.sent_tokenize(self.file_contents)

    def sentence_into_words(self, sentence):
        return nltk.word_tokenize(sentence)

    def sentences_into_word_lists(self):
        word_list = []
        for sentence in self.all_sentences : 
            word_list.append( self.sentence_into_words(sentence) )
        return word_list

    def get_output(self, sentence_index, word_index):
        sentence = []
        if sentence_index < len(self.list_of_list_of_words):
            sentence = self.list_of_list_of_words[sentence_index]

        num_words_left = len(sentence) - word_index

        if num_words_left > self.num_words_per_output:
            output_amount = self.num_words_per_output
        else: 
            output_amount = num_words_left

        content = "" #test2
        for i in range(word_index, word_index+output_amount):
            content += sentence[i] + " "

        if num_words_left > self.num_words_per_output:
            word_index += self.num_words_per_output
            end_of_sentence_flag = 0
            sentence_index += 0
        else: 
            word_index = 0
            end_of_sentence_flag = 1
            sentence_index += 1

        return content, sentence_index, word_index, end_of_sentence_flag

    def change_refresh_rate(self, speed_change):
        if self.refresh_rate + speed_change > 0:
            self.refresh_rate = self.refresh_rate + speed_change

    def flip_pause_flag(self):
        self.pause_flag = not self.pause_flag

    def go_back_x_sentences(self, num_sentences=10):
        if self.sentence_index - num_sentences > 0: 
            self.sentence_index = self.sentence_index - num_sentences
            self.word_index = 0
        else: 
            self.sentence_index = 0
            self.word_index = 0

    def adjust_num_words(self, change):
        if self.num_words_per_output + change > 0: 
            self.num_words_per_output = self.num_words_per_output + change

    def adjust_sentence_placement_num(self, change):
        if self.num_sentence_before_place_change + change >= 1:
            self.num_sentence_before_place_change += change 

    def start_tkinter(self): 
        
        def pick_file(event=None):
            filename = tk.filedialog.askopenfilename()
            if filename:
                self.file_name = filename

        def Load_file():
            file_button = tk.Button(root, text="Pick File", command= pick_file)
            file_button.place(x=5, y=5)

        def Speed_up():
            speed_up_button = tk.Button(root, text="Speed Up", command= lambda: self.change_refresh_rate(-25))
            speed_up_button.place(x=225, y=65)

        def Speed_down():
            speed_down_button = tk.Button(root, text="Speed Down", command= lambda: self.change_refresh_rate(25))
            speed_down_button.place(x=225, y=5)

        def Pause():
            pause_button = tk.Button(root, text="Pause/Resume", command= lambda:self.flip_pause_flag())
            pause_button.place(x=225, y=35)

        def Go_back_ten_sentences():
            go_back_button = tk.Button(root, text = "Go Back 10 Sentences.", command= lambda: self.go_back_x_sentences(10))
            go_back_button.place(x=450, y=5)

        def Increment_num_words_output():
            increment_num_words = tk.Button(root, text = "Add 1 Word per Output", command= lambda: self.adjust_num_words(1))
            increment_num_words.place(x=450, y=35)

        def Decrement_num_words_output():
            decrement_num_words = tk.Button(root, text = "Remove 1 Word per Output", command= lambda: self.adjust_num_words(-1))
            decrement_num_words.place(x=450, y=75)

        def Increment_sentence_number_before_placement_change():
            global increment_sentence_change
            increment_sentence_text = f"Increment number of sentences before change. \n Curr: {self.num_sentence_before_place_change}"
            increment_sentence_change = tk.Button(root, 
                text = increment_sentence_text, 
                command = lambda: self.adjust_sentence_placement_num(1))
            increment_sentence_change.place(x=450, y=95)

        def Decrement_sentence_number_before_placement_change():
            global decrement_sentence_change
            decrement_sentence_change = tk.Button(root, 
                text = f"Decrement number of sentences before change. \n Curr: {self.num_sentence_before_place_change}", 
                command = lambda: self.adjust_sentence_placement_num(-1))
            decrement_sentence_change.place(x=450, y=125)


        def Draw():
            Load_file()
            Speed_down()
            Pause()
            Speed_up()
            Increment_num_words_output()
            Decrement_num_words_output()
            Go_back_ten_sentences()
            Increment_sentence_number_before_placement_change()
            Decrement_sentence_number_before_placement_change()

        def Create_text_frame():
            global text, frame 

            new_x = random.randint(0,700)
            new_y = random.randint(150,400)
            frame=tk.Frame(root,width=100,height=100,relief='flat',bd=1)
            frame.place(x=new_x,y=new_y)
            text=tk.Label(frame)
            text.pack()
            return frame

        def Delete_text_frame(frame):
            frame.place_forget() 

        def Refresher():
            global text, frame
            if not self.pause_flag and not self.waiting_for_file_flag:
                self.content, self.sentence_index, self.word_index, self.end_of_sentence_flag = self.get_output(self.sentence_index, self.word_index)
            elif self.waiting_for_file_flag:
                if self.file_name == None: pass
                else: 
                    self.initialize_word_list()
                    self.waiting_for_file_flag = 0

            if self.new_frame_flag:
                if self.initial_frame_flag: 
                    self.initial_frame_flag = 0
                else:
                    Delete_text_frame(frame)
                Create_text_frame() 
                self.new_frame_flag = 0
            
            text.configure(text=self.content, foreground="red") if self.end_of_sentence_flag  else text.configure(text=self.content, foreground = "black")
            
            increment_sentence_change.configure(text=f"Increment number of sentences before change. \n Curr: {self.num_sentence_before_place_change}")
            decrement_sentence_change.configure(text=f"Decrement number of sentences before change. \n Curr: {self.num_sentence_before_place_change}")
            
            if self.end_of_sentence_flag:
                self.sentence_counter += 1 

            if self.sentence_counter == self.num_sentence_before_place_change:
                self.sentence_counter = 0
                self.new_frame_flag = 1

            root.after(self.refresh_rate, Refresher)

        root = tk.Tk()
        root.geometry("850x500")
        Draw()
        Refresher()
        root.mainloop()