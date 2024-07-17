import pymysql
from .celery_conf import celery_app
__all__ = ('celery_app',)
pymysql.install_as_MySQLdb()

