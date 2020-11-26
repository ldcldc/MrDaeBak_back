from ..db_model.mysqldb_conn import conn_mysqldb
import pymysql

class StockManagement:
    @staticmethod
    def getStock(id=None):
        """
            id(menu_id) 값을 받지 않으면 전체 행을 반환
            id가 있을 경우 해당하는 값만 반환

            반환 형태
            [
                {
                    menu_id: "..",
                    menu_name: "..",
                    stock: 0,
                    note: "..",
                }, {
                    ...
                }
            ]
        """
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
    def setStock(data: list[dict[str, str]]): 
        """
        인수 형태
            [
                {
                    menu_id: "..",
                    menu_name: "..",
                    stock: 0,
                    note: "..",
                }, {
                    ...
                }
            ]

        """
        db = conn_mysqldb()
        db_cursor = db.cursor()

        sql = """
                UPDATE menus
                SET menu_name=%s, stock=%s, note=%s
                WHERE menu_id=%s
                """

        for d in data:
            try:
                db_cursor.execute(sql, (d['menu_name'], str(d['stock']), d['note']))
            except pymysql.err.InternalError as e:
                code, msg = e.args
                print(code, msg)

        db.commit() 
        db.close()

        return True