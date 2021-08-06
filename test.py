from speed_reader import Speed_reader
import unittest

class TestSpeedReader(unittest.TestCase):
    def test_list_init(self):
        pass

    def test_initialize_word_list(self):
        
        test_empty_file_read = Speed_reader("Test_files/empty_msg.txt")
        empty_file_contents = test_empty_file_read.initialize_word_list(test_empty_file_read.file_name)
        self.assertEqual(empty_file_contents, [])

        test_file_read = Speed_reader("Test_files/short_msg.txt")
        short_msg_contents = test_file_read.initialize_word_list(test_file_read.file_name)
        self.assertEqual(short_msg_contents, [['This', 'is', 'a', 'short', 'message', '.'], 
                                        ['The', 'program', 'should', 'be', 'able', 'to', 'split', 'this', 'up', '.'],
                                        ['Let', "'s", 'see', 'if', 'it', 'can', 'do', 'it', '.']])
        
    def test_get_output(self):
        pass

    def test_button_inner_functionality(self):
        pass

    def test_tkinter(self):
        pass

    
if __name__ == '__main__':
    Speed_reader("Test_files/test_data.txt")
    unittest.main()
