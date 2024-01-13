"""Ponto de inicialização para um futuro server Flask"""

from flask import Flask, render_template

from modules.databases.manager_main import ManagerMain

database_manager = ManagerMain()

app = Flask(__name__,
             template_folder='modules/front/templates',
               static_folder='modules/front/static'
            )
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/accounts')
def accounts():
    return render_template('accounts.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/log')
def log():
    return render_template('log.html')

@app.route('/support')
def support():
    return render_template('support.html')




if __name__ == '__main__':
    PORTA = 6102
    print('[INIT] Por favor, ignore todos os textos abaixo/acima, vá até o seu '
          f'navegador e acesse o endereço http://localhost:{PORTA}\n'
          'Estes textos são apenas de debug. Não feche esse terminal enquanto '
          'estiver utilizando o Katomart em sua interface web (porém você pode '
          'fechar o navegador e voltar até o site para gerenciar o Katomart quando quiser')

    app.run(debug=True, port=PORTA)
