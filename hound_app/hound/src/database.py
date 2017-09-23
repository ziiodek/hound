import pymysql

class Database:

    def clear_profile(user_id, type):
        database = pymysql.connect('localhost', 'root', '', 'hound_db')
        cursor = database.cursor()
        try:
            cursor.execute("delete from hound_profile")
            database.commit()
        except:
            database.rollback()

        database.close()

    def clear_prints(user_id):
        database = pymysql.connect('localhost', 'root', '', 'hound_db')
        cursor = database.cursor()
        try:
            cursor.execute("delete from hound_prints")
            database.commit()
        except:
            database.rollback()

        database.close()
