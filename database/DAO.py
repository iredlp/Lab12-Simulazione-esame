from database.DB_connect import DBConnect
from model.attore import Attore


class DAO():
    @staticmethod
    def getAllRange():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct avg_rating 
                    from ratings r 
                    order by r.avg_rating """

        cursor.execute(query)

        for row in cursor:
            results.append(row["avg_rating"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(voto1,voto2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select  distinct n.*
                    from names n ,ratings r , movie m , role_mapping rm 
                    where rm.name_id =n.id  and m.id =rm.movie_id  
                    and m.id =r.movie_id  and r.avg_rating  between %s and %s """

        cursor.execute(query, (voto1,voto2))

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

