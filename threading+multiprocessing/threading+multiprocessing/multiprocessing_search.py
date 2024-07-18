from multiprocessing import Queue, Process
import sys
from threading_search import split_equally, analyze_files
from pathlib import Path
from pprint import pprint


result_dict = {}


def split_on_processes(file_list: list, number_of_processes: int, func, args):
    '''
    Split function execution on several processes.
    args = ([list of files], '<string to search for>')
    '''
    processes = []
    queue_to_process = args[0]
    queue_out_process = args[1]
    
    for i in split_equally(len(file_list), number_of_processes):
        short_file_list = [file_list.pop() for _ in range(i)]
        
        process = Process(target=func, args=args)
        process.start()
        processes.append(process)

        queue_to_process.put(short_file_list)

    [p.join() for p in processes]

    while queue_out_process.empty() is False:
        dict_to_add = queue_out_process.get()
        
        for word in dict_to_add.keys():
            if word not in result_dict.keys():
                result_dict[word] = set()
            result_dict[word].update(dict_to_add[word])
     
    for word in result_dict:
        if len(result_dict[word]) == 0:
            result_dict[word] = 'No such word in given files'


def search_with_processes(path: Path, number_of_processes: int, words_to_search: list) -> dict:
    '''
    Applies 'split_on_processes' function to every word we want to search to
    '''
    global result_dict

    for word in words_to_search:
        
        # Якщо слово вже шукали - працюємо з наступним
        if word in result_dict:
            continue
        
        queue_to_process = Queue()
        queue_out_process = Queue()

        file_list = [file for file in path.iterdir()]

        split_on_processes(file_list, number_of_processes, function_for_process, (queue_to_process, queue_out_process, word,))
    
    return result_dict


def function_for_process(queue_in: Queue, queue_out: Queue, word):
    '''
    The function gets a file_list from queue_in, and returns a dictionary of result to queue_out.
    Used inside other processes.
    '''
    file_list = queue_in.get()
    temp_dict = {}

    analyze_files(file_list, word, temp_dict)       # function changes temp_dict
   
    queue_out.put(temp_dict)                        # temp_dict returned back to Main Process, where it will be used to update result_dict

    # sys.exit(0)


if __name__ == '__main__':
    
    path = Path('./files_to_analyze')
    NUMBER_OF_PROCESSES = 7
    words_to_search = ['some', 'know', 'get', 'too', 'extra']

    
    result = search_with_processes(path, NUMBER_OF_PROCESSES, words_to_search)

    pprint(result)
