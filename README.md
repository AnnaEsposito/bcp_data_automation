# Paraguay Economic Indicators ETL

## 🌍 Contexto

En Paraguay, el acceso a los principales indicadores económicos provistos por el Banco Central del Paraguay (BCP) se realiza mediante archivos Excel estáticos. Este formato dificulta la automatización, el análisis dinámico y la integración de datos económicos en herramientas modernas de Business Intelligence y Ciencia de Datos.

## 🧩 Problema

Cada mes (o trimestre), analistas económicos deben descargar manualmente archivos Excel con múltiples cuadros, extraer manualmente los datos relevantes, procesarlos en Excel, y luego analizarlos. Este proceso es repetitivo, propenso a errores y poco escalable.

## 🎯 Objetivo del Proyecto

Automatizar el proceso de:

1. Descarga de los archivos Excel del BCP.
2. Extracción de los cuadros de indicadores seleccionados.
3. Transformación y limpieza de los datos.
4. Carga en una base de datos PostgreSQL estructurada.
5. Posibilitar su análisis desde dashboards y modelos predictivos.

## ⚙️ Tecnologías utilizadas

- Python
- Pandas
- Requests
- SQLAlchemy / psycopg2
- PostgreSQL
- Power BI (para visualización)

## 📊 Cuadros de indicadores seleccionados

- Producto Interno Bruto (PIB)
- Inflación
- Tipo de cambio
- Comercio exterior
- Tasas de interés

## 🚀 Estado actual

✅ Estructura del proyecto creada  
🔜 Implementación del flujo ETL automatizado

## 📁 Estructura del proyecto

(ver estructura de carpetas)

## 💡 Futuras mejoras

- Deploy del ETL en una nube (ej: cronjob en PythonAnywhere)
- Interfaz web para descarga bajo demanda
- Incorporación de APIs internacionales para comparar indicadores

Desarrollado por Anna Paula Esposito
