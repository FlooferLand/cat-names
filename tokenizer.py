import unicodedata

class Dataset:
    """Separated input and expected output"""
    data: [str]
    labels: [str]
    duplicates: [str]
    path: str = None
    def __init__(self, path: str):
        self.data = []
        self.labels = []
        self.duplicates = []
        self.path = path
    def pairs(self) -> [(str, str)]:
        pair: [(str, str)] = []
        if len(self.data) != len(self.labels):
            raise KeyError()
        for i in range(0, len(self.data)):
            data = self.data[i]
            label = self.labels[i]
            pair.append((data, label))
        return pair
    def combine(self, other: "Dataset") -> "Dataset":
        new = Dataset(path=self.path)
        
        # Extending
        new.data.extend(self.data)
        new.labels.extend(self.labels)
        new.data.extend(other.data)
        new.labels.extend(other.labels)
        
        new.duplicates.extend(other.duplicates)
        return new

def accented_to_ascii(text: str) -> str:
    return unicodedata.normalize("NFD", text).encode("ascii", "ignore")

def tokenize(text: str, name: str=None) -> Dataset:
    md = Dataset(path=f"./data/{name}" if name != None else None)
    for line in text.splitlines():
        line = line.strip().lower()
        if len(line) <= 1 or line[0] == '#':
            continue
        line_unsplit = "" + line
        (key, value) = line.split('-') if line.find('-') != -1 else (line, line)
        key = key.strip()
        value = value.strip()
        
        # Important checks
        if key in md.data and value in md.labels:
            md.duplicates.append(line_unsplit)
            continue
        
        # Adding the data
        md.data.append(key)
        md.data.append(accented_to_ascii(key))
        md.labels.append(value)
        md.labels.append(accented_to_ascii(key))
    if len(md.duplicates) > 0:
        print(f"Duplicates found in '{name}': {len(md.duplicates)}")
    return md

def read_from_file(path: str) -> str:
    text: str
    with open(f"./data/{path}", 'r', encoding="utf8") as f:
        text = f.read()
    return text

def dataset_from_file(filename: str) -> Dataset:
    normal = tokenize(read_from_file(filename), name=filename)
    ai = tokenize(read_from_file(f"ai_{filename}"), name=f"ai_{filename}")
    return normal.combine(ai)

def get_datasets() -> (Dataset, Dataset):
    train = dataset_from_file("training.txt")
    test = dataset_from_file("testing.txt")
    
    # Adding train data to the test dataset
    test = test.combine(train)
    print(f"len(train) : {len(train.data)}")
    print(f"len(test) : {len(test.data)}")
    
    return (train, test)
