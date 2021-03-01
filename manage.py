import pymysql
from newblog import create_app


pymysql.install_as_MySQLdb()
app = create_app('dev')
