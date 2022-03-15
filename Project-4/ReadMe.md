# Project 4
In this project, you will implement dynamic programming algorithms for computing the minimal cost of aligning gene sequences and for extracting optimal alignments.
</br></br>
You are using dynamic programming to align multiple gene sequences (taxa), two at a time. In light of the SARS outbreak a few years ago, we have chosen to use the SARS 
virus as one of our DNA sequences. SARS is a coronavirus, and we have also provided the genomes for several other coronaviruses. It is your job in this project to align 
all pairs in order to assess the pair-wise similarity. To prepare to succeed on this project, make sure you understand the sequence alignment and solution extraction 
algorithms as presented in class and in the book.

## Installation
In order to run the program, simply fork the repository and install the three Python files Proj4GUI.py, GeneSequencing.py, and which_pyqt.py. You will also need the genomes.txt file. These four files can be placed in whatever directory you wish. </br>
This project uses [PyQt5](https://pypi.org/project/PyQt5/) in order to build the GUI for the application. Assuming you have installed [Python](https://www.python.org/downloads/) and your PATH variable is set up properly to run Python commands from the terminal, use the following command to install PyQt5:
```bash
$ pip install PyQt5
```
After PyQt5 has been installed, simply run the following command from the directory where the project is located:
```bash
$ python Proj4GUI.py
```

## Usage
**goals:**
1. Design and implement a Dynamic Programming algorithm that has applications to gene sequence alignment.
2. Think carefully about the use of memory in an implementation.
3. Solve a non-trivial computational genomics problem.

When you press the “Process” button on the GUI, the matrix fills with numbers, one number for each pair, as shown in the figure below. You will generate these numbers by aligning the first n characters (bases) in each sequence pair (the default will be n = 1000 but you can change this). Note that your alignment may be slightly longer than this due to inserts. Your job will be to fill in the proper numbers based on a sequence alignment function that employs dynamic programming. You will fill the matrix with the pair-wise scores. You do not need to fill in the lower triangle of the matrix (since it is symmetric), but you should fill in the diagonal. When the “Process” button is clicked, the GUI calls the GeneSequencing.align_all() method which you will implement.

Each gene sequence consists of a string of letters and is stored in the given database file. The scaffolding code loads the data from the database. For example, the record for the “sars9” genome contains the following sequence (prefix shown here):

```atattaggtttttacctacccaggaaaagccaaccaacctcgatctcttgtagatctgttctctaaacgaactttaaaatctgtgtagctgtcgctcggctgcatgcctagtgcaccta...```
