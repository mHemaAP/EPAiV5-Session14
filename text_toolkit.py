import os
import re

def word_frequency(text_or_file, filter_func = None):
    """
    Counts the frequency of each word in the given text, which can be provided 
    as either a string or a file path.
    
    This function processes the text by removing special characters, converting
    it to lowercase, and optionally applying a filter function. It then counts 
    how frequently each word appears in the text or file.

    Parameters:
    text_or_file (str): The input data, which can be either a string of text or
    a file path to a text file.
    filter_func (callable, optional): A function used to filter the words before
    counting their frequency. If not provided, all words are counted. The filter
    function should take a string (word) as input and return `True` to include 
    the word in the count or `False` to exclude it.

    Returns:
    dict: A dictionary where the keys are unique words and the values are their
    corresponding frequency counts.

    Raises:
    TypeError: If `text_or_file` is not a string.
    
    Example usage:
    word_frequency("This is a test text. This test is only a test.", 
    lambda word: len(word) > 2)
    """
    freq_words = {}
    if not isinstance(text_or_file, str):
        raise TypeError ("Only 'str' data with text or filepath allowed")
    
    def count_word_frequency(data:str, filter_func)->None:
        """
        Count the occurrences of each word in the provided string `data`, 
        applying the filter function if provided.

        Parameters:
        data (str): The text to be processed and counted.
        filter_func (callable): A function used to filter words before
        counting.
        """
        nonlocal freq_words
        # Remove all special characters (keeping only letters, numbers, 
        # and spaces)
        string_cleaned = re.sub(r'[^A-Za-z0-9\s]', '', data)
        # convert string data to lower case (to avoid confict between 
        # capital and non-capital words)
        string_cleaned = string_cleaned.lower()

        # Split the text into words
        string_cleaned = string_cleaned.split()

        # Apply the filter function if provided
        string_cleaned = list(filter(filter_func, string_cleaned))

        # For each word in the text
        for data in string_cleaned:
            if data in freq_words.keys():
                freq_words[data] += 1
            else:
                freq_words[data] = 1
    
    # Function supports only two types of strings
    #   1. A valid file path - If exists it reads and processes it
    #   2. A text data - It processes directly
    if os.path.isfile(text_or_file):
        # Open the file, read each line and send for processing
        with open(text_or_file, 'r') as file:
            for row in file:
                count_word_frequency(row, filter_func)

    else:
       # Text data, send the raw text for processing
       count_word_frequency(text_or_file, filter_func)

    return freq_words

def unique_words(text_or_file):
    """
    Extract unique words from a given text or file path.

    Parameters:
        text_or_file (str): Input can either be a string containing text or 
                            a file path to a text file.

    Returns:
        set: A set of unique words in lowercase from the input text.
    
    Raises:
        TypeError: If the input is not a string.
        IOError: If the file path provided is invalid or cannot be read.
    """
    unique_words_txt = set()

    if not isinstance(text_or_file, str):
        raise TypeError ("Only 'str' data with text or filepath allowed")
    
    def count_unique_words(data:str):
        nonlocal unique_words_txt

        # Remove all special characters (keeping only letters, numbers, 
        # and spaces)
        string_cleaned = re.sub(r'[^A-Za-z0-9\s]', '', data)

        # convert string data to lower case (to avoid confict between 
        # capital and non-capital words)
        string_cleaned = string_cleaned.lower()
        curr_unique_words = set(string_cleaned.split())

        # create unique word set
        unique_words_txt = unique_words_txt.union(curr_unique_words)


    # If it is a path or file, send each row for processing
    if os.path.isfile(text_or_file):
        try:
            with open(text_or_file, 'r') as file:
                for row in file:
                    count_unique_words(row)
        except IOError as e:
            raise IOError(f"Error reading file: {e}")
    
    else:
        count_unique_words(text_or_file)

    return unique_words_txt


def word_co_occurrence_matrix(text_or_file, window=2)-> list:
    """
    Returns the word co-ocurrence matrix from a given text or file path.

    Parameters:
        text_or_file (str): Input can either be a string containing text or 
                            a file path to a text file.
        window(int): The window size for fetching adjecent words

    Returns:
        list: A list containing tuples of word co-occurance matrix.
    
    Raises:
        TypeError: If the input is not a string.
        IOError: If the file path provided is invalid or cannot be read.
    """
    if not isinstance(text_or_file, str):
        raise TypeError ("Only 'str' data with text or filepath allowed")
    
    if not isinstance(window, int):
        raise TypeError ("For \'window\', only integer are allowed")
    
    co_words_list = []

    def process_co_occurance(data: str, window: int):
        ''' Creates the list of tuples containing word cooccurence pairs
        '''

        nonlocal co_words_list

        # Clean up special charecters and lower the case
        string_cleaned = re.sub(r'[^A-Za-z0-9\s]', '', data).lower()
        string_cleaned = string_cleaned.split()

        # form the pair
        for index in range(len(string_cleaned)-window):
            co_word_pair = tuple(string_cleaned[index:index + window])
            co_words_list.append(co_word_pair)

    # If it is a path or file, send each row for processing
    if os.path.isfile(text_or_file):
        try:
            with open(text_or_file, 'r') as file:
                for row in file:
                    process_co_occurance(row, window)
        except IOError as e:
            raise IOError(f"Error reading file: {e}")
    
    else:
        process_co_occurance(text_or_file, window)


    return co_words_list


def text_generator(text_or_file):
    """
    A generator function that yields one line of text at a time, either from a 
    file or a string.

    If `text_or_file` is a file path, the function opens the file and yields 
    each line. 
    If `text_or_file` is a plain string, it cleans up special characters, 
    converts the string to lowercase, splits it into lines, and then yields 
    each cleaned line.

    Parameters:
    text_or_file (str): The input data, which can be either a file path 
    or a string.

    Yields:
    str: One line of text at a time, either from the file or the cleaned 
    string.

    Raises:
    TypeError: If the input is not a string or file path.
    IOError: If there is an error opening or reading from the file.
    """

    if not isinstance(text_or_file, str):
        raise TypeError ("Only 'str' data with text or filepath allowed")
    
    if (os.path.isfile(text_or_file)):
        try:
            with open(text_or_file, 'r') as file:
                for row in file:
                    yield row
        except IOError as e:
            print(f"Error reading file: {e}")

    else:
        # Clean up special charecters and lower the case
        string_cleaned = re.sub(r'[^A-Za-z0-9\s]', '', text_or_file).lower()
        string_cleaned = string_cleaned.split('\n')

        for data in string_cleaned:
            yield data