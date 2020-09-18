# coding:utf-8
import logging.config
import asyncio
import asyncpg
import time
import concurrent.futures

logging.config.fileConfig("logging.conf")
logger = logging.getLogger(__name__)






async def connect():
    pool = await asyncpg.create_pool(database='test',
                                     user='postgres',
                                     password='123456',
                                     host='127.0.0.1')
    return pool

async def execSQL(pool, sql):
    async with pool.acquire() as connection:
    # Open a transaction.
        async with connection.transaction():
            # Run the query passing the request argument.
            result = await connection.fetchval(sql)
            logger.info("Message show : {}".format(result))
            return result

# 回调函数

async def parse(task):
    #result():返回的就是特殊函数的返回值
    result = task.result()
    logger.info(result)


async def main():
    
    # 生成连接池
    pool = await connect()
    # create database
    # sql = """
    #     CREATE TABLE COMPANY(
    #     ID INT PRIMARY KEY     NOT NULL,
    #     NAME           TEXT    NOT NULL,
    #     AGE            INT     NOT NULL,
    #     ADDRESS        CHAR(50),
    #     SALARY         REAL,
    #     JOIN_DATE	  DATE
    #     ); """
    # await execSQL(pool, sql)   

    # insert data
    
    # for i in range(1, 10000): 
    #     sql = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE)  VALUES ({}, 'Paul{}', 32, 'California', 20000.00 ,'2001-07-13');".format(i, i)
    #     await execSQL(pool, sql)
    # 使用异步连接池
    for j in range(1, 10000):
        sql = "select * from COMPANY where ID={};".format(j)
        await execSQL(pool, sql)

    # 线程池
    # sql_list = []
    # for k in range(1, 10000):
    #     sql = "select * from COMPANY where ID={};".format(k)
    #     sql_list.append(sql)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     # Start the load operations and mark each future with its URL
    #     future_to_url = {executor.submit(execSQL, pool, ss): ss for ss in sql_list}
    #     for future in concurrent.futures.as_completed(future_to_url):
    #         try:
    #             data = future.result()
    #             logger.info(data)
    #         except Exception as exc:
    #             logger.exception(exc)



if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    app = loop.run_until_complete(main())
    print("time end {}".format(time.time() - start))
