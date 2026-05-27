from abc import ABC, abstractmethod

class EstrategiaValidacion(ABC):
    """
    Patrón Strategy: Interfaz para estrategias de validación
    Cada categoría de gasto tiene su propia validación
    """
    
    @abstractmethod
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        pass

class ValidacionPapeleriaBasica(EstrategiaValidacion):
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        if gasto_data['monto'] > 50:
            return False, "❌ Gastos de papelería básica no pueden superar Bs 50 por transacción"
        if not gasto_data.get('concepto') or len(gasto_data['concepto']) < 5:
            return False, "❌ El concepto debe tener al menos 5 caracteres"
        return True, "✅ Válido"

class ValidacionToner(EstrategiaValidacion):
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        if gasto_data['monto'] > 200:
            return False, "❌ Gastos de toner requieren aprobación especial (máximo Bs 200)"
        return True, "✅ Válido"

class ValidacionMobiliario(EstrategiaValidacion):
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        if not gasto_data.get('justificacion'):
            return False, "❌ Gastos de mobiliario requieren justificación detallada"
        if len(gasto_data['justificacion']) < 20:
            return False, "❌ Justificación debe tener al menos 20 caracteres"
        return True, "✅ Válido"

class ValidacionTransporte(EstrategiaValidacion):
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        if gasto_data['monto'] > 30:
            return False, "❌ Gastos de transporte no pueden superar Bs 30 por transacción"
        return True, "✅ Válido"

class ValidacionViaticos(EstrategiaValidacion):
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        if gasto_data['monto'] > 100:
            return False, "❌ Gastos de viáticos requieren aprobación (máximo Bs 100)"
        return True, "✅ Válido"

class ValidacionImprevistos(EstrategiaValidacion):
    def validar(self, gasto_data: dict) -> tuple[bool, str]:
        if not gasto_data.get('justificacion'):
            return False, "❌ Gastos imprevistos requieren justificación"
        return True, "✅ Válido"

class EstrategiaFactory:
    """Factory para obtener la estrategia según categoría"""
    
    @staticmethod
    def get_estrategia(categoria: str) -> EstrategiaValidacion:
        estrategias = {
            'Papeleria Basica': ValidacionPapeleriaBasica(),
            'Toner y Cartuchos': ValidacionToner(),
            'Mobiliario': ValidacionMobiliario(),
            'Transporte': ValidacionTransporte(),
            'Viaticos': ValidacionViaticos(),
            'Imprevistos': ValidacionImprevistos(),
        }
        return estrategias.get(categoria, ValidacionPapeleriaBasica())