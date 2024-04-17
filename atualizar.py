import os
import shutil
from zipfile import ZipFile
import requests

def should_keep(file):
    return file in ["Cursos", "jsons", "main.sqlite3", ".git"]

def clean_directory():
    for item in os.listdir():
        if not should_keep(item):
            if os.path.isdir(item):
                shutil.rmtree(item)
            else:
                os.remove(item)

def download_zip(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def extract_zip(filename):
    with ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()

def move_contents_from_folder(source_folder):
    for item in os.listdir(source_folder):
        if should_keep(item):
            continue
        full_item_path = os.path.join(source_folder, item)
        target_path = os.path.join(".", item)
        if os.path.isfile(target_path):
            os.remove(target_path)
        elif os.path.isdir(target_path):
            shutil.rmtree(target_path)
        shutil.move(full_item_path, ".")
    os.rmdir(source_folder)

def main():
    print("Atualização do sistema Katomart. IMPORTANTE: Se você estiver executando após o dia 15/04/2024 (ou se o aviso na página inicial mandou), delete o arquivo 'main.sqlite3' manualmente para que ele seja recriado corretamente na próxima execução alguma mudança significativa na estrutura ocorreu. Você precisará reconfigurar o sistema ao fazer isso. Não delete a pasta jsons nem a pasta cursos para atualizar caso existam.")
    user_consent = input("Deseja atualizar o sistema? (s/n)\n").strip().lower()
    if user_consent != "s":
        print("A atualização foi cancelada pelo usuário.")
        return
    clean_directory()
    zip_url = "https://github.com/katomaro/katomart/archive/refs/heads/master.zip"
    zip_filename = "master.zip"
    download_zip(zip_url, zip_filename)
    extract_zip(zip_filename)
    os.remove(zip_filename)
    move_contents_from_folder("katomart-master")
    print("A atualização foi concluída com sucesso!")

if __name__ == "__main__":
    main()
