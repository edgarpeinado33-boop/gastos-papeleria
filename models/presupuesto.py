from config.supabase_client import get_db
from datetime import datetime
from models.gasto import Gasto

class Presupuesto:
    """
    Patrón Singleton para manejar el presupuesto activo
    Solo existe una instancia del presupuesto en toda la aplicación
    """
    
    _instancia = None
    _presupuesto_actual = None
    
    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._cargar_presupuesto()
        return cls._instancia
    
    def _cargar_presupuesto(self):
        """Cargar presupuesto activo desde Supabase"""
        db = get_db()
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        
        try:
            result = db.table('presupuesto').select('*').eq('mes', mes_actual).eq('anio', anio_actual).execute()
            
            if result.data:
                self._presupuesto_actual = result.data[0]
            else:
                # Presupuesto por defecto si no existe
                self._presupuesto_actual = {'monto_limite': 1500.00, 'mes': mes_actual, 'anio': anio_actual}
        except Exception as e:
            print(f"Error al cargar presupuesto: {e}")
            self._presupuesto_actual = {'monto_limite': 1500.00}
    
    def obtener_limite(self) -> float:
        return self._presupuesto_actual.get('monto_limite', 1500.00)
    
    def verificar_disponibilidad(self, monto_gasto: float, mes: int, anio: int) -> tuple:
        """Verificar si hay presupuesto disponible"""
        total_gastado = Gasto.total_por_mes(mes, anio)
        disponible = self.obtener_limite() - total_gastado
        disponible_restante = disponible - monto_gasto
        
        if monto_gasto <= disponible:
            return True, disponible, disponible_restante
        return False, disponible, disponible_restante
    
    def obtener_total_gastado_mes_actual(self) -> float:
        """Obtener total gastado en el mes actual"""
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        return Gasto.total_por_mes(mes_actual, anio_actual)