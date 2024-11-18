import logging
from servidor import create_app

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    encoding='utf-8',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
logging.getLogger('sqlalchemy.engine.Engine').setLevel(logging.WARNING)

app = create_app()


if __name__ == '__main__':
    app.run(port=6102, debug=False)
