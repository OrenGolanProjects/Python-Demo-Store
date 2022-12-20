import mysql.connector as mc
import sqlite3


class database_mysql:
    def __init__(self) -> None:
        self.host = "localhost"
        self.root = "root"
        self.password = 'Og305275@'
        self.schema = 'shope'
        self.databaseConnection = None

    def create_connection_MYSQL(self):
        try:
            conn = mc.connect(host=self.host, user=self.root,
                              password=self.password, database=self.schema)
            if conn.is_connected():
                self.databaseConnection = conn

        except mc.error as e:
            print("DB Connect failed, error is: " + e)


class customer:
    def __init__(self) -> None:
        self.Role = None
        self.Password = None
        self.UserName = None
        self.Id = None
        self.isCustomerExists = False
        self.customers = None

    def getCustomer(self, db_connection, bool_sqlite3):
        res = None
        """
        By user name and password, run query that gets all the details about customer.

        :param db_connection:
        :param user_name:
        :param password:
        :return: tuple of: customer details
        """

        try:
            if bool_sqlite3 == True:
                cur = db_connection.cursor()
                cur.execute("""
                SELECT IdCustomer,UserName,Password,Role
                from customers
                WHERE UserName= :UserName and Password=:Password
                """, {'UserName': self.UserName, 'Password': self.Password})
                res = cur.fetchall()

            else:
                cur = db_connection.cursor(prepared=True)
                sql = """
                select IdCustomer,UserName,Password,Role from customers
                where UserName = %s and Password = %s
                """
                cur.execute(sql, (self.UserName, self.Password))
                res = cur.fetchall()
        except mc.Error as e:
            print("Execute failed!")
            print(e)
        else:
            if len(res) > 0:
                self.Id = int(res[0][0])
                self.Role = str(res[0][3])
                self.isCustomerExists = True
            else:
                self.isCustomerExists = False

    def getCustomers(self, db_connection, bool_sqlite3):
        """
        Get all customers

        :param db_connection:
        :return: list of tuple
        """
        if bool_sqlite3 == True:
            cur = db_connection.cursor()
        else:
            cur = db_connection.cursor(prepared=True)
        sql = """
        select IdCustomer,UserName,Password,Role from customers
        """
        try:
            cur.execute(sql)
            res = cur.fetchall()
        except mc.Error as e:
            print("Execute failed!")
            print(e)
        else:
            self.customers = res


class product:
    def __init__(self) -> None:
        self.Id = None
        self.Name = None
        self.Description = None
        self.Price = None
        self.products = None

    def GetAppProducts(self, db_connection, bool_sqlite3):
        """
        :param db_connection:
        :return: Function that returns all the products in the data base.
        """
        if bool_sqlite3 == True:
            cur = db_connection.cursor()
        else:
            cur = db_connection.cursor(prepared=True)
        sql = """
        select IdProduct,Name,Description,Price from product
        """
        try:
            cur.execute(sql)
            tup_reportValues = cur.fetchall()
        except mc.Error as e:
            print("Execute failed!")
            print(e)
        else:
            self.products = tup_reportValues


class cart:
    def __init__(self) -> None:
        self.Id = None
        self.idCustomer = None
        self.idProduct = None
        self.Quantity = 0
        self.isInsertSucceeded = False
        self.goldCustomers = None

    def AddProductToCustomerTranscation(self, db_connection, bool_sqlite3):
        """
        :param db_connection:
        :param id_customer:
        :param id_product:
        :param quantity:
        :return: True - insert to db a row successfully, False - failed to insert row.
        """

        try:
            if bool_sqlite3 == True:
                cur = db_connection.cursor()
                cur.execute("INSERT INTO ProductToCustomer VALUES (:IdProductToCustomer,:IdCustomer,:IdProduct,:Quantity)", {
                    'IdProductToCustomer': None, 'IdCustomer': self.IdCustomer, 'IdProduct': self.IdProduct, 'Quantity': self.Quantity})
                db_connection.commit()
            else:
                cur = db_connection.cursor(prepared=True)
                sql = """INSERT INTO shope.producttocustomer(`idCustomer`, `IdProduct`, `Quantity`) values( % s, % s, % s); """
                cur.execute(
                    sql, (self.idCustomer, self.idProduct, self.Quantity))
                db_connection.commit()

        except mc.Error as e:
            print(e)
            raise Exception(
                "Execute insert AddProductToCustomerTranscation Failed!")
        except sqlite3.Error as e:
            print(e)
            raise Exception(
                "Execute insert AddProductToCustomerTranscation Failed!")
        else:
            self.isInsertSucceeded = True
        finally:
            cur.close()

    def GetCustomerGoldReport(self, db_connection, bool_sqlite3):
        """: param db_connection: : return: The sum amount of money that each customer paid for products.
        """

        try:
            if bool_sqlite3 == True:
                cur = db_connection.cursor()
                cur.execute("""
                                select cp.IdCustomer, UserName, sum((Quantity*Price)) as sumPrice
                                from ProductToCustomer cp
                                inner join product p
                                on cp.IdProduct=p.IdProduct
                                inner join  customers c
                                on cp.IdCustomer=c.IdCustomer
                                group by UserName, cp.IdCustomer
                                order by sumPrice desc;
                            """)
            else:
                cur = db_connection.cursor(prepared=True)
                sql = """
                    select cp.IdCustomer, UserName, sum((Quantity*Price)) as sumPrice
                    from producttocustomer cp
                    inner join product p
                    on cp.IdProduct=p.IdProduct
                    inner join  customers c
                    on cp.IdCustomer=c.IdCustomer
                    group by UserName, cp.IdCustomer
                    order by sumPrice desc;
                """
                cur.execute(sql)
            tup_productList = cur.fetchall()
        except mc.Error as e:
            print("Execute failed!")
            print(e)
        else:
            print("Function GetAppProducts, Execute successful!")
            self.goldCustomers = tup_productList


class database_sqlite3:
    def __init__(self) -> None:
        self.schema = 'sqlite3\shope.db'
        self.databaseconnection = None
        self.isconnected = False
        self.tableName = None

    def create_connection_sqlite3(self):
        conn = None
        try:
            conn = sqlite3.connect(f"{self.schema}", check_same_thread=False)
        except sqlite3.Error as e:
            print(f"Database connection failed, error is: {e}")
        finally:
            self.databaseconnection = conn

    def insert(self):
        curser = self.databaseconnection.cursor()
        if self.tableName == 'customers':
            if not hasattr(self, 'UserName'):
                raise Exception("UserName not in object self")

            elif not hasattr(self, 'Password'):
                raise Exception("Password not in object self")
            elif not hasattr(self, 'Role'):
                raise Exception("Role not in object self")
            else:
                try:
                    curser.execute("INSERT INTO customers VALUES (:IdCustomer,:UserName,:Password,:Role)", {
                        'IdCustomer': None, 'UserName': self.UserName, 'Password': self.Password, 'Role': self.Role})
                    print("insert table customers done.")
                except sqlite3.Error as e:
                    print(e)

        if self.tableName == 'product':
            if not hasattr(self, 'Name'):
                raise Exception("Name not in object self")
            elif not hasattr(self, 'Description'):
                raise Exception("Description not in object self")
            elif not hasattr(self, 'Price'):
                raise Exception("Price not in object self")
            elif not hasattr(self, 'IdProduct'):
                raise Exception("IdProduct not in object self")
            else:
                try:
                    curser.execute("INSERT INTO product VALUES (:IdProduct,:Name,:Description,:Price)", {
                        'IdProduct': self.IdProduct, 'Name': self.Name, 'Description': self.Description, 'Price': float(self.Price)})
                    print(f"insert id: {self.IdProduct} done.")
                except sqlite3.Error as e:
                    print(e)

        if self.tableName == 'ProductToCustomer':

            if not hasattr(self, 'IdCustomer'):
                raise Exception("IdCustomer not in object self")
            elif not hasattr(self, 'IdProduct'):
                raise Exception("IdProduct not in object self")
            elif not hasattr(self, 'Quantity'):
                raise Exception("Quantity not in object self")

            else:
                try:
                    curser.execute("INSERT INTO ProductToCustomer VALUES (:IdCustomer,:IdProduct,:Quantity)", {
                        'IdCustomer': self.IdCustomer, 'IdProduct': self.IdProduct, 'Quantity': self.Quantity})
                    print("insert table customers done.")
                except sqlite3.Error as e:
                    print(e)

        self.databaseconnection.commit()
        curser.close()

    def update(self):
        raise Exception("update function not avalible")

    def delete(self):
        raise Exception("delete function not avalible")
