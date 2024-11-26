import os
import json

from pathlib import Path
from datetime import datetime

trace_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

def load_file(filepath):
    with open(filepath, 'r') as file:  
        contents = file.read()
        return contents
    
def load_json_file(filepath):
    with open(filepath, 'r') as file:  
        jsonData = json.load(file)
        return jsonData
    
def load_file_from_path_variable(pathVariable):
    filePath = os.environ.get(pathVariable)
    return load_file(filePath)

def write_file(filepath, content):
    with open(filepath, 'w') as file:
            file.write(content)

def output_content(filePath, content):
    write_file(filePath, content)

def trace(filename, content):
    targetDirctory = "target"
    traceDirectory = os.path.join(targetDirctory, "trace", trace_timestamp)
    Path(traceDirectory).mkdir(parents=True, exist_ok=True)
    write_file(os.path.join(traceDirectory, filename), content)
     
def load_configuration():
    configurationFilePath = os.getenv("CONFIGURATION")
    configurationJson = load_json_file(configurationFilePath)
    return configurationJson

def get_trace_timestamp():
    return trace_timestamp

def list_files(dirpath):
    directory_path = Path(dirpath)
    files = [f.name for f in directory_path.iterdir() if f.is_file()]
    return files
