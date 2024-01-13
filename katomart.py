"""Ponto de inicialização para um futuro server Flask"""

from flask import Flask, render_template

from modules.databases.manager_main import ManagerMain

database_manager = ManagerMain()

app = Flask(__name__,
             template_folder='modules/front/templates',
               static_folder='modules/front/static'
            )

@app.route('/')
def katomart_root():
    return render_template('index.html')


if __name__ == '__main__':
    PORTA = 6102
    print('[INIT] Por favor, ignore todos os textos abaixo/acima, vá até o seu '
          f'navegador e acesse o endereço http://localhost:{PORTA}\n'
          'Estes textos são apenas de debug. Não feche esse terminal enquanto '
          'estiver utilizando o Katomart em sua interface web (porém você pode '
          'fechar o navegador e voltar até o site para gerenciar o Katomart quando quiser')

    app.run(debug=True, port=PORTA)
