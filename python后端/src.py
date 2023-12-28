import copy

from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import datetime
import json

app = Flask(__name__)
CORS(app)

'''
江西理工大学 钟悦明
'''

class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None
        self.nickname = None
        self.avatar_url = None
        self.address = None
        self.create_time = None
        self.role = None


class UserDTO:
    def __init__(self, user, menus):
        self.id = user["id"]
        self.username = user["username"]
        self.password = user["password"]
        self.nickname = user["nickname"]
        self.avatarUrl = user["avatarUrl"]
        self.role = user["role"]
        self.menus = menus


#
# # 打开数据库连接
# try:
#
#     print('连接成功！')
# except:
#     print('something wrong!')


@app.route('/')
def hello_world():
    return 'Hello World'


'''
UserController
'''


# 增&改
@app.route("/user", methods=['POST'])
def save():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor()
    user_data = request.json
    print("user_data!!!", user_data)

    for key, value in user_data.items():
        if isinstance(value, str) and 'GMT' in value:  # 判断是否是日期格式的字符串
            user_data[key] = datetime.datetime.strptime(value, '%a, %d %b %Y %H:%M:%S %Z').strftime(
                '%Y-%m-%d %H:%M:%S')  # 将日期字符串转换成MySQL支持的格式

    user_fields = user_data.keys()
    user_values = list(user_data.values())

    if "id" not in user_fields:
        sql = "INSERT INTO system_user ({}) VALUES ({})".format(
            ', '.join(user_fields),
            ', '.join(['%s'] * len(user_fields))
        )
        print("sql insert!!!")
    else:
        set_clause = ", ".join(["{} = %s".format(field) for field in user_fields])
        user_id = user_data["id"]
        user_values.append(user_id)
        sql = "UPDATE system_user SET {} WHERE id = %s".format(set_clause)
        print("sql update")

    try:
        cursor.execute(sql, user_values)
        db.commit()
        db.close()
        print('数据插入成功！')
        return jsonify({'code': '200'})
    except Exception as e:
        print(e)
        db.rollback()
        db.close()
        print('数据插入错误！')
        return jsonify({'code': '500'})


@app.route('/user/<int:id>', methods=['DELETE'])
def delete(id):
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor()
    sql = f"DELETE FROM system_user WHERE id = {id}"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        print('数据删除成功')
        return jsonify({'code': '200'})
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})


# 传入id数组批量删除,
@app.route('/user/del/batch', methods=['POST'])
def delete_batch():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    data = request.json
    print("data!!!", data)
    try:
        for value in data:
            sql = f"DELETE FROM system_user WHERE id = {value}"
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        db.close()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})
    return jsonify({'code': '200'})


@app.route('/user/page', methods=['GET'])
def user_page():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    pageNum = request.args.get('pageNum', 1, type=int)  # 默认值为1
    pageSize = request.args.get('pageSize', 10, type=int)  # 默认值为10
    username = request.args.get('username', '')
    address = request.args.get('address', '')

    # 构建模糊查询的 SQL 语句
    sql = "SELECT * FROM system_user WHERE 1=1"  # 初始SQL语句
    sql_params = []  # 初始化 SQL 参数列表

    if username:  # 如果有提供username参数
        sql += " AND username LIKE %s"
        sql_params.append('%' + username + '%')

    if address:  # 如果有提供address参数
        sql += " AND address LIKE %s"
        sql_params.append('%' + address + '%')

    with db.cursor() as cursor:
        cursor.execute(sql, tuple(sql_params))  # 使用参数化查询的方式
        column_names = [i[0] for i in cursor.description]  # 获取查询结果的字段名
        total_records = cursor.rowcount

        # 分页逻辑
        start = (pageNum - 1) * pageSize
        end = start + pageSize
        sql += " LIMIT %s, %s"
        sql_params.extend([start, pageSize])
        cursor.execute(sql, tuple(sql_params))

        records = []
        for row in cursor.fetchall():
            record = {}
            for i, value in enumerate(row):
                column_name = column_names[i]
                record[column_name] = value
            records.append(record)

        response_data = {
            'records': records,
            'total': total_records
        }
        db.close()
        return jsonify(response_data)


@app.route("/user/username/<username>", methods=['GET'])
def find_by_username(username):
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = f"select * from system_user where username = '{username}'"
    cursor.execute(sql)
    res = cursor.fetchone()
    db.close()
    print("username!!! res !!!")
    res.pop("create_time")
    print(res)
    return jsonify(res)


@app.route("/user/password", methods=['POST'])
def change_password():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    password_dto = request.json
    username = password_dto["username"]

    print("password_dto")
    print(password_dto)

    cursor.execute(f"select password from system_user where username = '{username}'")
    res = cursor.fetchone()
    print("change_password res!!!!")
    print(res)

    response_data = {
        'code': None,
        'msg': None
    }

    if res[0] == password_dto["password"]:
        new_password = password_dto["newPassword"]
        cursor.execute(f"update system_user set password = '{new_password}' where username = '{username}'")
        # 提交修改
        db.commit()
        response_data["code"] = "200"
    else:
        response_data["code"] = "501"
        response_data["msg"] = "原密码错误"
    db.close()
    return jsonify(response_data)


@app.route("/user", methods=['GET'])
def find_all_user():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    cursor.execute("select * from system_user")
    res = cursor.fetchall()
    db.close()
    return res


@app.route("/user/login", methods=['POST'])
def user_login():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor(pymysql.cursors.DictCursor)

    user_dto = request.json
    print("user_dto", user_dto)
    username = user_dto["username"]
    print("username")
    print(username)
    print("password")
    password = user_dto["password"]
    print(password)
    sql = "select * from system_user where username = '{}' and password = '{}'".format(username, password)

    cursor.execute(sql)
    res = cursor.fetchone()
    print("res")
    print(res)
    db.close()
    if res is not None:
        code = "200"
        user = res
        if res["role"] == "ROLE_ADMIN":
            menus = find_all_menus()
        else:
            menus = find_home_menu()
        userDTO = UserDTO(user, menus)
        print("before userdto_dict!!!!!")
        userDTO_dict = userDTO.__dict__
        print("userDTO_dict", userDTO_dict)
        # result = dict(zip(keys, res))
        # print("userDTO", userDTO)
        response_data = {
            'code': code,
            'data': userDTO_dict
        }
    else:
        response_data = {
            'code': "501",
            'data': None
        }
    return jsonify(response_data)


@app.route("/user/register", methods=['POST'])
def register():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    user_register = request.json
    username = user_register["username"]
    cursor.execute(f"select * from system_user where username = '{username}'")
    res = cursor.fetchone()

    if res is None:
        code = "200"
        password = user_register["password"]
        cursor.execute(f"insert into system_user (username, nickname, password, role) values ('{username}', '{username}', '{password}', 'ROLE_USER')")
        # 提交修改
        db.commit()
        code = "200"
        msg = "注册成功"
    else:
        code = "501"
        msg = "用户名已存在"
    response_data = {
        'code': code,
        'msg': msg
    }
    return jsonify(response_data)


'''
RoleController
'''


@app.route('/role', methods=['GET'])
def find_all_role():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    try:
        # 使用 cursor() 方法创建一个游标对象 cursor
        cursor = db.cursor()
        cursor.execute("select * from system_role")
        res = cursor.fetchall()
        keys = [x[0] for x in cursor.description]  # 获取查询结果的列名
        result = []
        for row in res:
            result.append(dict(zip(keys, row)))  # 将每一行转换为字典并添加到结果列表中
        print(result)
        db.close()
        return jsonify(result)
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})


'''
MenuController
'''


# @app.route('/menu', methods=['GET'])
def find_all_menus():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor(pymysql.cursors.DictCursor)
    home = "Home"
    cursor.execute(f"select * from system_menu")
    res = cursor.fetchall()
    # keys = [x[0] for x in cursor.description]  # 获取查询结果的列名
    # for row in res:
    #     result.append(dict(zip(keys, row)))  # 将每一行转换为字典并添加到结果列表中

    for i in res:
        i["children"] = []
    for parent in res:
        for child in res:
            if child["pid"] == parent["id"]:
                parent["children"].append(child)

    res_list = [item for item in res if item.get('pid') is None]
    print(res_list)
    print("all_menus")
    print(res_list)
    db.close()
    return res_list


def find_home_menu():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor(pymysql.cursors.DictCursor)
    home = "Home"
    dashbord = "Dashbord"
    m_map = "Map"
    cursor.execute(f"select * from system_menu where page_path = '{home}' or page_path = '{dashbord}' or page_path = '{m_map}'")
    res = cursor.fetchall()
    # keys = [x[0] for x in cursor.description]  # 获取查询结果的列名
    result = res  # 将keys和res合并为字典
    print(result)
    db.close()
    return result


'''
GoodController
'''


# 增&改
@app.route("/good", methods=['POST'])
def good_save():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor()
    user_data = request.json
    print("user_data!!!", user_data)

    user_fields = user_data.keys()
    user_values = list(user_data.values())

    if "id" not in user_fields:
        sql = "INSERT INTO system_goods ({}) VALUES ({})".format(
            ', '.join(user_fields),
            ', '.join(['%s'] * len(user_fields))
        )
        print("sql insert!!!")
    else:
        set_clause = ", ".join(["{} = %s".format(field) for field in user_fields])
        user_id = user_data["id"]
        user_values.append(user_id)
        sql = "UPDATE system_goods SET {} WHERE id = %s".format(set_clause)
        print("sql update")

    try:
        cursor.execute(sql, user_values)
        db.commit()
        db.close()
        print('数据插入成功！')
        return jsonify({'code': '200'})
    except Exception as e:
        print(e)
        db.rollback()
        db.close()
        print('数据插入错误！')
        return jsonify({'code': '500'})


@app.route('/good/<int:good_id>', methods=['DELETE'])
def good_delete(good_id):
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor()
    sql = f"DELETE FROM system_goods WHERE id = {good_id}"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        print('数据删除成功')
        return jsonify({'code': '200'})
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})


# 传入id数组批量删除,
@app.route('/good/del/batch', methods=['POST'])
def good_delete_batch():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    data = request.json
    print("data!!!", data)
    try:
        for value in data:
            sql = f"DELETE FROM system_goods WHERE id = {value}"
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        db.close()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})
    return jsonify({'code': '200'})


@app.route('/good/page', methods=['GET'])
def good_page():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    pageNum = request.args.get('pageNum', 1, type=int)  # 默认值为1
    pageSize = request.args.get('pageSize', 10, type=int)  # 默认值为10
    name = request.args.get('name', '')

    # 构建模糊查询的 SQL 语句
    sql = "SELECT * FROM system_goods WHERE 1=1"  # 初始SQL语句
    sql_params = []  # 初始化 SQL 参数列表

    if name:  # 如果有提供username参数
        sql += " AND name LIKE %s"
        sql_params.append('%' + name + '%')

    with db.cursor() as cursor:
        cursor.execute(sql, tuple(sql_params))  # 使用参数化查询的方式
        column_names = [i[0] for i in cursor.description]  # 获取查询结果的字段名
        total_records = cursor.rowcount

        # 分页逻辑
        start = (pageNum - 1) * pageSize
        end = start + pageSize
        sql += " LIMIT %s, %s"
        sql_params.extend([start, pageSize])
        cursor.execute(sql, tuple(sql_params))

        records = []
        for row in cursor.fetchall():
            record = {}
            for i, value in enumerate(row):
                column_name = column_names[i]
                record[column_name] = value
            records.append(record)

        response_data = {
            'records': records,
            'total': total_records
        }
        db.close()
        return jsonify(response_data)


'''
OrderController
'''

# 增&改
@app.route("/order", methods=['POST'])
def order_save():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor()
    user_data = request.json
    print("user_data!!!", user_data)
    if "time" in user_data.keys():
        user_data.pop("time")
    print("user_data!!!", user_data)

    user_fields = user_data.keys()
    user_values = list(user_data.values())

    if "id" not in user_fields:
        sql = "INSERT INTO system_sales ({}) VALUES ({})".format(
            ', '.join(user_fields),
            ', '.join(['%s'] * len(user_fields))
        )
        print("sql insert!!!")
    else:
        set_clause = ", ".join(["{} = %s".format(field) for field in user_fields])
        user_id = user_data["id"]
        user_values.append(user_id)
        sql = "UPDATE system_sales SET {} WHERE id = %s".format(set_clause)
        print("sql update")

    try:
        cursor.execute(sql, user_values)
        db.commit()
        db.close()
        print('数据插入成功！')
        return jsonify({'code': '200'})
    except Exception as e:
        print(e)
        db.rollback()
        db.close()
        print('数据插入错误！')
        return jsonify({'code': '500'})


@app.route('/order/<int:order_id>', methods=['DELETE'])
def order_delete(order_id):
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    cursor = db.cursor()
    sql = f"DELETE FROM system_sales WHERE id = {order_id}"
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 提交修改
        db.commit()
        db.close()
        print('数据删除成功')
        return jsonify({'code': '200'})
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})


# 传入id数组批量删除,
@app.route('/order/del/batch', methods=['POST'])
def order_delete_batch():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    data = request.json
    print("data!!!", data)
    try:
        for value in data:
            sql = f"DELETE FROM system_sales WHERE id = {value}"
            # 执行SQL语句
            cursor.execute(sql)
            # 提交修改
            db.commit()
        db.close()
    except Exception as e:
        print(e)
        # 发生错误时回滚
        db.rollback()
        db.close()
        return jsonify({'code': '500'})
    return jsonify({'code': '200'})


@app.route('/order/page', methods=['GET'])
def order_page():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    pageNum = request.args.get('pageNum', 1, type=int)  # 默认值为1
    pageSize = request.args.get('pageSize', 10, type=int)  # 默认值为10
    user_id = request.args.get('user_id', '')
    goods_id = request.args.get('goods_id', '')

    # 构建模糊查询的 SQL 语句
    sql = "SELECT * FROM system_sales WHERE 1=1"  # 初始SQL语句
    sql_params = []  # 初始化 SQL 参数列表

    if user_id:  # 如果有提供username参数
        sql += " AND user_id LIKE %s"
        sql_params.append('%' + user_id + '%')

    if goods_id:  # 如果有提供username参数
        sql += " AND goods_id LIKE %s"
        sql_params.append('%' + goods_id + '%')

    with db.cursor() as cursor:
        cursor.execute(sql, tuple(sql_params))  # 使用参数化查询的方式
        column_names = [i[0] for i in cursor.description]  # 获取查询结果的字段名
        total_records = cursor.rowcount

        # 分页逻辑
        start = (pageNum - 1) * pageSize
        end = start + pageSize
        sql += " LIMIT %s, %s"
        sql_params.extend([start, pageSize])
        cursor.execute(sql, tuple(sql_params))

        records = []
        for row in cursor.fetchall():
            record = {}
            for i, value in enumerate(row):
                column_name = column_names[i]
                record[column_name] = value
            records.append(record)

        response_data = {
            'records': records,
            'total': total_records
        }
        db.close()
        return jsonify(response_data)


@app.route('/order/good', methods=['GET'])
def order_good():
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='python_shop')
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor(pymysql.cursors.DictCursor)

    sql = f"select id, name from system_goods"
    cursor.execute(sql)
    res = cursor.fetchall()
    db.close()
    return jsonify(res)


'''
EchartsController
'''


@app.route("/echarts/members", methods=['GET'])
def echarts():
    return jsonify()


if __name__ == '__main__':
    app.run(port=9090)
