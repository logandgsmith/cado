# Content Aware Downloads Organizer (CADO)

CADO seeks to sort folders by file type, and further sort human readable files by their subject. It can automatically detect and sort your downloads folder on Windows or Linux, or can be run independently on any given folder.

*NOTE: I would highly suggest backing up any important files in your Downloads folder before allowing the program to run automatically (by passing no flags and allowing the program to detect your downloads folder).* 

*If you do not wish to have your Downloads sorted, I would also suggest generating the testfiles (with the `-t` and `-p` flags) in a safe directory and running the sort on those (again with the `-p` flag. Please see the [How to Run](#how-to-run) section for further detail.*

***While there was never any file loss or damage in testing, I take no responsibility for possible damage or loss of files.***

## Requirements

* Python 3.8.0 or higher
* Natural Language Toolkit (NLTK)
* Python-Docx
* PyPDF2

## How to Run

### Installing Dependencies

This program requires the external packages listed above to run correctly. You can use install these packages using pip. Note that pip installations vary on different machines, so please use the pip command that is supported on your machine. 

*If you'd like to use `requirements.txt`:*
```sh
sudo pip3 install -r requirements.txt
```

*If you'd like to install the packages individually:*
```sh
sudo pip3 install nltk
sudo pip3 install python-docx
sudo pip3 install PyPDF2
```

### Running the Program on Test Files or a Specific Directory

These instructions walk you through creating a safe testing directory with test files that can be regenerated at any time. Please ensure that you've followed the steps outlined in [Installing Dependencies](#installing-dependencies) before attempting to run the program.

**Please review the [flags](#Flags) before continuing.** 

#### 1. Create the Test Directory

Open a terminal and navigate to the project folder. Then, make a new directory to generate files in. Example:

```sh
cd cado
mkdir test_directory
```

#### 2. Generate Test Files

Verify that you are in the directory with the `cado.py` script and run it with the `-p <pathname>` and `-t` flags. You can provide an absolute or relative path. Verify that the files are created. Python3.8 is aliased to `python3` on my machine, but it may be different on yours. Example:

```sh
python3 cado.py -p test_directory -t
cd test_directory
ls # Or `dir` on CMD
cd ..
```

#### 3. Running CADO on a Specific Directory (Non-Interactive)

Verify that you are in the directory with the `cado.py` script and run it with the `-p <pathname>` flag. You can provide an absolute or relative path. Verify the results by examining the new subfolders.

```sh
python3 cado.py -p test_directory
cd test_directory
ls # Or `dir` on CMD
```

### Running Interactively

**NOTE: Again, before running the program in this mode, I would suggest backing up any important files in your Downloads folder. This mode is intended for use on Windows or Linux**

Please ensure that you've followed the steps outlined in [Installing Dependencies](#installing-dependencies) before attempting to run the program.

CADO is made to run interactively if no flags are provided. Place the `cado` folder anywhere on the same disk as your Downloads folder and use `python3 cado.py` or `python cado.py` depending on your installation of Python. 

### Flags

Passing these flags will modify the behavior of the application.

* `-p <pathname>, --path <pathname>` - By itself will direct the program to sort the folder at the given path.
* `-t, --testfiles` - Directs the program to generate testfiles. Used with the `-p <pathname>` flag, it will generate test files at the given path with the folder given being the parent folder to the test files. 
* `-n, --nocontent` - Directs the program to NOT attempt or prompt for content sorting.

## Output/Results

Assuming there are no errors, after running the application, the terminal should show a readout of all of the sorts made. To verify results, the user can also examine the files manually via the file explorer or command line.

## Limitations

The application is written with Windows and Linux in mind, as such, it has not been tested on iOS machines and is not recommended for use on them.

## Author
[Logan D.G. Smith](https://github.com/logandgsmith)
