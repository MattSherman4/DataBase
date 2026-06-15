import shutil
from pathlib import Path

for file_path in Path("C:/Users/pensh/Desktop/VSCode/DataBase/_Draft_CFG_Maker/Data/").iterdir():
    if file_path.is_file():
        shutil.copy(file_path, "C:/Users/pensh/Desktop/VSCode/DraftClassMaker/Data")
        print(f"Moved file: {file_path.name}!")

print("--All files moved--")

