'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-09-18 09:13:33
LastEditTime: 2020-09-18 10:30:29
'''
import time
import concurrent.futures
import psycopg2
import logging.config
logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)

def connect(sql):
    conn = psycopg2.connect("dbname=test user=postgres password=123456 host=127.0.0.1")
    cur = conn.cursor()
    cur.execute(sql)
    for row in cur.fetchall():
        logger.info(row)
    conn.commit()
    cur.close()
    conn.close()

def threadPool():
    sql_list = []
    for i in range(1, 1000):
        sql = "select * from COMPANY where ID={};".format(i)
        sql_list.append(sql)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # for sql in sql_list:
        #     executor.submit(connect, sql)
        result = {executor.submit(connect, sql): sql for sql in sql_list}
        for r in result:
            try:
                logging.info(r.result())
            except Exception as e:
                logging.exception(e)

def tp():
    from psycopg2.pool import ThreadedConnectionPool
    pool = ThreadedConnectionPool(10,10, "dbname=test user=postgres password=123456 host=127.0.0.1")
    conn = pool.getconn()
    cursor=conn.cursor()
    for i in range(1, 1000):
        sql = "select * from COMPANY where ID={};".format(i)
        cursor.execute(sql)
        for row in cursor.fetchall():
            logger.info(row)
    pool.putconn(conn)
    pool.closeall()
if __name__ == '__main__':
    sql = "select * from COMPANY where ID=1;"
    # connect(sql)
    start = time.time()
    # threadPool()
    tp()
    logging.info('runing time : {}'.format(time.time() - start))