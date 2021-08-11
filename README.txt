Reason for project? 
	I am better able to focus when reading if I reduce my eye movement. Speed reading takes advantage of that by fixing the placement of the outputted sentences.

Implementation (through exe.py):
	1. Starts the GUI. 
	2. Pick a file (through user input).  
	3. Tokenize file into sentences, and then into words.
	4. Create next ouput message with the now-tokenized file. 
	5. Output new output, works by refreshing output every x milliseconds (can be user-specified). 

Available GUI Buttons:
	"Pick File" : Import a file to read from. 
	"Speed Down" : Reduce the refresh rate by 25 milliseconds. 
	"Pause/Resume" : Pauses or resumes the production of new output with a flag, and not by editing the refresh rate. 
	"Speed Up"   : Increase the refresh rate by 25 milliseconds. 
	"Go back 10 Sentences" : Move the sentence_index back by 10. 
	"Remove 1 Word per Output" : Removes 1 word per output. 
	"Add 1 Word per Output" :  Adds 1 word per output. 
	"Decrement Number of Sentences before Change" : Decreases the number of sentences output before its location moves by 1. 
	"Increment Number of Sentences before Change" : Increases the number of sentences output before its location moves by 1.

Testing: 
	test_speed_reader.py: Tests the tokenation of a file, the get_output() function, and the functionality of each button. 
