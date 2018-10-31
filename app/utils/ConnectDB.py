import pymysql

#数据库配置信息
host='120.79.89.116'
user='root'
passwd='Xuh781787'
db='owl'
port=3306
charset='utf8'

class ConnectDB:
    #建立连接
    def getConnect(self):
        # 连接数据库
        conn = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port,charset=charset)
        print('连接mysql成功')
        return conn

    #断开连接
    def closedConnect(self,conn):
        conn.close()  # 释放数据库资源
        print('数据库已断开')

    #数据库操作
    def queryDB(self,conn,sql):
        cursor = conn.cursor()
        query = sql
        print(query)
        cursor.execute(query)
        comment = list(cursor.fetchall())
        #print(comment)
        cursor.close()  # 关闭游标
        return comment

