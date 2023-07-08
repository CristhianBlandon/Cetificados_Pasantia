from mysql.connector import connect
from config import Config
from .logger import logger

def coneccion_db():
    try:
        conec_mysql =   connect(
            host    =   Config.MYSQL_HOST,
            user    =   Config.MYSQL_USER,
            password=   Config.MYSQL_PASS,
            db      =   Config.MYSQL_DB
        )
        return conec_mysql
    except Exception as e:
        # Si hay un error, registra el error en el archivo de log
        logger.error(f'Error en la coneccion a la base de datos: {e}')
        raise e  # Lanza la excepción para que el programa no continúe