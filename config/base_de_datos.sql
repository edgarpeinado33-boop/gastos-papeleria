-- Tabla de gastos
CREATE TABLE IF NOT EXISTS gastos (
    id SERIAL PRIMARY KEY,
    concepto VARCHAR(200) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    justificacion TEXT,
    estado VARCHAR(20) DEFAULT 'aprobado',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de presupuesto mensual
CREATE TABLE IF NOT EXISTS presupuesto (
    id SERIAL PRIMARY KEY,
    mes INTEGER NOT NULL,
    anio INTEGER NOT NULL,
    monto_limite DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(mes, anio)
);

-- Tabla de categorías
CREATE TABLE IF NOT EXISTS categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) UNIQUE NOT NULL,
    requiere_comprobante BOOLEAN DEFAULT TRUE,
    requiere_justificacion BOOLEAN DEFAULT FALSE,
    limite_diario DECIMAL(10,2)
);

-- Insertar categorías
INSERT INTO categorias (nombre, requiere_comprobante, limite_diario) VALUES
('Papeleria Basica', TRUE, 50.00),
('Toner y Cartuchos', TRUE, 200.00),
('Mobiliario', TRUE, 500.00),
('Transporte', TRUE, 30.00),
('Viaticos', TRUE, 100.00),
('Imprevistos', TRUE, 50.00)
ON CONFLICT (nombre) DO NOTHING;

-- Insertar presupuesto inicial (Mes actual)
INSERT INTO presupuesto (mes, anio, monto_limite) 
VALUES (EXTRACT(MONTH FROM CURRENT_DATE), EXTRACT(YEAR FROM CURRENT_DATE), 1500.00)
ON CONFLICT (mes, anio) DO NOTHING;
-- 1. Configurar zona horaria para la sesión
SET timezone = 'America/La_Paz';

-- 2. Modificar la columna fecha para usar zona horaria Bolivia
ALTER TABLE gastos 
ALTER COLUMN fecha SET DEFAULT (CURRENT_DATE AT TIME ZONE 'America/La_Paz');

-- 3. Modificar created_at
ALTER TABLE gastos 
ALTER COLUMN created_at SET DEFAULT (NOW() AT TIME ZONE 'America/La_Paz');

-- 4. Verificar
SHOW timezone;
SELECT CURRENT_DATE AT TIME ZONE 'America/La_Paz' as fecha_bolivia;