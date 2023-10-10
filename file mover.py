import shutil
import os

def get_dir() -> str:
    dir_old = input("Paste the directory of the folder to move files from: ") 
    dir_new = input("Paste the directory of the folder to move files to: ") 
    return [dir_old, dir_new]

def excl_files():
    ex = []
    cont_exc = True
    exc1 = input("Exclude any files from being moved? (Y or N): ")
    if exc1 == "N" or exc1 == "n" or exc1 == "No" or exc1 == "no":
        cont_exc = False
    while cont_exc:
        ex.append(input("Name of file to be excluded (case sensitive): "))
        exc = input("Continue excluding? (Y or N): ")
        if exc == "N" or exc == "n" or exc == "No" or exc == "no":
            cont_exc = False
    return ex

def repl_files():
    rp = []
    cont_rep = True
    rep1 = input("Replace certain files that already exist? (Y or N): ")
    if rep1 == "N" or rep1 == "n" or rep1 == "No" or rep1 == "no":
        cont_rep = False
    while cont_rep:
        rp.append(input("Name of file to be replaced (case sensitive): "))
        rep = input("Continue replacing? (Y or N): ")
        if rep == "N" or rep == "n" or rep == "No" or rep == "no":
            cont_rep = False
    return rp

def add_files(old_path:str, new_path:str, file_name:str, ex_rp:list):
    exclude = False
    replace = False
    if file_name in ex_rp[0]:
        exclude = True
    if file_name in ex_rp[1]:
        replace = True
    if exclude:
        exc = input("Exclude moving this file? (Y or N): ")
        if exc == "Y" or exc == "y" or exc == "Yes" or exc == "yes":
            return
    shutil.copy(old_path, new_path)
    print("File at path:" + old_path + " moved to path:" + new_path + "\n")

def check_files(directories:list, ex_rp:list):
    for files in os.listdir(directories[0]):
        full_path = os.path.abspath(os.path.join(directories[0], files))
        local_path = full_path.replace(directories[0], "")
        local_path = local_path[1:]
        new_path = os.path.join(directories[1], local_path)
        file_name = os.path.splitext(os.path.basename(full_path))[0]
        print("Checking file: " + file_name + " at path:" + full_path)
        if (os.path.isfile(full_path) and not os.path.exists(new_path)) or (os.path.isfile(full_path) and file_name in ex_rp[1]):
            print("File " + file_name + " to be moved to destination...")
            add_files(full_path, new_path, file_name, ex_rp)
        elif os.path.isdir(full_path) and not os.path.exists(new_path):
            print("The folder at directory " + new_path + " does not exist.")
            add_folder = input("Would you like to add this folder to the destination? (Y or N)")
            if add_folder == "Y" or add_folder == "y" or add_folder == "Yes" or add_folder == "yes":
                shutil.copytree(full_path, new_path)
                print("Folder " + file_name + " moved to " + new_path + "\n")
        elif os.path.isdir(full_path) and os.path.exists(new_path):
            check_files([full_path, new_path], ex_rp)

def file_mover():
    is_dir = False
    while is_dir == False:
        directories = get_dir()
        dir_old = directories[0]
        dir_new = directories[1]
        if os.path.isdir(dir_old) and os.path.isdir(dir_new):
            is_dir = True
        else:
            print("One or more directories do not exist.")
    ex_rp = [excl_files(), repl_files()]
    check_files(directories, ex_rp)
    is_dir = False
    cont = input("Move another folder? (Y or N): ")
    if cont == "N" or cont == "n" or cont == "No" or cont == "no":
        return 
    else:
        file_mover()  

file_mover()
