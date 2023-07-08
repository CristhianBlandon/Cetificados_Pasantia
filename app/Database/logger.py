import logging

# Crea un objeto logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Crea un archivo de log y agrega un manejador
handler = logging.FileHandler('App/Database/database_errors.log')
handler.setLevel(logging.ERROR)

# Define el formato de los mensajes en el archivo de log
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Agrega el manejador al logger
logger.addHandler(handler)