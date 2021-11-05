from pathlib import Path as pth
import os
import shutil

descargas = pth(r'C:\Users\danie\Downloads')
os.chdir(descargas)

file_types = {
            'Pictures': ['.png', '.jpg', '.jpeg'],
            'Documents': ['.docx', '.doc', '.txt'],
            'E-book': ['.epub', '.mobi', '.azw3'],
            'Movies': ['.mp4', '.avi'],
            'PDF': ['.pdf'],
            'Apps': ['.exe'],
            'Excel': ['.csv', '.xls', '.xlsx'],
            'ZIP': ['.zip', '.rar'],
            }

# if these folders already exist, skip them when processing folder content
folders_to_exclude = list(file_types)
folders_to_exclude.extend(['Misc', 'Misc folders'])

# create the classification folders
for key in file_types.keys():
    new_dir = (pth.cwd() / key)  # create a new folder using name stored in 0 pos
    new_dir.mkdir(exist_ok=True)
(descargas / 'Misc').mkdir(exist_ok=True)  # finally create a miscellaneous folder
(descargas / 'Misc folders').mkdir(exist_ok=True)

# content of folder to process
content = descargas.iterdir()
# exclude the classification folders
process_items = [i for i in content if i.name not in folders_to_exclude]
for item in process_items:
    # move item to Miscellaneous folder unless is a file of type...
    to_misc = True
    if item.is_dir():  # check if it is a folder
        shutil.move(item, descargas / 'Misc folders')
    else:
        # check if file belongs any classified category
        for filetype, extensions in file_types.items():
            file_ext = item.suffix  # get the file extension
            if file_ext in extensions:  # check if belongs to current category
                dest_folder = descargas / filetype  # destination folder
                # avoid shutil.move exception when a file exists in destination
                if not (dest_folder / item.name).exists():
                    shutil.move(item, dest_folder)
                    to_misc = False
                    break  # stop trying to categorize file
        # file belongs to miscellaneous category
        if to_misc:
            dest_folder = descargas / 'Misc'
            if not (dest_folder / item.name).exists():
                shutil.move(item, dest_folder)

with open('dir.txt', 'w') as f:
    categorized_content = descargas.iterdir()
    for item in categorized_content:
        line = f'{item}\n'.replace('C:\\Users\\danie\\Downloads\\', '')
        f.write(line)