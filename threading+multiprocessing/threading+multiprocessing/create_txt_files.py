from faker import Faker
from pathlib import Path

def create_files(path: Path, num: int):
    fake_data = Faker()
    
    for i in range(num):
        filename = f'file{i}.txt'
        with open(path / filename, 'w') as fh:
            fh.write(fake_data.text(1000))
            
if __name__ == '__main__':
    path = Path('./files_to_analyze')

    NUMBER_OF_FILES = 20
    
    create_files(path, NUMBER_OF_FILES)
