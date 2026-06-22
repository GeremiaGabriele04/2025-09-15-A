from database.DB_connect import DBConnect
from model.arco import Arco
from model.pilota import Pilota


class DAO():

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct year FROM seasons s  ORDER BY year"

        cursor.execute(query)

        for row in cursor:
            results.append(row["year"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(anno1, anno2):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct d.driverId,d.driverRef,d.number,d.code,d.forename,d.surname,d.dob,d.nationality,d.url
                    from races r , drivers d , results r2 
                    where r.raceId = r2.raceId and r2.driverId = d.driverId 
                    and r.`year` >= %s
                    and r.`year` <= %s
                    and r2.`position` is not null"""

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            results.append(Pilota(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(anno1, anno2):
        conn = DBConnect.get_connection()

        listaArchi = []
        listaIdPiloti = []

        cursor = conn.cursor(dictionary=True)
        query = """select r1.driverId as id1, r2.driverId as id2, count(*) as numero
                    from results r1 , results r2, races r 
                    where r1.constructorId = r2.constructorId and r1.raceId = r2.raceId  and r1.raceId = r.raceId
                    and r.`year` >= %s
                    and r.`year` <= %s
                    and r1.position is not null 
                    and r2.position is not null 
                    and r1.driverId != r2.driverId 
                    group by r1.driverId, r2.driverId"""

        cursor.execute(query, (anno1, anno2))

        for row in cursor:
            listaArchi.append((row["id1"], row["id2"], row["numero"]))
            listaIdPiloti.append((row["id1"], row["id2"]))

        cursor.close()
        conn.close()
        return listaArchi, listaIdPiloti