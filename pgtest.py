'''
Author: xianxiaoyin
LastEditors: xianxiaoyin
Descripttion: 
Date: 2020-09-17 10:23:56
LastEditTime: 2020-09-17 11:34:38
'''
# coding:utf-8

import asyncio
import asyncpg
import time

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
            return result

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
    
    for i in range(1, 10000): 
        sql = "INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY,JOIN_DATE)  VALUES ({}, 'Paul{}', 32, 'California', 20000.00 ,'2001-07-13');".format(i, i)
        await execSQL(pool, sql)

start = time.time()
loop = asyncio.get_event_loop()
app = loop.run_until_complete(main())
print("time end {}".format(time.time() - start))