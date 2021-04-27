#!/usr/bin/env python3

__version__ = 'cado v0.1.0'

# Content Aware Downloads Organizer (CADO)
# Attempts to organize your downloads folder in two parts
# First into sub-folders by file extension, then by
# content in human-readable files (PDFs, Docx, etc.)
# Author: Logan D.G. Smith

import argparse
import docx
import getpass
import nltk
import os
import platform
import PyPDF2

from pathlib import Path

class TextClassifier:
    def __init__(self):
        self.classifier = None
        self.training_folder = 'training_docs'
        self.subjects = []
        self.subject_words = [] # Subject specific word dictionaries
        self.subject_dictionary = {}

    def train(self):
        # Format and organize the words
        training_files = [os.path.join(self.training_folder, file) for file in os.listdir(self.training_folder) if os.path.isfile(os.path.join(self.training_folder, file))]
        for file in training_files:
            self.subjects.append(file.replace('.txt', '').replace('training_docs/', ''))
            with open(file) as this_file:
                self.subject_words.append(this_file.readlines())
        
        # Strip and tag the words
        for index, word_sets in enumerate(self.subject_words):
            new_set = []
            for word in word_sets:
                stripped_word = word.strip('\n').lower()
                new_set.append((stripped_word, self.subjects[index]))
                self.subject_dictionary[stripped_word] = index
            self.subject_words[index] = new_set

        # Feature Extraction
        feature_sets = []
        for subjects in self.subject_words:
            feature_sets += [(self.matching_features(line), subject) for (line, subject) in subjects]

        self.classifier = nltk.NaiveBayesClassifier.train(feature_sets)

    def predict(self, lines: list) -> str:
        if self.classifier == None:
            print('No classifier is initialized! You must call train() before predict()!')
            return

        return self.classifier.classify(self.matching_features(lines))

    # Naive classification of text based on the similarity to subject
    def matching_features(self, line: str):
        scores = [0] * len(self.subjects)

        if(type(line) == list):
            for word in line:
                subject_index = self.subject_dictionary.get(word, -1)
                if subject_index == -1:
                    continue
                scores[subject_index] += 1
        else:
            subject_index = self.subject_dictionary.get(line, -1)
            if subject_index > -1:
                scores[subject_index] += 1

        most_like = 0
        highest_score = -1
        for index, score in enumerate(scores):
            if score > highest_score:
                highest_score = score
                most_like = index
        
        # Returning the scores
        return {'subject' : self.subjects[most_like]}


def read_docx(path: str) -> list:
    """Reads a docx and returns list of non-symbol words"""
    try:
        doc = docx.Document(path)
        lines = [paragraph.text for paragraph in doc.paragraphs]
    except:
        lines = ''
    
    # Read lines of the word doc
    words = []
    for line in lines:
        if line != '':
            words += nltk.word_tokenize(line)

    return strip_symbols(words)

def read_pdf(path: str) -> list:
    """Reads a pdf and returns list of non-symbol words"""
    try:
        # Open the PDF
        with open(path, 'rb') as pdf:
            # Read the contents of the PDF
            pdf = PyPDF2.PdfFileReader(pdf)
            pages = []
            for x in range(pdf.numPages):
                page = pdf.getPage(x).extractText().replace('\n', '')
                pages += nltk.word_tokenize(page)
    except:
        pages = []

    return strip_symbols(pages)

def read_txt(path: str) -> list:
    """Read text files"""
    textstr = ''
    try:
        with open(path, 'r') as txt:
            textstr = txt.read()
    except:
        textstr = ''
    
    return strip_symbols(nltk.word_tokenize(textstr))

def strip_symbols(text: list) -> list:
    """Strip symbols from a list of words and put words in lowercase"""
    tokens = []
    for word in text:
        if word not in '!@#$%^&*(),<>./\'\"\\':
            tokens.append(word.lower())
    return tokens

def create_test_files(test_path):
    """Creates a number of empty files for testing the file extension sorting"""
    # Quick filetype declaration
    print('Creating test files...')
    file_types = {
        '.pdf'  : 'PDFs',   # PDF
        '.docx' : 'Docs',   # MS Word post-2007
        '.doc'  : 'Docs',   # MS Word pre-2007
        '.txt'  : 'Docs',   # Text Document
        '.md'   : 'Docs',   # Markdown File
        '.exe'  : 'Bin',    # Windows Executable
        '.sh'   : 'Bin',    # BASH Script
        '.fish' : 'Bin',    # Fish Shell Script
        ''      : 'Bin',    # Probably a script
        '.py'   : 'Source', # Python (You can change this to 'Bin' if you want)
        '.rs'   : 'Source', # Rust
        '.c'    : 'Source', # C
        '.cpp'  : 'Source', # C++
        '.cs'   : 'Source', # C#
        '.java' : 'Source', # Java
        '.js'   : 'Source', # Javascript
        '.jpg'  : 'Images', # Needs more JPG
        '.jpeg' : 'Images', # JPG with an accent
        '.png'  : 'Images', # The cooler JPG
        '.tmp'  : 'Temp',   # Temp files
        '.zip'  : 'Misc'
    }

    # Creating filenames from keys
    for key in file_types.keys():
        filename = key[1:] + '_test' + key
        Path(os.path.join(test_path, filename)).touch()

def classify_files(path: str) -> list:
    """Classifies files and sorts them into subfolders"""
    # Initializations
    classifier = TextClassifier()
    classifier.train()
    classifications = set() # Folders to create
    file_classifications = [] # Tuples of (filename, classification) 

    # Attempt to collect files
    files = [file for file in os.listdir(path) if os.path.isfile(os.path.join(path, file))]
    
    # Attempt to read files
    for file in files:
        text = []
        classification = 'Misc'
        if file.endswith('.docx'):
            text = read_docx(file)
        elif file.endswith('.pdf'):
            text = read_pdf(file)
        elif file.endswith('.txt'):
            text = read_txt(file)

        if text:
            classification = classifier.predict(text)
        
        classifications.add(classification)
        file_classifications.append((file, classification))

    # Create folders if they don't exist
    for folder in classifications:
        print(f'  Attempting to Create {os.path.join(path, folder)}...')
        Path(os.path.join(path, folder)).mkdir(parents=True, exist_ok=True)

    # Sort the files into their folders
    for file, classification in file_classifications:
        # Define the source and destination
        folder_to = os.path.join(path, classification)
        folder_to = os.path.join(folder_to, file)
        folder_from = os.path.join(path, file)

        # Debugging output
        print(f'    FROM: {folder_from}')
        print(f'      TO: {folder_to}')

        # Rename (move) the file to the new folder
        os.rename(folder_from, folder_to)

def file_content_sort(downloads_path):
    """Sorts the files in subdirectories based on content"""
    docs_path = os.path.join(downloads_path, 'Docs')
    pdfs_path = os.path.join(downloads_path, 'PDFs')

    # Determine if the paths are valid
    if os.path.isdir(docs_path):
        classify_files(docs_path)
    else:
        print(f'Cannot find "Docs" Folder.')

    if os.path.isdir(pdfs_path):
        classify_files(pdfs_path)
    else:
        print(f'Cannot find "PDFs" Folder.')


def file_ext_sort(downloads_path):
    """Sorts the files in a directory based on file type. Will NOT sort folders."""

    # File Extensions that we care about. Add additional file extensions here
    ext_to_subfolder = {
        '.pdf'  : 'PDFs',   # PDF
        '.docx' : 'Docs',   # MS Word post-2007
        '.doc'  : 'Docs',   # MS Word pre-2007
        '.txt'  : 'Docs',   # Text Document
        '.md'   : 'Docs',   # Markdown File
        '.exe'  : 'Bin',    # Windows Executable
        '.sh'   : 'Bin',    # BASH Script
        '.fish' : 'Bin',    # Fish Shell Script
        ''      : 'Bin',    # Probably a script
        '.ppt'  : 'Slides', # MS Powerpoint pre-2007
        '.pptx' : 'Slides', # MS Powerpoint post-2007
        '.py'   : 'Source', # Python (You can change this to 'Bin' if you want)
        '.rs'   : 'Source', # Rust
        '.c'    : 'Source', # C
        '.cpp'  : 'Source', # C++
        '.cs'   : 'Source', # C#
        '.java' : 'Source', # Java
        '.js'   : 'Source', # Javascript
        '.jpg'  : 'Images', # Needs more JPG
        '.jpeg' : 'Images', # JPG with an accent
        '.png'  : 'Images', # The cooler JPG
        '.tmp'  : 'Temp',   # Temp files
        '.zip'  : 'Misc'
    }

    # Create folders if they don't exist
    for folder in set(ext_to_subfolder.values()):
        print(f'  Creating {os.path.join(downloads_path, folder)}...')
        Path(os.path.join(downloads_path, folder)).mkdir(parents=True, exist_ok=True)

    # Collect the files in the given directory
    downloaded_files = [file for file in os.listdir(downloads_path) if os.path.isfile(os.path.join(downloads_path, file))]

    print('  Sorting files into categories...')
    for file in downloaded_files:
        # Attempt to find the last '.' in the filename
        ext_index = file.rfind('.')
        folder_to = ''
        # Files without extensions are probably executables
        if ext_index == -1:
            folder_to = os.path.join(downloads_path, 'Bin')
        # Attempt to collect file extensions
        else:
            ext = file[ext_index:]
            folder_to = os.path.join(downloads_path, ext_to_subfolder.get(ext, 'Misc'))
        
        # Define the source and destination
        folder_to = os.path.join(folder_to, file)
        folder_from = os.path.join(downloads_path, file)

        # Debugging output
        print(f'    FROM: {folder_from}')
        print(f'      TO: {folder_to}')

        # Rename (move) the file to the new folder
        os.rename(folder_from, folder_to)

def main():
    # Setup the argument parser
    parser = argparse.ArgumentParser(description='Sorts files in a given directory. Defaults to the Downloads directory.')
    parser.add_help = True
    parser.add_argument('-p', '--path', help='Override default behavior. Path to the folder to sort.')
    parser.add_argument('-t', '--testfiles', action='store_true', help='Creates test files instead of sorting. Must specify the "-p" flag to use this.')
    parser.add_argument('-n', '--nocontent', action='store_true', help='Disables content sorting.')
    parser.add_argument('--version', action='version', version=__version__)
    flags = parser.parse_args()

    # Check if default behavior is overrided
    if flags.path:
        # Create test files if desired
        if flags.testfiles:
            create_test_files(flags.path)
            return
        
        # Sorting by file extension
        print(f'Attempting to sort {flags.path}')
        file_ext_sort(flags.path)
        if not flags.nocontent:
            print('Sorting content...')
            file_content_sort(flags.path)
        else:
            print('Skipping content sort.')
        print('Complete!')
        return

    # Default interactive mode
    res = input('Attempt to detect path? (Y/n): ')
    if res.lower() == 'y' or res == '':
        # Attempt to read system info
        user = getpass.getuser()
        print(f'User: {user}')
        system = platform.system()
        print(f'System: {system}')
        path = ''

        # System info is detected
        if system == 'Windows':
            path = f'C:\\Users\\{user}\\Downloads'
        elif system == 'Linux':
            path = f'/home/{user}/Downloads'
        
        # Unable to determine path
        if path == '':
            print('Couldn\'t detect path automatically.')
    # Attempt to manually obtain path
    else:
        path = input('Please input the path of the folder to sort: ')
        
    # Determine if the path is valid
    if os.path.isdir(path):
        file_ext_sort(path)

        is_content_sort = input('Would you like to perform a content sort? (Y/n): ')
        if not flags.nocontent or (is_content_sort.lower() == 'y' or is_content_sort == ''):
            print('Sorting content...')
            file_content_sort(path)
        else:
            print('Skipping content sort.')
    else:
        print(f'Cannot find the path: "{path}".')
        
if __name__ == '__main__':
    main()
    # print('UNCOMMENT THE MAIN FUNCTION')
    # tc = TextClassifier()
    # tc.train()
    # #doc = read_txt('expectations.txt')
    # #doc = read_pdf('hacker.pdf')
    # doc = read_docx('expectations.docx')
    # print(tc.predict(doc))