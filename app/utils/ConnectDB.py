import pymysql

# #数据库配置信息
# host='120.79.89.116'
# user='root'
# passwd='Xuh781787'
# db='owl'
# port=3306
# charset='utf8'


class ConnectDB:
    def __init__(self):
        self.host = '120.79.89.116'
        self.user = 'root'
        self.passwd = 'Xuh781787'
        self.db = 'owl'
        self.port = 3306
        self.charset = 'utf8'

    #建立连接
    def getConnect(self):
        # 连接数据库
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=self.port,charset=self.charset)
        print('connect mysql success')
        return conn

    #断开连接
    def closedConnect(self,conn):
        conn.close()  # 释放数据库资源
        print('disconnect mysql')

    #数据库操作
    def queryDB(self,conn,sql):
        global comment
        cursor = conn.cursor()
        print("执行SQL语句：",sql)
        try:
            conn.ping()
            cursor.execute(sql)
            conn.commit()
            comment = cursor.fetchall()
            print('operation success')
            # print('comment:',comment)
        except:
            conn.ping(True)
            conn.rollback()
            print('operation error')
        finally:
            cursor.close()  # 关闭游标
        return comment

    #返回搜索语句
        #通过关键字限制进行查询（返回所有）
        #select * from DB where colName = 'keyWord'
    def searchByDBColKey_All(self,DBName,colName,keyWord,conn):
        sql = "select * from %s where %s = '%s'" %(DBName,colName,keyWord)
        results = self.queryDB(conn,sql)
        self.closedConnect(conn)
        return results

        #无关键字限制查询（限制查询列）
        # select colName from DB
    def searchColByDB(self, DBName, colName,conn):
        sql = "select %s from %s " % (DBName, colName)
        results = self.queryDB(conn,sql)
        self.closedConnect(conn)
        return results


    #返回插入语句
    #List[V1,V2,V3...]
    def insertDBSql(self,DBName,insertLists,conn):
        DBDetails = self.showDBDetails(DBName,conn)
        cols = []
        for DBDeatil in DBDetails:
            cols.append(DBDeatil[0])
        # print(cols)
        sql1 = "insert into %s (" %DBName
        sql2 = ""
        for col in cols[1:-1]:
            col = col+','
            sql2 += col
        sql2+=cols[-1]
        sql3 = ") values ("
        sql4 = ""
        for insertList in insertLists[:-1]:
            insertList = "'"+insertList+"',"
            sql4 += insertList
        sql4 += "'"+insertLists[-1]+"'"
        sql = sql1+sql2+sql3+sql4+')'
        results = self.queryDB(conn,sql)
        self.closedConnect(conn)
        return results

    #返回DB的建表信息
    #('OCid', 'int(11)', 'NO', 'PRI', None, 'auto_increment')
    def showDBDetails(self,DBName,conn):
        sql = "desc %s" % DBName
        results = self.queryDB(conn, sql)
        self.closedConnect(conn)
        return results

if __name__ == "__main__":
    lists = [0,1,2,3,4,5]
    for list in lists[1:-1]:
        print(list)
    print(lists[-1])


