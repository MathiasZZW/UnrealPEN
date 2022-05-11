from flask import Flask
from flask import request


app = Flask(__name__)
data_all = ""

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/login',methods=["GET"])
def login():
    global data_all
    # 以GET方式传参数，通过args取值
    data = request.args['data']
    # a = eval(data)
    # data_all += str(hex(a))+" "
    # print(data_all)
    for i in data.split("_")[:-1]:
        a= eval(i)
        print(str(hex(a))[2:]," ",end='')
    print("")
    return "OK"


if __name__ == '__main__':
    app.run()
