from mysql.connector import Error
from mysql.connector import pooling
import json
from .selenium_logger.selenium_logger import CrawlerLogger

class MysqlConnectionPool:
    """
    Mysql Connection Pool 여러 인스턴스에서 공유해서 사용하기 위함
    1. 데이터를 삽입하는 함수
    2. 로그를 삽입하는 함수
    """
    connection_pool = None

    with open("../utils/ServerInfo/mysql.json", "r") as f:
        mysql_access_info = json.load(f)
        mysql_access_info = mysql_access_info["DataKnlab"]

    with open("../data/RnDKeyValue.json") as f:
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
        self.logger = CrawlerLogger("Master")
        self.logger.file_log()

    @classmethod
    def connection_pool_data_insert(cls, table_name, json):
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
            finally:
                pass

        sql = f"INSERT INTO {table_name} {field_names} VALUES {string_count}"

        connection_object = cls.connection_pool.get_connection()
        try:
            with connection_object.cursor() as cur:
                cur.execute(sql, insert_data)
            connection_object.commit()
            return 1

        except Error as e:
            print("Error: ", e)  # logging 으로 바꿀 것
            return 0

        except Exception as e:
            print(e)  # logging 으로 바꿀 것
            return 0

        finally:
            connection_object.close()

    def connection_pool_log_insert(cls, site_name, document_count):
        """
        작업 로그 디비 insert
        마스터에서 한 번만 실행
        사이트 , 수, 시간
        """
        crawling_time = datetime.datetime.now()
        sql = f"INSERT INTO cralwer_logs (site_name,document_count,crawling_time) VALUES (%s, %s, %s)"



        connection_object = cls.connection_pool.get_connection()
        try:
            with connection_object.cursor() as cur:
                cur.execute(sql, (site_name, document_count, crawling_time))
            connection_object.commit()
            return 1

        except Error as e:
            self.logger.error(e)

        finally:
            pass



