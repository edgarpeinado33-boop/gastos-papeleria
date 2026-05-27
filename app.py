from flask import Flask
from controllers.gasto_controller import GastoController
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, template_folder='views', static_folder='views/static')


# Rutas
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