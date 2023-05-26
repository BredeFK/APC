import os.path
import pathlib

from dotenv import dotenv_values

import util.printWithColors as printColors

config = dotenv_values(".env")
SOURCE_PATH = config["SOURCE_PATH"]
DESTINATION = f'{SOURCE_PATH}\\Songs'


def main():
    print(SOURCE_PATH)
    if os.path.exists(SOURCE_PATH):
        printColors.green("File exists")
        organize_files()
    else:
        printColors.red(f'File at path {SOURCE_PATH} does not exist')


def organize_files():
    if not os.path.exists(DESTINATION):
        os.mkdir(DESTINATION)

    path = f'{SOURCE_PATH}\\complete'
    if os.path.exists(path):
        complete_folder = os.listdir(path)
        printColors.blue(f'Organizing {len(complete_folder)} folders...')

        for user_folder in complete_folder:

            if os.path.isdir(f'{path}\\{user_folder}'):
                for song_folder in os.listdir(f'{path}\\{user_folder}'):

                    song_path = f'{path}\\{user_folder}\\{song_folder}'
                    if os.path.isdir(song_path):
                        for file in os.listdir(song_path):
                            if os.path.isfile(f'{song_path}\\{file}'):
                                move_files(song_path, file)
                            else:
                                print("Is folder")

            elif os.path.isfile(path):
                print(f'Is a file: {path}')


def move_files(folder_source, file_name):
    file_destination = f'{DESTINATION}\\{file_name}'
    printColors.green(f'Moving {file_name} to {file_destination}')
    pathlib.Path(f'{folder_source}\\{file_name}').rename(file_destination)


main()
