from pathlib import Path
from threading import Thread
from pprint import pprint


result_dict = {}


def split_equally(amount: int, divisor: int) -> list:
    '''
    Function splits some amount on a given number maintaining results being integer and having a difference not greater than 1.
    For example, 25 tasks among 7 threads (or 7 processes) will be split as [4, 4, 4, 4, 3, 3, 3]
    '''
    a = amount // divisor
    n1 = divisor * (a+1) - amount
    n2 = amount - divisor * a
    
    equal_split = [a+1 for _ in range(n2)] + [a for _ in range(n1)]

    return equal_split
    

def search_in_file(path: Path, string: str) -> bool:
    '''
    Returns True if there is '<string>' in the file, which path is used as the argument.
    Otherwise returns False
    '''
    with open(path, 'r') as fh:
        text = fh.read()
        if text.find(string) != -1:
            return True
        return False
    

def split_on_threads(number_of_threads, func, *args):
    '''
    Split function execution on several threads.
    args: ([list of files], 'string to search for')
    '''
    global result_dict
    
    string = args[1]    
    number_of_files = len(args[0])
    threads = []

    if number_of_threads > number_of_files:
        number_of_threads = number_of_files

    for i in split_equally(number_of_files, number_of_threads):     # Here tasks are split among threads
        
        files = [args[0].pop() for _ in range(i)]

        thread = Thread(target=func, args=(files, string))
        thread.start()
        threads.append(thread)

    # Чекаємо на завершення всіх потоків, щоб не було ніяких зайвих помилок
    [thread.join() for thread in threads]
    
    if len(result_dict[string]) == 0:
        result_dict[string] = 'No such word in given files'
        

# The main executable function which is split on threads
def analyze_files(file_paths: list, string: str, result_dict=result_dict):
    '''
    Searches for the '<string>' in every file within the list of file_paths.
    Returns a dictionary where key is a '<string>' and value is a list of paths to files with a '<string>' in it
    '''
    
    temp_result = {string: set()}

    # Якщо шукане слово є у файлі - додаємо файл до тимчасового результату temp_result
    for file in file_paths:
        if search_in_file(file, string) is True:
            temp_result[string].add(str(file))    

    # Оновлюємо спільний словник даними з тимчасового результату
    if string not in result_dict:
        result_dict[string] = set()
    result_dict[string].update(temp_result[string])


def search_with_threads(path: Path, number_of_threads: int, words_to_search: list) -> dict:
    '''
    Applies 'split_on_threads' function to every word we want to search to
    '''
    global result_dict
    
    for word in words_to_search:
        # Якщо слово вже шукали, то працюємо з наступним
        if word in result_dict:
            continue
        
        split_on_threads(number_of_threads, analyze_files, [file for file in path.iterdir()], word)
    
    return result_dict
    

if __name__ == '__main__':
    path = Path('./files_to_analyze')
    NUMBER_OF_THREADS = 7
    words_to_search = ['some', 'know', 'get', 'too', 'extra']
    
    result = search_with_threads(path, NUMBER_OF_THREADS, words_to_search)

    pprint(result)
    
    print(split_equally(25, 25))
    print(split_equally(25, 7))
    print(split_equally(7, 25))
    print(split_equally(13, 4))