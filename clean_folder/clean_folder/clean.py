import sys
import shutil
from pathlib import Path

# Обьявим перечни расширений файлов в целевой папке
unknown_ext = set()
known_ext = set()

# Обьявим константы сортируемых файлов
IMAGE = ('JPEG', 'PNG', 'JPG', 'SVG')
VIDEO = ('AVI', 'MP4', 'MOV', 'MKV')
DOC = ('DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX')
AUDIO = ('MP3', 'OGG', 'WAV', 'AMR')
ARCHIVE = ('ZIP', 'GZ', 'TAR')

# список основных папок
FOLDER = ('archives', 'video', 'documents', 'audio', 'images', 'unknown')

# словарь транслитерации
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANSLIT = {}
for c, t in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANSLIT[ord(c)] = t
    TRANSLIT[ord(c.upper())] = t.upper()


# Функция принимает имя файла или папки и приводит к виду условий задачи
def normalize(fd_name):
    def normalize_name(name):
        new_name = ''
        for ch in name:
            if "0" <= ch <= "9" or "A" <= ch <= "Z" or "a" <= ch <= "z":
                new_name += ch
            elif ch in CYRILLIC_SYMBOLS or ch in CYRILLIC_SYMBOLS.upper():
                new_name += TRANSLIT[ord(ch)]
            else:
                new_name += '_'
        return new_name

    if '.' in fd_name:
        fd_names = fd_name.split(".")
        fd_name_res = normalize_name(fd_names[0]) + '.' + fd_names[1]
        return fd_name_res
    else:
        return normalize_name(fd_name)


# Функция распаковки архивов

def unpack_archive():
    arch = Path(Main_wave, 'archives')
    for f in arch.iterdir():
        if f.is_file():
            name_folder_archiv = f.stem
            wave_string = '\\'.join(f.parts[:-1]) + '\\' + name_folder_archiv
            try:
                shutil.unpack_archive(f, wave_string)
                Path.unlink(f)
            except ValueError as err_unpack:
                print(f'Archiv is not unpack {err_unpack}')

# Функция удаления пустых папок


def delete_oll_empty_folder(path):
    for dir in path.iterdir():
        if dir.is_dir() and (not (dir.name in FOLDER)):
            folder_wave = '\\'.join(dir.parts)
            try:
                shutil.rmtree(folder_wave)
            except OSError:
                print('delete error folders')


# Проверяем заданную для сортировки папку  если она не пустая, то сортируем а если она пустая то удаляем ее.

def folder_is_empty(path_folder):
    try:
        if path_folder.exists():
            path_folder.rmdir()
            return True
    except OSError:
        return False

# Функция отчет работы программы


def repotr():
    list_folders = []
    list_files = []
    list_exp = set()
    for folder in Main_path.iterdir():
        if folder.name != 'archives':
            list_folders.append(folder.name)
            print(folder.name.upper())
            for i in folder.iterdir():
                list_files.append(i.name)
                list_exp.add(i.suffix)
            if list_files:
                print(f'Files:{list_files} - Extensions:{list_exp}')
            else:

                print(f'Files: not found')
            list_files.clear()
            list_exp.clear()


# Функция сортировки файлов и папок

def sort_func(path_f):
    for el in path_f.iterdir():
        try:
            if el.is_file():
                path_file = el
                exp = el.suffix.replace(".", "")
                if exp.upper() in IMAGE:
                    normal_fname = normalize(el.name)
                    move_path = Path(Main_wave, 'images/', normal_fname)
                    if not move_path.exists():
                        path_file.rename(move_path)
                    else:
                        path_file.unlink()
                elif exp.upper() in DOC:
                    normal_fname = normalize(el.name)
                    move_path = Path(Main_wave, 'documents/', normal_fname)
                    if not move_path.exists():
                        path_file.rename(move_path)
                    else:
                        path_file.unlink()
                elif exp.upper() in AUDIO:
                    normal_fname = normalize(el.name)
                    move_path = Path(Main_wave, 'audio/', normal_fname)
                    if not move_path.exists():
                        path_file.rename(move_path)
                    else:
                        path_file.unlink()
                elif exp.upper() in VIDEO:
                    normal_fname = normalize(el.name)
                    move_path = Path(Main_wave, 'video/', normal_fname)
                    if not move_path.exists():
                        path_file.rename(move_path)
                    else:
                        path_file.unlink()
                elif exp.upper() in ARCHIVE:
                    normal_fname = normalize(el.name)
                    move_path = Path(Main_wave, 'archives/', normal_fname)
                    if not move_path.exists():
                        path_file.rename(move_path)
                    else:
                        path_file.unlink()
                else:
                    normal_fname = normalize(el.name)
                    move_path = Path(Main_wave, 'unknown/', normal_fname)
                    if not move_path.exists():
                        path_file.rename(move_path)
                    else:
                        path_file.unlink()

            if el.is_dir() and (not (el.name in FOLDER)):
                if not folder_is_empty(el):
                    sort_func(el)

        except (FileNotFoundError, FileExistsError) as err:
            print(f'file Exist error {err}')


# Проверим введенный аргумент и создадим подкаталоги в указанном каталоге

if len(sys.argv) != 2:
    print('Input please argument - path sortering folder')
    quit()
else:
    Main_wave = sys.argv[1]
    Main_path = Path(Main_wave)
if folder_is_empty(Main_path):
    print('Folder is empty and was removed')
    quit()
else:
    for folder in FOLDER:
        wave_new_folder = Path(Main_path, folder)
        try:
            wave_new_folder.mkdir()
        except FileExistsError:
            continue


def main():

    # Проверим введенный аргумент и создадим подкаталоги в указанном каталоге

    if len(sys.argv) != 2:
        print('Input please argument - path sortering folder')
        quit()
    else:
        Main_wave = sys.argv[1]
        Main_path = Path(Main_wave)
    if folder_is_empty(Main_path):
        print('Folder is empty and was removed')
        quit()
    else:
        for folder in FOLDER:
            wave_new_folder = Path(Main_path, folder)
            try:
                wave_new_folder.mkdir()
            except FileExistsError:
                continue

    sort_func(Main_path)
    delete_oll_empty_folder(Main_path)
    unpack_archive()
    repotr()


if __name__ == '__main__':
    main()
