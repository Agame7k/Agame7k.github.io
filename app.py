from flask import Flask, send_file, request, session
import os, random, configparser

config = configparser.ConfigParser()
config.read(r'config.txt')

app = Flask(__name__)
app.secret_key = config.get("DEFAULT", "secret")
host = config.get("DEFAULT", "host")
buzzy_noises = ["buzz!", "bzzz", "bzzzzzz", "zzzz", "brrrr", "vrrrr", "whirr", "hummm"]
@app.route('/', methods=["GET"])
def home():
    noise = random.choice(buzzy_noises)
    html_content = f"""
    <html>
    <head>
        <title>{noise} - sillybuzzy.me</title>
        <meta property="og:title" content="{noise} - sillybuzzy.me" />
        <meta property="og:type" content="image.webp" />
        <meta property="og:url" content="http://sillybuzzy.me" />
        <meta property="og:image" content="http://sillybuzzy.me/api/buzz" />
    </head>
    <body style="background-color: #131516; color: #FFFFFF">
        <center><br><h3>{noise}</h3><br><img width="300px" src="{host}/api/buzz" alt="silly buzzy image"><br><br><a href="http://github.com/sstock2005/sillycats.me" target="_blank" style="font-weight: bold;text-decoration: none;color: #FFFFFF;">Source Code</a>  |  <a href="http://github.com/sstock2005" target="_blank" style="font-weight: bold;text-decoration: none;color: #FFFFFF;">My GitHub</a><br><br></center>
    </body>
    </html>
    """

    return html_content, 200, {'Content-Type': 'text/html'}

@app.route('/api/buzz')
def cat():
    if 'last_buzz' not in session:
        session['last_buzz'] = None
    picture = random.choice(os.listdir("./pictures"))
    while picture == session['last_buzz']:
        picture = random.choice(os.listdir("./pictures"))
    session['last_buzz'] = picture
    return send_file("pictures/{}".format(picture), "image/png", False)

@app.route('/api/noise')
def noise():
    return random.choice(buzzy_noises), 200, {'Content-Type': 'text/plain'}
app.run('0.0.0.0', 80, False, threaded=True)