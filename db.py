import mysql.connector
from mysql.connector import pooling
import jwt
import logging

logger = logging.getLogger('db')

# 数据库管理类
class DatabaseManager:
    def __init__(self):
        # self.pool = pooling.MySQLConnectionPool(
        #     pool_name="my_pool",
        #     pool_size=5,
        #     user="xagc",
        #     password="123456",
        #     database="xSales_test",
        #     connect_timeout=5,
        #     ssl_disabled=True  # SSL/TLS连接,云端False
        # )

        self.pool = pooling.MySQLConnectionPool(
            pool_name="my_pool",
            pool_size=5,
            user="xagc",
            password="123456",
            host='172.31.42.24',
            database="xSales_test",
            connect_timeout=5,
        )

    def get_connection(self):
        return self.pool.get_connection()


db_manager = DatabaseManager()


# 用户类
class User:
    def __init__(self, phone, pwd, id=None):
        self.id = id
        self.phone = phone
        self.pwd = pwd


def create_user(self):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM user WHERE phone = %s", (self.phone,))
        if cursor.fetchone():
            return "用户已存在"
        cursor.execute(
            "INSERT INTO user (phone, pwd) VALUES (%s, %s)", (self.phone, self.pwd)
        )
        cnx.commit()
        user_id = cursor.lastrowid
        logger.info("用户 %s 创建成功", self.phone)
        return User(self.phone, self.pwd, user_id)
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


# Bot 类
class Bot:
    def __init__(
        self,
        uid,
        shopper_id,
        shopper_name,
        live_name,
        live_url,
        live_doc,
        id=None,
        life_id = None,
        status=0,
        live_status=0,
    ):
        self.id = id or None
        self.uid = uid
        self.shopper_id = shopper_id
        self.shopper_name = shopper_name
        self.live_name = live_name
        self.live_url = live_url
        self.live_doc = live_doc
        self.life_id = life_id
        # 0: 未开启 1: 开启中 2: 开启中待打开直播 3：开启成功
        self.status = status
        self.live_status = live_status
        self.driver = None

    def get_id(self):
        return self.id

    def get_uid(self):
        return self.uid

    def get_live_name(self):
        return self.live_name

    def get_shopper_id(self):
        return self.shopper_id
    
    def get_shopper_name(self):
        return self.shopper_name

    def get_live_url(self):
        return self.live_url

    def get_live_doc(self):
        return self.live_doc

    def get_status(self):
        return self.status

    def get_live_state(self):
        return self.live_state

    def get_live_qrcode_path(self):
        live_name_id = self.get_live_name() + "-" + self.get_shopper_id()
        qr_path = "./data/" + live_name_id + "/qrcode/qr_code.png"
        return qr_path

    def get_live_doc_path(self):
        live_name_id = self.get_live_name() + "-" + self.get_shopper_id()
        path_text = "data/" + live_name_id + "/text"
        path_vector = "storage/" + live_name_id
        return [path_text, path_vector]
    
    def get_driver(self):
        return self.driver

def create_bot(self):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "INSERT INTO bot (uid, shopper_id, shopper_name, life_id, live_name, live_url, live_doc, status, live_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (self.uid, self.shopper_id, self.shopper_name, self.life_id, self.live_name, self.live_url, self.live_doc, self.status, self.live_status),
        )
        cnx.commit()
        bot_id = cursor.lastrowid
        return Bot(self.uid, self.shopper_id, self.shopper_name, self.live_name, self.live_url, self.live_doc, bot_id, self.life_id, self.status, self.live_status)
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.close()
        if cnx:
            cnx.close()


# 用户操作函数
def select_user_by_id(user_id):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if row:
            return User(row[1], row[2], row[0])
        return None
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def update_user(user):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "UPDATE user SET pwd = %s WHERE phone = %s", (user.pwd, user.phone)
        )
        cnx.commit()
        logger.info("用户 %s 更新成功", user.phone)
        return User(user.phone, user.pwd, user.id)
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def delete_user(user_id):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM user WHERE id = %s", (user_id,))
        cnx.commit()
        logger.info("用户id: %s 删除成功", user_id)
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()

def select_user(phone, pwd):
    cursor = None
    cnx = None
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM user WHERE phone = %s and pwd = %s", (phone, pwd))
        row = cursor.fetchone()
        if row is None:
            return ['未查到用户'+ str(phone), None]
        else:
            user_info = {"id": row[0],"phone": phone, "pwd": pwd}
            token = jwt.encode(user_info, "secret", algorithm="HS256")
            return [token, User(row[1], row[2], row[0])]
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


# Bot 操作函数
def select_botlists_by_id(token):
    try:
        uid = token2uid(token)
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM bot WHERE uid = %s", (uid,))
        rows = cursor.fetchall()
            # (self.uid, self.shopper_id, self.shopper_name, self.life_id, self.live_name, self.live_url, self.live_doc, self.status, self.live_status),
        logger.info("bot信息: %s", rows)
        res = [
            Bot(row[1], row[2],row[3], row[5], row[6], row[7], row[0], row[4],row[8],row[9]) for row in rows
        ]

        return res
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
        return []  # 返回空列表表示出错
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def select_bot_by_id(bot_id):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT * FROM bot WHERE id = %s", (bot_id,))
        row = cursor.fetchone()
        if row:
            return Bot(row[1], row[2],row[3], row[5], row[6], row[7], row[0], row[4],row[8],row[9])
        return None
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def update_bot(bot):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "UPDATE bot SET live_name = %s, shopper_id = %s, shopper_name = %s, live_url = %s, live_doc = %s, status = %s WHERE id = %s",
            (
                bot.live_name,
                bot.shopper_id,
                bot.shopper_name,
                bot.live_url,
                bot.live_doc,
                bot.status,
                bot.id,
            ),
        )
        cnx.commit()
        logger.info("bot %s 更新成功", bot.id)
        return bot
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def delete_bot(bot_id):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM bot WHERE id = %s", (bot_id,))
        cnx.commit()
        logger.info("bot %s 删除成功", bot_id)
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def update_bot_status(bot_id, status):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("UPDATE bot SET status = %s WHERE id = %s", (status, bot_id))
        cnx.commit()
        logger.debug("bot %s status更新为: %s", bot_id, status)
        return "bot status更新成功"
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
        return "数据库错误"
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()


def get_bot_status(bot_id):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT status FROM bot WHERE id = %s", (bot_id,))
        row = cursor.fetchone()
        return row[0] if row else 0
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
        return 0
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()



def get_live_status(shopper_id):
    status = 0
    cnx = None
    cursor = None

    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT live_status FROM bot WHERE shopper_id = %s", (shopper_id,))
        row = cursor.fetchone()
        status = row[0] if row and row[0] is not None else 0
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()
        return status



def set_live_status(shopper_id, status):
    try:
        cnx = db_manager.get_connection()
        cursor = cnx.cursor()
        cursor.execute(
            "UPDATE bot SET live_status = %s WHERE shopper_id = %s", (status, shopper_id)
        )
        cnx.commit()
        logger.debug("直播状态更新 %s 成功", status)
    except mysql.connector.Error as err:
        logger.error("数据库错误: %s", err)
    finally:
        if cursor:
            cursor.fetchall()
            cursor.close()
        if cnx:
            cnx.close()

def token2uid(token):
    user_info = jwt.decode(token, "secret", algorithms=["HS256"])
    return user_info["id"]

def token_decode(token):
    auth_dic = {}

    try:
      user_info = jwt.decode(token, "secret", algorithms=["HS256"])
      auth_dic['phone'] = user_info['phone']
      auth_dic['pwd'] = user_info['pwd']
      auth_dic['id'] = user_info['id']
      token_user_info = select_user(user_info['phone'], user_info['pwd'])
      auth_dic['db_token_check'] = token_user_info[0]
    except Exception as e:
      logger.error("token解析错误: %s", e)
      auth_dic['db_token_check'] = None
    return auth_dic
    


# 主函数
if __name__ == "__main__":
    # 示例用法
    # 创建用户
    new_user = User.create_user("16619906311", "123456")
    # print(new_user)

    # 创建 bot
    new_bot = Bot.create_bot(1, "code123", "live123", "http://example.com", "doc123")
    # print(new_bot)
