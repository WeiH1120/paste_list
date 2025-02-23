# paste_list


# 項目說明
純文字簡易剪貼簿，允許複數剪貼項目（純文字），並可用左右鍵選取。

# 版本

- Version:1.0
- 支援系統
    - macOS Sequoia 15.3.1（24D70）
    - Windows 10


# How to use?

1. open the app.
2. write something.
3. select the word, and copy it.
4. repeat step 2~3 
5. open the clipboard with:
    1. macOS: control + command + v
    2. Windows: ctrl + windows + v
6. Choose the text with left or right key
7. paste or exit
    1. return to paste
    2. esc to exit




# Virtual environment
## Install package
pip install pipenv

## Create virtual environment according to Pipfile and Pipfile.lock
pipenv install

## Activate environment
pipenv shell

<br><br><br>

## pip install
pip install --upgrade pip

pip install keyboard
pip install pynput 

# Execute
## cmd
python .\paste_list.py

## pack it be a .exe file
pyinstaller.exe -F -w .\paste_list.py
