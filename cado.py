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
                stripped_word = word.strip('\n')
                new_set.append((stripped_word, self.subjects[index]))
                self.subject_dictionary[stripped_word] = index
            self.subject_words[index] = new_set

        # Feature Extraction
        feature_sets = []
        for subjects in self.subject_words:
            feature_sets += [(self.matching_features(line), subject) for (line, subject) in subjects]

        self.classifier = nltk.NaiveBayesClassifier.train(feature_sets)

    def predict(self):
        pass

    # Naive classification of text based on the similarity to subject
    def matching_features(self, line: str):
        scores = [0] * len(self.subjects)

        # Find all words in the top occuring
        words = nltk.word_tokenize(line)

        for word in words:
            subject_index = self.subject_dictionary.get(word, -1)
            if subject_index == -1:
                continue
            scores[subject_index] += 1

        most_like = scores.index(max(scores))

        # Returning the scores
        return {'subject' : most_like}


def read_docx(path: str) -> list:
    """Reads a docx and returns list of non-symbol words"""
    doc = docx.Document(path)
    lines = [paragraph.text for paragraph in doc.paragraphs]
    
    # Read lines of the word doc
    words = []
    for line in lines:
        if line != '':
            words += nltk.word_tokenize(line)

    # Strip symbols and put words in lowercase
    tokens = []
    for word in words:
        if word not in '!@#$%^&*(),<>./?\'\"\\':
            tokens.append(word.lower())

    return tokens

def read_pdf(path: str) -> list:
    """Reads a pdf and returns list of non-symbol words"""
    # Open the PDF
    with open(path, 'rb') as pdf:
        # Read the contents of the PDF
        pdf = PyPDF2.PdfFileReader(pdf)
        pages = []
        for x in range(pdf.numPages):
            page = pdf.getPage(x).extractText().replace('\n', '')
            pages += nltk.word_tokenize(page)

        # Strip symbols and put words in lowercase
        tokens = []
        for word in pages:
            if word not in '!@#$%^&*(),<>./\'\"\\':
                tokens.append(word.lower())

    return tokens

def file_content_sort(downloads_path):
    """Sorts files into subfolders based on their content"""

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
    else:
        print(f'Cannot find the path: "{path}".')
        
if __name__ == '__main__':
    #main()
    print('UNCOMMENT THE MAIN FUNCTION')
    tc = TextClassifier()
    tc.train()
    print(tc.subject_words)