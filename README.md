# Content Aware Downloads Organizer (CADO)

CADO seeks to sort folders by file type, and further sort human readable files by their subject. It can automatically detect and sort your downloads folder on Windows or Linux, or can be run independently on any given folder.

## Requirements

* Python 3.8.0 or higher
* Natural Language Toolkit (NLTK)
* Python-Docx
* PyPDF2
* gensim

## How to Run

CADO is made to run interactively if no flags are provided. Place the script anywhere on the same disk as your Downloads folder and use `python3 cado.py` or `python cado.py` depending on your installation of Python. 

### Flags

Passing these flags will modify the behavior of the application.

* `-p <pathname>, --path <pathname>` - By itself will direct the program to sort the folder at the given path.
* `-t, --testfiles` - Directs the program to generate testfiles. Used with the `-p <pathname>` flag, it will generate test files at the given path with the folder given being the parent folder to the test files. 

## Output/Results

Assuming there are no errors, after running the application, the terminal should show a readout of all of the sorts made. To verify results, the user can also examine the files manually via the file explorer or command line.

## Limitations

The application is written with Windows and Linux in mind, as such, it has not been tested on iOS machines and is not recommended for use on them.

## Author
[Logan D.G. Smith](https://github.com/logandgsmith)
