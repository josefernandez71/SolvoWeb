from os import curdir
from colorama import Cursor
from .entities.Company import Company
from .entities.City import City
class ModelCompanyCity():
        
    @classmethod
    def ExistCompany(self, db, company):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT NOMBRE_COMPANIA FROM compania 
                    WHERE NOMBRE_COMPANIA = '{}'""".format(company.nombre)        
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                company = Company(0,row[0],"")
                return company
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def ExistCity(self, db, city):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT NOMBRE_CIUDAD FROM ciudad 
                    WHERE NOMBRE_CIUDAD = '{}'""".format(city.nombre)        
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                city = City(0,row[0],"")
                return city
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def addCompany(self, db, company):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO compania (ID_COMPANIA, NOMBRE_COMPANIA
                VALUES (null, %s)"""
            cursor.execute(sql,(company.nombre_compania))
            db.connection.commit()
               
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def addCity(self, db, city):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO ciudad (ID_CIUDAD, NOMBRE_CIUDAD)
                VALUES (null, %s)"""
            cursor.execute(sql,(city.nombre_ciudad))
            db.connection.commit() 
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def ListCompany(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM compania "
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ListCity(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT * FROM ciudad "
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def EditCity(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT NOMBRE_CIUDAD FROM ciudad WHERE ID_CIUDAD = %s", (id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def updaCity(self, db, id, city):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE ciudad SET NOMBRE_CIUDAD=%s WHERE ID_CIUDAD=%s"
            cursor.execute(sql,(city.nombre, id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def EditCompany(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT NOMBRE_COMPANIA FROM compania WHERE ID_COMPANIA=%s", (id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def updaCompany(self, db, id, company):
        try: 
            cursor = db.connection.cursor()
            sql = "UPDATE compania SET NOMBRE_COMPANIA=%s WHERE ID_COMPANIA=%s", (id)
            cursor.execute(sql,(company.nombre, id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ShowCompCity(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ciudad.NOMBRE_CIUDAD, compania.NOMBRE_COMPANIA from companiaciudad JOIN ciudad on ciudad.ID_CIUDAD=companiaciudad.ID_CIUDAD JOIN compania ON compania.ID_COMPANIA=companiaciudad.ID_COMPANIA"
            cursor.execute(sql)
            return cursor.fetchall() 
        except Exception as ex:
            raise Exception(ex)

        

