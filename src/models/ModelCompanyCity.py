from os import curdir
from colorama import Cursor
from .entities.CompanyCity import CompanyCity
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
                company = Company(0,row[0])
                return company
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def addCompany(self, db, company):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO compania (ID_COMPANIA, NOMBRE_COMPANIA
                VALUES (null, '{}')""".format(company.nombre)
            cursor.execute(sql)
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
    def EditCompany(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_COMPANIA, NOMBRE_COMPANIA FROM compania WHERE ID_COMPANIA={}".format(id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def updaCompany(self, db, company):
        try: 
            cursor = db.connection.cursor()
            sql = "UPDATE compania SET NOMBRE_COMPANIA=%s WHERE ID_COMPANIA=%s"
            cursor.execute(sql,(company.nombre, company.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def deleteCompany(seld, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM compania WHERE ID_COMPANIA = {}".format(id)
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

    @classmethod
    def ExistCity(self, db, city):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT NOMBRE_CIUDAD FROM ciudad 
                    WHERE NOMBRE_CIUDAD = '{}'""".format(city.nombre)        
            cursor.execute(sql)
            row = cursor.fetchone()
            if row != None:
                city = City(0,row[0])
                return city
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def addCity(self, db, city):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO ciudad (ID_CIUDAD, NOMBRE_CIUDAD)
                VALUES (null, '{}')""".format(city.nombre)
            cursor.execute(sql)
            db.connection.commit() 
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
            sql = "SELECT ID_CIUDAD, NOMBRE_CIUDAD FROM ciudad WHERE ID_CIUDAD={}".format(id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def updaCity(self, db, city):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE ciudad SET NOMBRE_CIUDAD=%s WHERE ID_CIUDAD=%s"
            cursor.execute(sql,(city.nombre, city.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def deleteCity(seld, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM ciudad WHERE ID_CIUDAD = {}".format(id)
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)
    
#-------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------

    @classmethod
    def ExistCompanyCity(self, db, companyCity):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT NOMBRE_COMPANIA, NOMBRE_CIUDAD FROM companiaciudad 
                JOIN compania ON compania.ID_COMPANIA=companiaciudad.ID_COMPANIA
                JOIN ciudad ON ciudad.ID_CIUDAD=companiaciudad.ID_CIUDAD
                WHERE  companiaciudad.ID_COMPANIA=%s  and companiaciudad.ID_CIUDAD=%s"""       
            cursor.execute(sql,(companyCity.id_company, companyCity.id_city))
            row = cursor.fetchone()
            if row != None:
                companyCity = CompanyCity(0,row[0],row[1])
                return companyCity
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def addCompanyCity(self, db, companyCity):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO companiaciudad (ID_COMCIU, ID_COMPANIA, ID_CIUDAD)
                VALUES (null, %s, %s)"""
            cursor.execute(sql,(companyCity.id_company, companyCity.id_city))
            db.connection.commit() 
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def ShowCompCity(self, db):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT companiaciudad.ID_COMCIU, ciudad.NOMBRE_CIUDAD, compania.NOMBRE_COMPANIA from companiaciudad JOIN ciudad on ciudad.ID_CIUDAD=companiaciudad.ID_CIUDAD JOIN compania ON compania.ID_COMPANIA=companiaciudad.ID_COMPANIA"
            cursor.execute(sql)
            return cursor.fetchall() 
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def EditCompanyCity(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT ID_COMCIU, ID_COMPANIA, ID_CIUDAD FROM companiaciudad WHERE ID_COMCIU={}".format(id)
            cursor.execute(sql)
            return cursor.fetchall()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def updaCompanyCity(self, db, companyCity):
        try:
            cursor = db.connection.cursor()
            sql = "UPDATE companiaciudad SET ID_COMPANIA=%s, ID_CIUDAD=%s WHERE ID_COMCIU=%s"
            cursor.execute(sql,(companyCity.id_company, companyCity.id_city, companyCity.id))
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def deleteCompanyCity(seld, db, id):
        try:
            cursor = db.connection.cursor()
            sql = "DELETE FROM companiaciudad WHERE ID_COMCIU = {}".format(id)
            cursor.execute(sql)
            db.connection.commit()
        except Exception as ex:
            raise Exception(ex)

