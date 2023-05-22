from flask import Flask
from flask import request
from flask import render_template
import udp_api

app = Flask(__name__, static_url_path='/static')

# wtf is this
microcontroller_ip = udp_api.find_stm32()

@app.route('/')
def hello():
    return render_template('despacito.html', name=None)

@app.route('/', methods = ['POST'])
def getUserInput():

    payload: int = 0;

    write = int(request.form['write'])
    channel = int(request.form['channel'])
    register_index = int(request.form['register number'])
    flag = int(request.form['flag'])
    data = int(request.form['data'])

    reserved_bit = 1

    payload |= (write << 31 | channel << 23 | register_index << 18 | flag << 17 | reserved_bit << 16 | data)
    udp_api.send_udp(microcontroller_ip, payload=payload)

    return {
        "write" : write,
        "channel" : channel,
        "register_index": register_index,
        "flag" : flag,
        "data" : data,
        "payload": payload
    }

@app.route('/about')
def test_connection_status():
    return {
        "microcontroller_ip" : microcontroller_ip,
        "local_ip" : udp_api.get_local_ip()
    }



