from flask import request, render_template, redirect, url_for
from models.gasto import Gasto
from models.presupuesto import Presupuesto
from models.estrategia import EstrategiaFactory
from datetime import datetime

class GastoController:
    """Controlador que maneja las peticiones HTTP y orquesta Modelos y Vistas"""
    
    @staticmethod
    def mostrar_dashboard():
        """Vista principal: Dashboard con resumen de gastos"""
        presupuesto = Presupuesto()
        limite = presupuesto.obtener_limite()
        
        mes_actual = datetime.now().month
        anio_actual = datetime.now().year
        total_gastado = Gasto.total_por_mes(mes_actual, anio_actual)
        
        gastos_recientes = Gasto.listar_todos(10)
        
        porcentaje = (total_gastado / limite) * 100 if limite > 0 else 0
        
        # Patrón Observer: Alertas automáticas basadas en el porcentaje
        alertas = []
        if porcentaje >= 100:
            alertas.append("🚨 ¡URGENTE! Has excedido el presupuesto mensual")
        elif porcentaje >= 80:
            alertas.append(f"⚠️ ¡Alerta! Has usado el {porcentaje:.0f}% del presupuesto mensual")
        elif porcentaje >= 60:
            alertas.append(f"📊 Has usado el {porcentaje:.0f}% de tu presupuesto")
        
        # Obtener mensaje de éxito de la URL (sin SECRET_KEY)
        mensaje_exito = request.args.get('mensaje', None)
        
        return render_template('index.html', 
                             total_gastado=total_gastado,
                             limite=limite,
                             porcentaje=porcentaje,
                             gastos_recientes=gastos_recientes,
                             alertas=alertas,
                             mensaje_exito=mensaje_exito)
    
    @staticmethod
    def registrar_gasto():
        """Registrar un nuevo gasto con validación por Strategy"""
        categorias = Gasto.obtener_categorias()
        
        if request.method == 'POST':
            datos = {
                'concepto': request.form.get('concepto'),
                'categoria': request.form.get('categoria'),
                'monto': float(request.form.get('monto')),
                'justificacion': request.form.get('justificacion', '')
            }
            
            # 1. Validar con Strategy según categoría
            estrategia = EstrategiaFactory.get_estrategia(datos['categoria'])
            valido, mensaje = estrategia.validar(datos)
            
            if not valido:
                return render_template('registrar.html', 
                                     error=mensaje, 
                                     categorias=categorias)
            
            # 2. Verificar presupuesto disponible
            presupuesto = Presupuesto()
            ahora = datetime.now()
            disponible, disponible_actual, restante = presupuesto.verificar_disponibilidad(
                datos['monto'], 
                ahora.month, 
                ahora.year
            )
            
            if not disponible:
                return render_template('registrar.html', 
                                     error=f"❌ Presupuesto insuficiente. Disponible: Bs {disponible_actual:.2f}",
                                     categorias=categorias)
            
            # 3. Guardar en Supabase
            gasto = Gasto.crear(datos)
            
            if gasto:
                # Redirigir al dashboard con mensaje en la URL (sin flash, sin SECRET_KEY)
                mensaje = f"✅ ¡Gasto registrado! Se gastaron Bs {datos['monto']:.2f} en {datos['concepto']}"
                return redirect(url_for('index', mensaje=mensaje))
            else:
                return render_template('registrar.html', 
                                     error="❌ Error al guardar en la base de datos",
                                     categorias=categorias)
        
        # GET: Mostrar formulario
        return render_template('registrar.html', categorias=categorias)
    
    @staticmethod
    def reportes():
        """Vista de reportes con filtros y gráficos"""
        mes = request.args.get('mes', type=int, default=datetime.now().month)
        anio = request.args.get('anio', type=int, default=datetime.now().year)
        
        gastos = Gasto.filtrar_por_mes(mes, anio)
        total = sum(g['monto'] for g in gastos)
        
        # Agrupar por categoría
        categorias_dict = {}
        for g in gastos:
            cat = g['categoria']
            categorias_dict[cat] = categorias_dict.get(cat, 0) + g['monto']
        
        # Datos para el gráfico
        categorias_json = {
            'labels': list(categorias_dict.keys()),
            'values': list(categorias_dict.values())
        }
        
        return render_template('reportes.html', 
                             gastos=gastos, 
                             total=total,
                             mes=mes,
                             anio=anio,
                             categorias=categorias_json)