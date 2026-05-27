from config.supabase_client import get_db
from datetime import date

class Gasto:
    """Modelo para gestionar gastos"""
    
    @staticmethod
    def crear(gasto_data: dict) -> dict:
        """Crear un nuevo gasto en Supabase"""
        db = get_db()
        data = {
            'concepto': gasto_data['concepto'],
            'categoria': gasto_data['categoria'],
            'monto': float(gasto_data['monto']),
            'fecha': gasto_data.get('fecha', str(date.today())),
            'justificacion': gasto_data.get('justificacion', ''),
            'estado': 'aprobado'
        }
        
        try:
            result = db.table('gastos').insert(data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error al crear gasto: {e}")
            return None
    
    @staticmethod
    def listar_todos(limite: int = 100):
        """Obtener todos los gastos ordenados por fecha"""
        db = get_db()
        try:
            result = db.table('gastos').select('*').order('fecha', desc=True).limit(limite).execute()
            return result.data
        except Exception as e:
            print(f"Error al listar gastos: {e}")
            return []
    
    @staticmethod
    def filtrar_por_mes(mes: int, anio: int):
        """Filtrar gastos por mes y año"""
        db = get_db()
        try:
            result = db.table('gastos').select('*').execute()
            gastos = result.data
            
            filtrados = [
                g for g in gastos 
                if g.get('fecha') and int(g['fecha'].split('-')[1]) == mes 
                and int(g['fecha'].split('-')[0]) == anio
            ]
            return filtrados
        except Exception as e:
            print(f"Error al filtrar gastos: {e}")
            return []
    
    @staticmethod
    def total_por_mes(mes: int, anio: int) -> float:
        """Calcular total gastado en un mes específico"""
        gastos = Gasto.filtrar_por_mes(mes, anio)
        return sum(g['monto'] for g in gastos)
    
    @staticmethod
    def obtener_categorias():
        """Obtener lista de categorías desde Supabase"""
        db = get_db()
        try:
            result = db.table('categorias').select('nombre').execute()
            return [c['nombre'] for c in result.data]
        except Exception as e:
            print(f"Error al obtener categorías: {e}")
            return ['Papeleria Basica', 'Toner y Cartuchos', 'Mobiliario', 'Transporte', 'Viaticos', 'Imprevistos']