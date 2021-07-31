from flask import Flask, render_template, request
import sqlite3
import sqlalchemy


app = Flask(__name__)

def transmit_song(arg):
    if arg is None:
        return '404'
    else:
        name = arg[0]
        composer = arg[1]
        milliseconds = arg[2]
        lengths=[milliseconds//60000, milliseconds//1000%60]
        words=[]
        if lengths[0]==1:
            words.append('minute')
        else:
            words.append('minutes')
        if lengths[1]==1:
            words.append('second')
        else:
            words.append('seconds')
        length=f'{lengths[0]} {words[0]} {lengths[1]} {words[1]}'
        unitprice = arg[3]
        return [name, composer, length,unitprice]

def transmit_artist(arg):
    if arg == []:
        return '404'
    else:
        return arg

@app.route('/song', methods = ['POST', 'GET'])
def finder():
    data = ""
    name = ""
    if request.method == 'POST':
        name = request.form.get('name')
        data = transmit_song(sql_song_parse(name))
        print(data)
    return render_template('finder.html', res = data)

@app.route('/artist', methods = ['POST', 'GET'])
def artist():
    data = ""
    name = ""
    if request.method == 'POST':
        name = request.form.get('name')
        data = transmit_artist(sql_artist_parse(name))
        print(data)
    return render_template('artist.html', res = data)

@app.route('/', methods = ['POST', 'GET'])
def menu():

    return render_template('menu.html')


def sql_song_parse(str):
    result = ""
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    query = """
        SELECT Name, Composer, Milliseconds, UnitPrice 
        FROM 'tracks' 
        WHERE LOWER(Name) = ?
    """
    res = c.execute(query, (str.lower(),))

    return res.fetchone()

def sql_artist_parse(str):
    result = ""
    conn = sqlite3.connect('chinook.db')
    c = conn.cursor()
    query = """
        SELECT Name, UnitPrice 
        FROM 'tracks' 
        WHERE LOWER(Composer) = ?
    """
    res = c.execute(query, (str.lower(),))
    return res.fetchall()

if __name__ == "__main__":
    app.run(debug = True)
