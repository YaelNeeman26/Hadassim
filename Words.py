import re
import matplotlib.colors as mcolors
from stop_words import get_stop_words
from word2number import w2n

class Words:
    def __init__(self, input_file):
        sum = max_sum = empty_lines = is_color = 0
        seq_k = temp_seq = ''
        text = []
        # Open data file
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            # Keeps the data
            for num_line, line in enumerate(f):
                text.append(line)

            # Check if the text contains only letters and numbers
            for num_line, line in enumerate(text):
                text_words = re.split(r'[^A-Za-z0-9]+', line)
                text[num_line] = [word.lower() for word in text_words if word != '']

            # Create the dictionary
            words_dict = {}
            for line in text:

                # Not counting blank lines
                if line == []:
                    empty_lines += 1
                    continue

                for token in line:
                    # The maximum sequence of words without the letter k
                    if 'k' in token or 'K' in token:
                        if sum > max_sum:
                            max_sum = sum
                            seq_k = temp_seq
                            temp_seq = ''
                        sum = 0
                    else:
                        temp_seq += token + ' '
                        sum += 1

                    # In case the word not exist in the dictionary
                    if token not in words_dict:
                        # Checks if the word is color
                        if mcolors.is_color_like(token):
                            is_color = 1
                        words_dict[token] = (1, is_color) # appears, color?
                        is_color = 0
                    # In case the word exists in the dictionary
                    else:
                        words_dict[token] = (words_dict[token][0] + 1, words_dict[token][1])
         
            self.num_lines = num_line + 1 - empty_lines 
            self.dict = words_dict
            self.sen_without_k = temp_seq if sum > max_sum else seq_k
    
    # 1. Number of lines in the text
    def number_of_lines(self):
        return self.num_lines

    # 2 - 3. Number of words in the text
    def num_of_words(self):
        count_words = count_unique_words = 0
        for key in self.dict:
            appears = self.dict[key][0]   
            if appears == 1:
                count_unique_words += 1
            count_words += appears
        return count_words, count_unique_words

    # 4. Avarage and max length
    def sentence_length(self, input_file):
        sum_len = max_len = 0
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read().replace('\n', ' ') 
            sentences = re.split('[.,;]',text) # Separation between sentences
            for sen in sentences:
                words_in_sen = sen.split()
                len_sen = len(words_in_sen)
                if len_sen > max_len:
                    max_len = len_sen
                sum_len += len_sen
        avarage_length = sum_len / len(sentences) 
        return avarage_length, max_len
    
    # 5. Popular word
    def popular_word(self):  
        max = max_stopword = 0 # max_stopword, that can be stopword
        stop_words = get_stop_words('en')
        for key in self.dict:
            key_appears = self.dict[key][0]
            # The word is stopword
            if key in stop_words:
                if key_appears > max_stopword:
                    max_stopword = key_appears
                    popular_stopword = key
            else:
                if key_appears > max:
                    max = key_appears
                    popular_word = key
        if max > max_stopword:
            popular_stopword = popular_word

        # All words are stopwords
        if max == 0:
            popular_word = 'All words are stopwords!!!'

        return popular_stopword, popular_word

    # 6. The maximum sequence of words without the letter k
    def seq_without_k(self):
        return self.sen_without_k

    # 7. Returns the max number
    def max_number(self, input_file):
        numbers = []

        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            split_text = re.split(r'[^A-Za-z0-9-]+', f.read()) # Remove all special chars except '-'
            for word in split_text:
                try:
                    numbers.append(w2n.word_to_num(word))
                except ValueError as e:
                    continue
      
        return max(numbers)

    # 8. The list of colors and the amount of them appearing at the text
    def colors(self):
        colors_dict = {}
        for key in self.dict:
            # The func mcolors.is_color_like returns the true value on such strings
            if key == 'none' or len(key) <= 1 or key.isdigit(): 
                continue
            if self.dict[key][1] == 1:
                colors_dict[key] = self.dict[key][0]
        return colors_dict

    

if __name__ == '__main__':
    w = Words('short.txt')

    with open('output.txt', 'w') as f_o:
        f_o.write('Output:\n')
        f_o.write(f'1. Number of lines: {w.number_of_lines()}\n')
        count_words, count_unique_words = w.num_of_words()
        f_o.write(f'2. Number of words: {count_words}\n')
        f_o.write(f'3. Number of unique words: {count_unique_words}\n')
        avarage_len, max_len = w.sentence_length('short.txt')
        f_o.write(f'4. Average sentence length: {avarage_len}\n')
        f_o.write(f'   Maximum sentence length: {max_len}\n')
        popular_stopword, popular_word = w.popular_word()
        f_o.write(f'5. Popular word: {popular_stopword}\n')
        f_o.write(f'   Popular word (not stopword): {popular_word}\n')
        seq = w.seq_without_k()
        f_o.write(f'6. Maximum sequence of words without k: {seq}\n')
        max_num = w.max_number('short.txt')
        f_o.write(f'7. Max number: {max_num}\n')
        f_o.write(f'8. Color list: {w.colors()}')







