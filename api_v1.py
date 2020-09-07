'''
1.superuser
2.没用数据库保存账户密码
3.没设置token，每次都要输入账户密码
'''
#!flask/bin/python
from flask import Flask,jsonify,request,abort,url_for,make_response
from flask_httpauth import HTTPBasicAuth
import xlrd
import json
# -*- coding:utf-8 -*-

app = Flask(__name__)
auth = HTTPBasicAuth()
app.config['JSON_AS_ASCII'] = False

@auth.get_password
def get_password(username):
    '''
    :param username:
    :return:
    '''
    if username == 'AaDd':
        return 'abcd1234'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def query_error(error):
    return make_response(jsonify({'code':'400','error': '输入有误'}),400)

@app.route('/api/query', methods=['POST'])
@auth.login_required
def check_data():
    if not request.json \
            and not 'qymc' in request.json \
            and not 'tyshxydm' in request.json \
            and not 'zzjgdm' in request.json \
            and not 'yyzzdm' in request.json:
        abort(400)
    temp = {
        'name':request.json.get('qymc',''),
        'xycode':request.json.get('tyshxydm',''),
        'jgcode':request.json.get('zzjgdm',''),
        'zzcode':request.json.get('yyzzdm',''),
    }
    for i in range(1,nor):
        result = {}
        for j in range(nol):
            title = table.cell_value(0,j)
            value = table.cell_value(i,j)
            result[title] = value
        if result['企业名称']== temp['name']\
                or result['统一社会信用代码']== temp['xycode']\
                or result['组织机构代码']== temp['jgcode']\
                or result['营业执照代码']== temp['zzcode']:
            return jsonify({'result':result}), 201
    return jsonify({'result': 'result not found'}), 400

if __name__ == '__main__':
    file_path = r'E:\pycharm\flast-restful-api\data\企业数据.xlsx'
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    nor = table.nrows
    nol = table.ncols

    app.run(host='0.0.0.0', port=9000,debug=True)