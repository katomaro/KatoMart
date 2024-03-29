import os
import shutil
from zipfile import ZipFile
import requests

def should_keep(file):
    return file in ["atualizar.py", "Cursos", "jsons", "main.sqlite3"]

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

# Função para extrair o conteúdo do ZIP
def extract_zip(filename):
    with ZipFile(filename, 'r') as zip_ref:
        zip_ref.extractall()

# Função principal
def main():
    print("Atualização do sistema Katomart. IMPORTANTE: Se você estiver executando após o dia XX/XX/XXXX, delete o arquivo 'main.sqlite3' manualmente para que ele seja recriado corretamente. Você precisará reconfigurar o sistema ao fazer isso. Não delete a pasta jsons nem a pasta cursos para atualizar.")
    user_consent = input("Deseja atualizar o sistema? (s/n)\n").strip().lower()
    if user_consent != "s":
        print("A atualização foi cancelada pelo usuário.")
        return
    clean_directory()  # Limpa o diretório
    zip_url = "https://github.com/katomaro/katomart/archive/refs/heads/master.zip"
    zip_filename = "master.zip"
    download_zip(zip_url, zip_filename)  # Baixa o ZIP
    extract_zip(zip_filename)  # Extrai o conteúdo
    os.remove(zip_filename)  # Remove o arquivo ZIP
    print("A atualização foi concluída com sucesso!")

if __name__ == "__main__":
    main()
