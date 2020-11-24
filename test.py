from pakages.stock_management.StockManagement import StockManagement as SM

stock = {
    'st01': 60,
    'br01': 60
}

datas = SM.getStock()
for d in datas:
    print(d)
SM.setStock(stock)
datas = SM.getStock()
for d in datas:
    print(d)