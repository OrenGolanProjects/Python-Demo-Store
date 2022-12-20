from Classes.processSetup import *


obj_db_sqlit3 = database_sqlite3()
obj_db_sqlit3.create_connection_sqlite3()

# con = obj_db_sqlit3.databaseconnection.cursor()
# con.execute('SELECT name from sqlite_master where type= "table"')
# print(con.fetchall())
# con.close()


# obj_db = database_mysql()
# obj_db.create_connection_MYSQL()
# obj_customer = customer()
# obj_product = product()
# obj_cart = cart()


# obj_product.GetAppProducts(obj_db.databaseConnection)

# obj_db_sqlit3.tableName = "ProductToCustomer"
# con = obj_db_sqlit3.databaseconnection.cursor()
# con.execute("select * from ProductToCustomer")


# con.execute("""
#                 select cp.IdCustomer, UserName, sum((Quantity*Price)) as sumPrice
#                 from ProductToCustomer cp
#                 inner join product p
#                 on cp.IdProduct=p.IdProduct
#                 inner join  customers c
#                 on cp.IdCustomer=c.IdCustomer
#                 group by UserName, cp.IdCustomer
#                 order by sumPrice desc;
#             """)
# lst_items = con.fetchall()
# # print()
# for product in lst_items:
#     print(product)
#     obj_db_sqlit3.IdProductToCustomer = product[0]
#     obj_db_sqlit3.IdCustomer = product[1]
#     obj_db_sqlit3.IdProduct = product[2]
#     obj_db_sqlit3.Quantity = product[3]
obj_db_sqlit3.tableName = "customers"
obj_db_sqlit3.UserName = "admin"
obj_db_sqlit3.Password = 123
obj_db_sqlit3.Role = "admin"
obj_db_sqlit3.insert()

# con.close()


# try:
#     con = obj_db_sqlit3.databaseconnection.cursor()
#     con.execute("DROP TABLE ProductToCustomer")
#     con.close()
#     print("delete table ProductToCustomer success")
# except sqlite3.Error as e:
#     print(e)

# con = obj_db_sqlit3.databaseconnection.cursor()
# con.execute('PRAGMA table_info("ProductToCustomer");')
# print(con.fetchall())
# con.close()

# obj_db_sqlit3.databaseconnection.execute("""
# CREATE TABLE `ProductToCustomer` (`IdProductToCustomer` 						INTEGER PRIMARY KEY AUTOINCREMENT ,
#                                           `IdCustomer`								 		INT NOT NULL,
#                                           `IdProduct` 										INT NOT NULL,
#                                           `Quantity`				 						INT NOT NULL DEFAULT 1,
#                                           FOREIGN KEY(`IdCustomer`) REFERENCES customers(`IdCustomer`) ,
#                                           FOREIGN KEY(`IdProduct`) REFERENCES product(`IdProduct`)
#                                   )
# """)

# con = obj_db_sqlit3.databaseconnection.cursor()
# con.execute('PRAGMA table_info("ProductToCustomer");')
# print(con.fetchall())
# con.close()


# bool_sqlite3 = True
# obj_db_sqlit3.create_connection_sqlite3()

# obj_customer.getCustomers(obj_db_sqlit3.databaseconnection, bool_sqlite3)
# print(obj_customer.customers)

# print("")
# print("")
# print("")

# obj_product.GetAppProducts(obj_db_sqlit3.databaseconnection, bool_sqlite3)
# print(obj_product.products)

# print("")
# print("")
# print("")

# obj_cart.GetCustomerGoldReport(obj_db_sqlit3.databaseconnection, bool_sqlite3)
# print(obj_cart.goldCustomers)
