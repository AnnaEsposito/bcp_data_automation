# etl/descargar_excel.py
import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Configuración de la carpeta de descarga
DOWNLOAD_DIR = os.path.abspath("data/raw_excel")

def configurar_chrome_para_descargas(download_path):
    options = webdriver.ChromeOptions()
    prefs = {
        "download.default_directory": download_path,
        "directory_upgrade": True,
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    options.add_experimental_option("prefs", prefs)
    return options

def borrar_archivos_anteriores():
    for archivo in os.listdir(DOWNLOAD_DIR):
        if archivo.endswith(".xlsx"):
            os.remove(os.path.join(DOWNLOAD_DIR, archivo))

def obtener_archivo_mas_reciente():
    archivos = [os.path.join(DOWNLOAD_DIR, f) for f in os.listdir(DOWNLOAD_DIR) if f.endswith(".xlsx")]
    if not archivos:
        return None
    return max(archivos, key=os.path.getctime)

def descargar_anexo_informe():
    # Asegurarse de que la carpeta existe
    os.makedirs(DOWNLOAD_DIR, exist_ok=True)
    borrar_archivos_anteriores()

    # Configurar Selenium
    service = Service("chromedriver-win64/chromedriver.exe")  # Ajustá esta ruta
    options = configurar_chrome_para_descargas(DOWNLOAD_DIR)
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get("https://www.bcp.gov.py/anexo-estadistico-del-informe-economico-i1507")
        time.sleep(5)
        link_texto = "Clic aquí para ver el documento"
        link_excel = driver.find_element(By.LINK_TEXT, link_texto)
        link_excel.click()
        print("⏬ Descarga iniciada...")

        time.sleep(15)  # Esperar que termine de descargar

        archivo_descargado = obtener_archivo_mas_reciente()
        if archivo_descargado:
            print(f"✅ Archivo descargado: {archivo_descargado}")
            return archivo_descargado
        else:
            print("❌ No se encontró el archivo descargado.")
            return None

    except Exception as e:
        print(f"❌ Error al descargar el archivo: {e}")
        return None
    finally:
        driver.quit()
