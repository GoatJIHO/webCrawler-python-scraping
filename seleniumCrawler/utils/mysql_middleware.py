import pymysql
import json

class Rnd_MySql:
    with open("./utils/ServerInfo/mysql.json", "r") as f:
        Mysql_access_info = json.load(f)

    conn = pymysql.connect(**Mysql_access_info["localhost"])

    with open("./scheme_table/scheme_table.json") as f:
        scheme_info = json.load(f)

    def __init__(self):
        pass


    def SQL_insert(self, table_name,json):
        field_names = "("
        string_count = "("
        keys_list = list(json.keys())
        insert_data = []

        for key in range(len(json)):
            try:
                if json[keys_list[key]] == json[keys_list[-1]]:
                    field_names += Rnd_MySql.scheme_info[table_name][keys_list[key]] + ")"
                    string_count += "%s)"
                else:
                    field_names += Rnd_MySql.scheme_info[table_name][keys_list[key]] + ", "
                    string_count += "%s, "

                insert_data.append(json[keys_list[key]])
            except:
                pass

        sql = f"INSERT INTO {table_name} {field_names} VALUES {string_count}"
        print(sql)
        try:
            with Rnd_MySql.conn.cursor() as cur:
                cur.execute(sql, insert_data)
                Rnd_MySql.conn.commit()
            return 1

        except pymysql.err.IntegrityError as e:
            print("Document Dup")
            return 0

        except Exception as e:
            print(e)
            pass
            return 0


