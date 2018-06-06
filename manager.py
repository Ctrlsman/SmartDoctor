# -*- coding：utf-8 -*-
from flask.cli import main
from doctor import create_app
from doctor import config

app = create_app()


@app.cli.command()
def start():
    host = config.HTTP_HOST
    port = config.HTTP_PORT
    print('* Running on http://{}:{}/ (Press CTRL+C to quit)'.format(host, port))
    app.run(host=host, port=port, use_reloader=False)


if __name__ == '__main__':
    main()
