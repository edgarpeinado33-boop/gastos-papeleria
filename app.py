from flask import Flask, send_from_directory
from controllers.gasto_controller import GastoController
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='views', static_folder='static')

# Servir archivos estáticos manualmente
@app.route('/static/<path:filename>')
def custom_static(filename):
    return send_from_directory('views/static', filename)

@app.route('/')
def index():
    return GastoController.mostrar_dashboard()

@app.route('/gasto/nuevo', methods=['GET', 'POST'])
def nuevo_gasto():
    return GastoController.registrar_gasto()

@app.route('/reportes')
def reportes():
    return GastoController.reportes()

if __name__ == '__main__':
    app.run(debug=True)