from create_txt_files import create_files
from pathlib import Path
from pprint import pprint
from threading_search import search_with_threads
from multiprocessing_search import search_with_processes
from timeit import timeit
from colorama import Fore

if __name__ == "__main__":
    path = Path('./files_to_analyze')
    # NUMBER_OF_FILES = 25
    # create_files(path, NUMBER_OF_FILES)

    words_to_search = ['some', 'know', 'get', 'too', 'extra']
    # words_to_search1 = ['any', 'spa', 'ever']
    
    NUMBER_OF_THREADS = 7
    NUMBER_OF_PROCESSES = 7
    
    # Виконаємо заміри виконання наших пошуків
    time_threads = timeit(lambda: search_with_threads(path, NUMBER_OF_THREADS, words_to_search), number=10000)
    time_processes = timeit(lambda: search_with_processes(path, NUMBER_OF_THREADS, words_to_search), number=10000)

    # Тепер збережемо результати пошуку. Насправді, ці функції тут вже не виконуватимуться, бо кожне зі слів уже є в словнику.
    # Тому корисна робота двух наступних рядків - саме збереження результатів у окремі змінні
    result_with_threads = search_with_threads(path, NUMBER_OF_THREADS, words_to_search)
    result_with_processes = search_with_processes(path, NUMBER_OF_PROCESSES, words_to_search)

    print(Fore.CYAN + "Results of searching with threads:" + Fore.RESET)
    pprint(result_with_threads)
    
    print()
    print(Fore.CYAN + "Results of searching with processes:" + Fore.RESET)
    pprint(result_with_processes)
    
    print()
    print(Fore.GREEN + "Search with threads:" + Fore.RESET, time_threads)
    print(Fore.GREEN + "Search with processes:" + Fore.RESET, time_processes)
