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
        self.refreshRate = refresh_rate
        self.pauseFlag = 0
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

    def changeRefreshRate(self, refreshRate, speedChange):
        if refreshRate + speedChange > 0:
            self.refreshRate = refreshRate + speedChange
            return refreshRate + speedChange
        return refreshRate

    def flipPauseFlag(self, pauseFlag):
        self.pauseFlag = not pauseFlag
        return not pauseFlag

    def displaceSentenceIndex(self, sentenceIndex, numSentences=-10):
        if sentenceIndex + numSentences > 0: 
            sentenceIndex = sentenceIndex + numSentences
        else: 
            sentenceIndex = 0

        self.word_index = 0
        self.sentence_index = sentenceIndex
        return sentenceIndex

    def changeNumWordsOutput(self, numWordsOutput, change):
        if numWordsOutput + change > 0: 
            self.num_words_per_output = numWordsOutput + change
            return numWordsOutput + change
        return numWordsOutput

    def changeNumSentencesPerPlacement(self, numSentencesPlacedPerLoc, change):
        if numSentencesPlacedPerLoc + change >= 1:
            self.num_sentence_before_place_change = numSentencesPlacedPerLoc + change
            return numSentencesPlacedPerLoc + change
        return numSentencesPlacedPerLoc

    def start_tkinter(self): 
        
        def pick_file(event=None):
            filename = tk.filedialog.askopenfilename()
            if filename:
                self.file_name = filename

        def Load_file():
            file_button = tk.Button(root, text="Pick File", command= pick_file)
            file_button.place(x=5, y=5)

        def Speed_up():
            speed_up_button = tk.Button(root, text="Speed Up", command= lambda: self.changeRefreshRate(self.refreshRate, -25))
            speed_up_button.place(x=225, y=65)

        def Speed_down():
            speed_down_button = tk.Button(root, text="Speed Down", command= lambda: self.changeRefreshRate(self.refreshRate, 25))
            speed_down_button.place(x=225, y=5)

        def Pause():
            pause_button = tk.Button(root, text="Pause/Resume", command= lambda:self.flipPauseFlag(self.pauseFlag))
            pause_button.place(x=225, y=35)

        def Go_back_ten_sentences():
            go_back_button = tk.Button(root, text = "Go Back 10 Sentences.", command= lambda: self.displaceSentenceIndex(self.sentence_index, 10))
            go_back_button.place(x=450, y=5)

        def Increment_num_words_output():
            increment_num_words = tk.Button(root, text = "Add 1 Word per Output", command= lambda: self.changeNumWordsOutput(self.num_words_per_output, 1))
            increment_num_words.place(x=450, y=35)

        def Decrement_num_words_output():
            decrement_num_words = tk.Button(root, text = "Remove 1 Word per Output", command= lambda: self.changeNumWordsOutput(self.num_words_per_output, -1))
            decrement_num_words.place(x=450, y=75)

        def Increment_sentence_number_before_placement_change():
            global increment_sentence_change
            increment_sentence_text = f"Increment number of sentences before change. \n Curr: {self.num_sentence_before_place_change}"
            increment_sentence_change = tk.Button(root, 
                text = increment_sentence_text, 
                command = lambda: self.changeNumSentencesPerPlacement(self.num_sentence_before_place_change, 1))
            increment_sentence_change.place(x=450, y=95)

        def Decrement_sentence_number_before_placement_change():
            global decrement_sentence_change
            decrement_sentence_change = tk.Button(root, 
                text = f"Decrement number of sentences before change. \n Curr: {self.num_sentence_before_place_change}", 
                command = lambda: self.changeNumSentencesPerPlacement(self.num_sentence_before_place_change, -1))
            decrement_sentence_change.place(x=450, y=125)

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

        def Refresher():

            if not (self.pauseFlag or self.waiting_for_file_flag):
                self.content, self.word_index, self.end_of_sentence_flag, self.sentence_index = self.get_output(self.sentence_index, self.word_index, self.num_words_per_output)
            elif self.waiting_for_file_flag and self.file_name != None:
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
            
            _foreground = "red" if self.end_of_sentence_flag else  "black"
            text.configure(text=self.content, foreground= _foreground) if self.end_of_sentence_flag  else text.configure(text=self.content, foreground = _foreground)
            
            increment_sentence_change.configure(text=f"Increment number of sentences before change. \n Curr: {self.num_sentence_before_place_change}")
            decrement_sentence_change.configure(text=f"Decrement number of sentences before change. \n Curr: {self.num_sentence_before_place_change}")
            
            if self.end_of_sentence_flag:
                self.sentence_counter += 1 

            if self.sentence_counter == self.num_sentence_before_place_change:
                self.sentence_counter = 0
                self.new_frame_flag = 1

            root.after(self.refreshRate, Refresher)

        root = tk.Tk()
        root.geometry("850x500")
        Draw()
        Refresher()
        root.mainloop()