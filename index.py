from flask import Flask, render_template, jsonify, session, request
from script import run#first_wave_part, load_vk, load_group_id, load_users
from history import get_history, add_history
from keys import get_keys, add_key

app = Flask(__name__)
app.debug = True
app.secret_key = 'asd'

@app.route("/")
def index():  
    values = request.args
    agent = str(request.user_agent)
    if 'group' not in values or 'step' not in values:
        #add_history(u'Start Page// ' + agent)
        return render_template('index.html')
    if (not 'key' in values) or (values['key'] == ''):
        if 'lone' in str(values['group']) or 'givenchystyle' in str(values['group']):
            key = '1985'
        else:
            return jsonify({'error': 'The personal key isn\'t given'})
    else:
        key = str(values['key'])
    if not key in get_keys():
        return jsonify({'error': 'The key doesn\'t exist'})
    step = int(values['step'])
    screen_name = str(values['group'])
    if 'full' in values and int(values['full']) == 1:
        full = True
    else:
        full = False
    if 'extra' in values and int(values['extra']) == 1:
        extra = True
    else:
        extra = False
    add_history(u'Request. step:{}, screen_name:{}, full:{}, key:{}, extra:{} // '.format(*[str(n) for n in [step, screen_name, full, key, extra]]))
    #try:
    instas = run(step, screen_name, full=full, extra_data=extra)
    #except KeyError:
    #    return jsonify({'error': 'Invalid datas'})
    if instas == 'Out of range':
        return jsonify({'error': 'Out of range'})
    dic = {'count': len(instas), 'items': instas}
    return jsonify(dic)


@app.route("/add_key")
def akey():
    if not ('password' in request.args and request.args['password'] == 'airjordan'):
        return u'Incorrect password'
    key = add_key()
    return jsonify({'new_key': key})

@app.route("/admin")
def admin():
    if 'password' in request.args and request.args['password'] == 'airjordan':
        return str(get_keys())
    else:
        return u'Incorrect key'

@app.route("/h")
def history():
    h = get_history()
    return jsonify({'count': len(h), 'history': h})

@app.route("/next_step")
def next_step():
    session['step'] = session.get('step', -1) + 1
    instas = first_wave_part(load_vk(), 0, 'python_programing')
    return jsonify({'count': len(instas), 'instas': instas})

if __name__=="__main__":
    app.run('127.0.0.1', 80)
