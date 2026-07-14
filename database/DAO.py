from database.DB_connect import DBConnect
from model.arco import Arco
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
        query = """ SELECT DISTINCT n.*
                    FROM names n, role_mapping rm, ratings r
                    WHERE rm.name_id = n.id 
                        AND n.date_of_birth is not null 
                      AND rm.movie_id = r.movie_id 
                      AND rm.category IN ('actor', 'actress')
                      AND r.avg_rating BETWEEN %s AND %s"""

        cursor.execute(query, (voto1,voto2))

        for row in cursor:
            results.append(Attore(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(voto1,voto2):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ SELECT rm1.name_id AS a1, rm2.name_id AS a2, 
                   SUM(CAST(REPLACE(REPLACE(m.worlwide_gross_income, '$ ', ''), ',', '') AS UNSIGNED)) AS peso
            FROM role_mapping rm1, role_mapping rm2, movie m, ratings r
            WHERE rm1.movie_id = rm2.movie_id
              AND rm1.movie_id = m.id
              AND m.id = r.movie_id
              AND r.avg_rating BETWEEN %s AND %s
              AND rm1.category IN ('actor', 'actress') 
              AND rm2.category IN ('actor', 'actress')
              AND rm1.name_id < rm2.name_id
              AND m.worlwide_gross_income IS NOT NULL
            GROUP BY rm1.name_id, rm2.name_id"""

        cursor.execute(query, (voto1, voto2))

        for row in cursor:
            results.append(Arco(**row))

        cursor.close()
        conn.close()
        return results


