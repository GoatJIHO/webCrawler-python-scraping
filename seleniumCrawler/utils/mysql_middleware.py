from mysql.connector import Error
from mysql.connector import pooling
import logging

class MysqlConnectionPool:
    """
    Mysql Connection Pool 여러 인스턴스에서 공유해서 사용하기 위함
    """
    connection_pool = None

    with open("./utils/ServerInfo/mysql.json", "r") as f:
        mysql_access_info = json.load(f)

    with open("./scheme_table/scheme_table.json") as f:
        scheme_info = json.load(f)

    if connection_pool is None:
        connection_pool = pooling.MySQLConnectionPool(pool_name="mysql_middleware",
                                                      pool_size=5,
                                                      pool_reset_session=True,
                                                      host=mysql_access_info["host"],
                                                      user=mysql_access_info["user"],
                                                      password=mysql_access_info["password"],
                                                      database=mysql_access_info["db"],
                                                      charset="utf8mb4")

    def __init__(self):
        pass

    @classmethod
    def connection_pool_insert(cls, table_name, json):
        field_names = "("
        string_count = "("
        keys_list = list(json.keys())
        insert_data = []

        for key in range(len(json)):
            try:
                if json[keys_list[key]] == json[keys_list[-1]]:
                    field_names += cls.scheme_info[table_name][keys_list[key]] + ")"
                    string_count += "%s)"
                else:
                    field_names += cls.scheme_info[table_name][keys_list[key]] + ", "
                    string_count += "%s, "

                insert_data.append(json[keys_list[key]])
            except:
                pass

        sql = f"INSERT INTO {table_name} {field_names} VALUES {string_count}"

        connection_object = cls.connection_pool.get_connection()
        try:
            with connection_object.cursor() as cur:
                cur.execute(sql, insert_data)
                connection_object.commit()
            return 1

        except connection_object.Error as e:
            print("Error: ", e)  #logging 으로 바꿀 것
            return 0

        except Exception as e:
            print(e)    #logging 으로 바꿀 것
            return 0

        finally:
            connection_object.close()


