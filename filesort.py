"""
Filesort.py

Intended as a tool to sort random files in my Downloads folder, but should sort unorganized files in any directory

At this stage it copies my target directory (what I want to sort) to a test directory and then sorts that, so I
don't lose any files while developing the script. At some point I could change it to have no redundancy.

I am identifying file types by reading their names backwards into a stack until I get to a period -- I'm sure
I could get the same results by another more concise method, but it was my first solution that I'm continuing with
because I think it leaves the door ajar for a wider application.

The basic task here consists of the python equivalent of a couple linux commands and one loop, so most of
the code is organized around testing and catching exceptions and edge cases (ideally to make it more broadly useful).
"""

import os
import shutil

HOME = '/home/user/PycharmProjects/FileSorter/testDl'  # site of test directory, change for practical use


# stack used to collect file extensions
class BbyStack:
    def __init__(self):
        self.__stack = []

    def push(self, incoming):
        self.__stack.append(incoming)

    def pop(self):  # for debug
        return self.__stack.pop()

    def peek(self):  # for debug
        return self.__stack[-1]

    def show_all(self):  # for debug
        print(self.__stack)

    def empty(self):  # returns extension of the file being examined as a string
        strng = ''
        while self.__stack:
            strng += self.__stack.pop()
        return strng


# to reuse yes/no interface option (returns Boolean)
def yesno(text):
    go = ''
    while go != 'y' and go != 'n':
        go = input(text + ' y/n')
    return True if go == 'y' else False


# gets or confirms (by path) the directory which will be copied and sorted
def get_path():
    path = os.getcwd()
    print(f'The current working directory is: {path}')
    if yesno('Is this the directory you would like to sort?'):
        return path
    else:
        while True:
            path = input('Please input path of directory you would like to sort or type "quit" to exit: \n')
            if path == 'quit':
                return
            if os.path.exists(path) and os.path.isabs(path) and os.path.isdir(path):
                return path


# copying a directory tree for debugging or redundancy if there's a mistake made
def copytree():
    batch = BbyStack()
    working_in = get_path()  # directory I want to copy
    path_to_sort = os.path.join(HOME, input('Name the test file: '))  # path to copy to
    batch.push(path_to_sort)  # lazy or efficient? -- reusing the stack to return two objects -- (1) the path
    try:
        shutil.copytree(working_in, path_to_sort)
    except FileExistsError:  # if I've already created the new directory
        print('A test file already exists.')
    finally:
        sorting = os.listdir(path_to_sort)
    batch.push(sorting)  # (2) the list of files
    return batch


# Now actually begin sorting files
done = 0
sort_this = copytree()
for index, each in enumerate(sort_this.pop()):  # pops list off
    file_path = os.path.join(sort_this.peek(), each)  # peeks at path and joins filename
    if os.path.isfile(file_path):
        stk = BbyStack()
        all_chars = list(each)
        char = all_chars.pop()
        while char != '.':  # remove characters from end of string and push to stack until we reach a period
            stk.push(char)
            char = all_chars.pop()
        file_type = stk.empty()  # empty stack to retrieve file type
        new_path = os.path.join(sort_this.peek(), file_type)  # make the path for this extension
        try:
            os.mkdir(new_path)  # make the new directory if it doesn't exist
        except FileExistsError:
            print(f'{index + 1}) Directory has already been made for {file_type}.')
        except FileNotFoundError:
            print(f'{index + 1}) Inconsistency in expected path.')
        finally:
            shutil.move(file_path, new_path)  # moves old path address to new path address
            done += 1

print(f'Sorting finished -- {done} files sorted.')
