import nltk
from os import system, name
from time import sleep
import time
from termcolor import colored
import tkinter as tk
import random

class Speed_reader:
    def __init__(self, file_name=None, refresh_rate=750) -> None:
        
        def is_file(file_name):
            return True if file_name else False

        self.waiting_for_file_flag = not is_file(file_name)
        self.file_name = file_name

        if is_file(file_name):
            self.list_of_list_of_words = self.initialize_word_list(self.file_name)

        # Default values for text output.
        self.sentence_index, self.word_index = 0, 0
        self.content, self.num_words_per_output, self.end_of_sentence_flag = "", 3, 0
        self.sentence_counter, self.num_sentence_before_place_change = 0, 3

        # Default values for tkinter use. 
        self.refresh_rate = refresh_rate
        self.pause_flag = 0
        self.new_frame_flag = 1
        self.initial_frame_flag = 1

    def initialize_word_list(self, file_name):

        def read_file(file_name): 
            with open(file_name) as f: 
                return f.read()

        def file_into_sentences(file_contents):
            return nltk.sent_tokenize(file_contents)

        def sentences_into_word_lists(sentences):
            def sentence_into_words(sentence):
                return nltk.word_tokenize(sentence)

            word_list = []
            for sentence in sentences : 
                word_list.append( sentence_into_words(sentence) )
            return word_list

        file_contents = read_file(file_name)
        sentences = file_into_sentences(file_contents)
        list_of_list_of_words = sentences_into_word_lists(sentences)
        return list_of_list_of_words

    def reset_file_variables(self):
        self.sentence_index, self.word_index = 0, 0
        self.content, self.num_words_per_output, self.end_of_sentence_flag = "", 3, 0
        self.sentence_counter, self.num_sentence_before_place_change = 0, 3

    def get_output(self, sentenceIndex, innerSentenceIndex, numWordsToOutput):
        sentence = []
        if sentenceIndex < len(self.list_of_list_of_words):
            sentence = self.list_of_list_of_words[sentenceIndex]

        numWordsLeft = len(sentence) - innerSentenceIndex
        outputSize = min(numWordsLeft, numWordsToOutput)

        content = ' '.join(sentence[innerSentenceIndex:innerSentenceIndex + outputSize])

        if numWordsLeft > outputSize:           # next get_output() is the same sentence
            innerSentenceIndex += outputSize
            end_of_sentence_flag = 0
        else:                                   # next get_output() is the next sentence
            innerSentenceIndex = 0
            end_of_sentence_flag = 1
            sentenceIndex += 1

        return content, innerSentenceIndex, end_of_sentence_flag, sentenceIndex

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
                self.content, self.word_index, self.end_of_sentence_flag, self.sentence_index = self.get_output(self.sentence_index, self.word_index, self.num_words_per_output)
            elif self.waiting_for_file_flag:
                if self.file_name == None: pass
                else: 
                    self.reset_file_variables()
                    self.list_of_list_of_words = self.initialize_word_list(self.file_name)
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