import os
import shutil
from distutils.dir_util import copy_tree
from tokenizer import Dataset, get_datasets

def cleanup(filename: str, dataset: Dataset):
    lines: [str]
    with open(f"./backup/{filename}", "r", encoding="utf8") as f:
        lines = f.readlines()
    with open(f"./data/{filename}", "w", encoding="utf8") as f:
        out: [str] = []
        saved_duplicates: dict = {}
        for line in lines:
            line = line.strip()
            if len(line) <= 2:
                out.append("")
                continue
            if line[0] == '#':
                if line[1] != ':':
                    out.append(line)
                continue
            line = line.lower()
            
            # Finding out if its a dupe
            is_duplicate = False
            for dupe in dataset.duplicates:
                if dupe in line:
                    if line in saved_duplicates.keys():
                        is_duplicate = True
                        saved_duplicates[line] += 1
                    else:
                        saved_duplicates[line] = 1
            
            # Adding the data if its not a dupe
            if not is_duplicate:
                out.append(line)

        # Adding the duplicates to the very end using comments for fun
        out.append("")
        out.append("#: Duplicates ")
        for line, count in saved_duplicates.items():
            count = f" [{count}]" if count > 1 else ""
            out.append(f"#: dupe {line}{count}")
        
        # Python's IO writelines method appears to be broken so I have to do this:      
        f.write('\n'.join(out))
        
        print(f"Cleaned up {len(saved_duplicates)} duplicates from './data/{filename}'")

if __name__ == "__main__":
    # Loading the data sets
    (train, test) = get_datasets()

    # Creating a backup
    if os.path.exists("./backup"):
        shutil.rmtree("./backup")
    os.makedirs("./backup")
    copy_tree("./data", "./backup")

    # Cleaning stuff up
    #cleanup("ai_training.txt", train)
    #cleanup("ai_testing.txt", train)
    