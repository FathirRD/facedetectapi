import os

path1 = os.path.join(os.path.dirname(__file__), "temp/")
for file_name in os.listdir(path1):
    # construct full file path
    file = path1 + file_name
    if os.path.isfile(file):
        os.remove(file)

path2 = os.path.join(os.path.dirname(__file__), "temp/detail/")
for file_name in os.listdir(path2):
    # construct full file path
    file = path2 + file_name
    if os.path.isfile(file):
        os.remove(file)