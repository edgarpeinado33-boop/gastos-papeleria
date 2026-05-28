from flask import Flask
from controllers.gasto_controller import GastoController
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='views', static_folder='views/static')

# Asegurar que los archivos estáticos se sirvan correctamente
app.static_folder = 'views/static'
app.static_url_path = '/static'

@app.route('/')
def index():
    return GastoController.mostrar_dashboard()

@app.route('/gasto/nuevo', methods=['GET', 'POST'])
def nuevo_gasto():
    return GastoController.registrar_gasto()

@app.route('/reportes')
def reportes():
    return GastoController.reportes()

# Para Vercel - Forzar que sirva archivos estáticos
@app.route('/static/<path:filename>')
def serve_static(filename):
    return app.send_static_file(filename)

if __name__ == '__main__':
    app.run(debug=True)