from ..db_model.mysqldb_conn import conn_mysqldb
import pymysql

class StockManagement:
    @staticmethod
    def getStock(id=None):
        db = conn_mysqldb()
        db_cursor = db.cursor()

        if id is None:
            sql = """
                    SELECT menu_id, menu_name, stock, note
                    FROM menus;
                    """
            db_cursor.execute(sql)
        else:
            sql = """
                    SELECT menu_id, menu_name, stock, note
                    FROM menus
                    WHERE menu_id=%s
                    """
            db_cursor.execute(sql, id)
        

        datas = []
        for _ in range(db_cursor.rowcount):
            menu_id, menu_name, stock, note = db_cursor.fetchone()
            datas.append({
                'menu_id' : menu_id,
                'menu_name': menu_name,
                'stock' : stock,
                'note' : note,
            })

        db.close()
        
        return datas

    @staticmethod
    def setStock(curStocks: dict[str, str]): # [ [ menu_id, stock ] ]
        db = conn_mysqldb()
        db_cursor = db.cursor()

        sql = """
                UPDATE menus
                SET stock=%s
                WHERE menu_id=%s
                """

        for st in curStocks.items():
            try:
                db_cursor.execute(sql, (str(st[1]), st[0]))
            except pymysql.err.InternalError as e:
                code, msg = e.args
                print(code, msg)

        db.commit() 
        db.close()

        return True