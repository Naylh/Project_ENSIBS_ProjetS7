#-----------------------------------#
#                                   #
#              Import               #
#                                   #
# ----------------------------------#   


import os
import sys
import json
import mysql.connector
import html
from typing import Optional
from cas import CASClient
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import urllib.parse
#import modules from the folder "parser"
sys.path.insert(0, 'parser')
from parserProjet import mainParser
from makeExcel import mainExcel

#from parser.routine import *

from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title=__name__,docs_url=None,redoc_url=None)

#os.system('python3 parser/routine.py')

#-----------------------------------#
#                                   #
#            Client CAS             #
#                                   #
# ----------------------------------#


cas_client = CASClient(
    version=3,
    service_url='http://127.0.0.1:8002/login?next=%2Fplanning',
    server_url='https://localhost:8444/cas/login',
    verify_ssl_certificate=False
)


app.add_middleware(SessionMiddleware, secret_key="NotSoSecretKey")
app.mount("/www", StaticFiles(directory="www"), name="www")
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/images", StaticFiles(directory="images"), name="images")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/addons", StaticFiles(directory="addons"), name="addons")


@app.get('/')
def index(request: Request):
    user = request.session.get("user")
    if user:
        cursor.execute('SELECT * FROM utilisateur WHERE prenom_user=%s' , (user["user"].split(".")[1],))
        fetch = cursor.fetchall()
        if len(fetch)==0:
            adduser(user["user"])
            return RedirectResponse(request.url_for('planning'))
        return RedirectResponse(request.url_for('planning'))
    return FileResponse('www/index.html')
   

@app.get('/planning')
def planning(request: Request):
    user = request.session.get("user")
    if user:
        cursor.execute('SELECT * FROM utilisateur WHERE prenom_user=%s' ,(user["user"].split(".")[1],))
        fetch = cursor.fetchall()
        if len(fetch)==0:
            adduser(user["user"])
            return FileResponse('www/planning.html')
        return FileResponse('www/planning.html')
    return RedirectResponse(request.url_for('login'))


@app.get('/administration')
def planning(request: Request):
    user = request.session.get("user")

    if user:
        cursor.execute('SELECT * FROM utilisateur WHERE prenom_user=%s' ,(user["user"].split(".")[1],))
        fetch = cursor.fetchall()
        print("FETCH === ",fetch)
        columns = cursor.column_names
        data = conv_json(fetch, columns)[0]
        if data['role']=='administrateur':
            return FileResponse('www/administration.html')
        else:
            return RedirectResponse(request.url_for('planning'))
    return RedirectResponse(request.url_for('login'))


@app.get('/mail')
def planning(request: Request):
    user = request.session.get("user")

    if user:
        cursor.execute('SELECT * FROM utilisateur WHERE prenom_user=%s' ,(user["user"].split(".")[1],) )
        fetch = cursor.fetchall()
        columns = cursor.column_names
        data = conv_json(fetch, columns)[0]
        if (data['role']=='administrateur' or data['role']=='superviseur'):
            return FileResponse('www/mail.html')
        return RedirectResponse(request.url_for('planning'))
    return RedirectResponse(request.url_for('login'))


@app.get('/login')
def login(
    request: Request, next: Optional[str] = None,
    ticket: Optional[str] = None):
    if request.session.get("user", None):
        # Already logged in
        return RedirectResponse(request.url_for('planning'))

    # next = request.args.get('next')
    # ticket = request.args.get('ticket')
    if not ticket:
        # No ticket, the request come from end user, send to CAS login
        cas_login_url = cas_client.get_login_url()
        print('CAS login URL: %s', cas_login_url)
        return RedirectResponse(cas_login_url)

    # There is a ticket, the request come from CAS as callback.
    # need call `verify_ticket()` to validate ticket and get user profile.
    print('ticket: %s', ticket)
    print('next: %s', next)

    user, attributes, pgtiou = cas_client.verify_ticket(ticket)

    print(
        'CAS verify ticket response: user: %s, attributes: %s, pgtiou: %s',
        user, attributes, pgtiou)

    if not user:
        return HTMLResponse('Failed to verify ticket. <a href="/login">Login</a>')
    else:  # Login successfully, redirect according `next` query parameter.
        response = RedirectResponse(next)
        request.session['user'] = dict(user=user)
        return response


@app.get('/log')
def logout(request: Request):
    # Clear session
    request.session.pop('user', None)
    redirect_url = request.url_for('logout_callback')
    cas_logout_url = cas_client.get_logout_url(redirect_url)
    print('CAS logout URL: %s', cas_logout_url)
    return RedirectResponse(cas_logout_url)


@app.get('/logout_callback')
def logout_callback(request: Request):
    # redirect from CAS logout request after CAS logout successfully
    # response.delete_cookie('username')
    request.session.pop("user", None)
    return HTMLResponse('Logged out from CAS. <a href="/login">Login</a>')


@app.get("/{full_path:path}")
async def catch_all(request: Request, full_path: str):
    #redirect all unknown requests to login
    return RedirectResponse(request.url_for('planning'))


#-----------------------------------#
#                                   #
#           BDD BackEnd             #
#                                   #
# ----------------------------------#


mydb = mysql.connector.connect(
    host = "localhost",
    user = "root", #os.getenv('UserMySQL'),
    password = "", #os.getenv('PasswordMySQL'),
    database = "bdplanning", #os.getenv('DatabaseName'),
    auth_plugin='mysql_native_password'
)


cursor = mydb.cursor()


def conv_json(fetch,columns):
    list_json = []
    for i in fetch:
        vals_ligne = {}
        for j in range(len(columns)):
            vals_ligne[str(columns[j])]=i[j]
        list_json.append(vals_ligne)
    return(list_json)


def conv_req(req):
    reqd = req.decode("utf-8")
    attributs_ncv = reqd.split("&")
    attributs_dict = {}
    for i in range(len(attributs_ncv)):
        attributs_dict[attributs_ncv[i].split("=")[0]] = attributs_ncv[i].split("=")[1]
    return attributs_dict

def checkadmin(user):
    user_numetud = user.split(".")[2]
    cursor.execute('SELECT role FROM utilisateur WHERE n_etudiant = %s' ,(user_numetud,))
    res = cursor.fetchall()
    if res[0][0] == "administrateur":
        print("ADMIN OKKK ")
        return True
    return False

def adduser(login_user):
    #type login : jones.matt.e0000000
    #champs exemple : "jones","matt","lecteur","jones.e0000000@etud.univ-ubs.fr","e0000000","oui"
    if ("'" in login_user or '"' in login_user or ";" in login_user):
        return False
    vals_login = login_user.split('.')
    nom_user = vals_login[0]
    prenom_user = vals_login[1]
    mail = vals_login[0]+"."+vals_login[2]+"@etud.univ-ubs.fr"
    numetud = vals_login[2]
    cursor.execute('INSERT INTO utilisateur (nom_user,prenom_user,role,mail,n_etudiant,Acontacter) VALUES (%s,%s,"lecteur",%s,%s,"non")',(nom_user,prenom_user,mail,numetud))
    mydb.commit()
    return True

def verif_injection_sql(chaine):
    vals = ["'",'"',";","#","--","/*","*/","%22","%27","%23","%3b","%2d%2d","%2f%2a","%2a%2f"]
    for valeur in vals:
        if valeur in chaine:
            return True
    return False



@app.post('/getRoomsGroups')
async def getRoomsGroups(request:Request):
    cursor.execute('SELECT * FROM groupe_salle')
    fetch = cursor.fetchall()
    columns = cursor.column_names
    return conv_json(fetch,columns)


@app.post('/getRooms')
async def getRooms(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    if verif_injection_sql(body["option"]):
        return ("Error SQL")
    if(body["option"] == "1"):
        cursor.execute('SELECT * FROM salle JOIN relation_groupe_salle ON salle.id_salle = relation_groupe_salle.id_salle WHERE id_groupe_salle=%s' ,(body["id_groupe_salle"],))
        fetch = cursor.fetchall()
        columns = cursor.column_names
        return conv_json(fetch,columns)
    elif(body["option"] == "2"):
        cursor.execute('SELECT * FROM salle EXCEPT SELECT * FROM salle WHERE id_salle IN (SELECT relation_groupe_salle.id_salle FROM relation_groupe_salle WHERE id_groupe_salle=%s)' ,(body["id_groupe_salle"],))
        fetch = cursor.fetchall()
        columns = cursor.column_names
        return conv_json(fetch,columns)
    return False


@app.post('/getRoomsSchedule')
async def getRoomsSchedule(request:Request):
    with open('json/JSON_name.json', 'r') as f:
        data = json.load(f)
    return data


@app.post('/createJSON')
async def createJSON(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    data = urllib.parse.unquote_plus(body["data"])
    json_obj = json.loads(data)
    with open(urllib.parse.unquote_plus(body["title"]), 'w', encoding='utf-8') as json_file:
        json.dump(json_obj, json_file)
    array = [urllib.parse.unquote(body["dayStart"]),urllib.parse.unquote(body["dayEnd"])]
    return array


@app.post('/makeExcel')
async def makeExcel(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    mainExcel(body["dayStart"],body["dayEnd"],body["maximumTreshold"],body["mediumTreshold"],body["numberRooms"])
    return True


@app.post('/createGroup')
async def createGroup(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    if verif_injection_sql(body["name"]):
        return ("Error SQL")
    cursor.execute("INSERT INTO groupe_salle (nom_groupe) VALUES (%s)" ,(body["name"],))
    mydb.commit()
    return True


@app.post('/getUsers')
async def getUsers(request:Request):
    cursor.execute('SELECT * FROM utilisateur')
    fetch = cursor.fetchall()
    columns = cursor.column_names
    return conv_json(fetch,columns)


@app.post('/deleteGroup')
async def deleteGroup(request:Request):
    user = request.session.get("user")["user"]
    b_req=await request.body()
    body = conv_req(b_req)
    if user:

        if not checkadmin(user):
            print("Not admin")
            return False
        if- verif_injection_sql(body["id_groupe"]):
            print("Error SQL")
            return False

        cursor.execute('DELETE FROM relation_groupe_salle WHERE id_groupe_salle = %s' ,(body["id_groupe"],))
        cursor.execute('DELETE FROM groupe_salle WHERE id_groupe = %s' ,(body["id_groupe"],))
        mydb.commit()
        return True
    return False


@app.post('/addRoomToGroup')
async def addRoomToGroup(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    if verif_injection_sql(body["group"]) or verif_injection_sql(body["room"]):
        return ("Error SQL") 
    cursor.execute('INSERT INTO relation_groupe_salle VALUES (%s,%s)' ,(body["group"],body["room"],))
    mydb.commit()
    return True


@app.post('/getWhoContact')
async def getWhoContact(request:Request):
    cursor.execute('SELECT * FROM utilisateur WHERE Acontacter = "oui"')
    fetch = cursor.fetchall()
    columns = cursor.column_names
    return conv_json(fetch,columns)


@app.post('/getAdmin')
async def getAdmin(request:Request):
    cursor.execute('SELECT * FROM utilisateur WHERE role = "administrateur"')
    fetch = cursor.fetchall()
    columns = cursor.column_names
    return conv_json(fetch,columns)


@app.post('/setWhoContact')
async def setWhoContact(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    if verif_injection_sql(body["id"]):
        return("Error SQL")
    cursor.execute('UPDATE utilisateur SET Acontacter = "oui" WHERE id_user = %s' ,(body["id"],))
    mydb.commit()
    return True


@app.post('/forceParse')
async def forceParse(request:Request):
    #b_req=await request.body()
    #body = conv_req(b_req)
    mainParser("-r","-o")
    return True


@app.post('/updateRole')
async def updateRole(request:Request):
    user = request.session.get("user")
    b_req=await request.body()
    body = conv_req(b_req)

    if user : 
        if not checkadmin(user["user"]):
            print("Not admin")
            return False
        if verif_injection_sql(body["role"]) or verif_injection_sql(body["mail"]):
            print("Error SQL")
            return False
    
    #cursor.execute('UPDATE utilisateur SET role = "%s" WHERE mail = "%s"' %(body["role"],urllib.parse.unquote_plus(body["mail"])))

        cursor.execute('UPDATE utilisateur SET role = %s WHERE mail = %s' ,(body["role"],urllib.parse.unquote_plus(body["mail"]),))
        mydb.commit()
        return True
    return False

@app.post('/insertTaux')
async def insertTaux(request:Request):
    b_req=await request.body()
    body = conv_req(b_req)
    #print(body["tauxAlerte"])
    #print(urllib.parse.unquote_plus(body["nom"]))
    #cursor.execute('UPDATE salle SET tauxAlerte = "%s" WHERE nom = "%s"' %(body["tauxAlerte"],urllib.parse.unquote_plus(body["nom"])))
    cursor.execute('UPDATE salle SET tauxAlerte = %s WHERE nom = %s' ,(body["tauxAlerte"],urllib.parse.unquote_plus(body["nom"]),))
    mydb.commit()
    return True

@app.post('/session')
def session(request:Request):
    user = request.session.get("user")
    if user:
        cursor.execute('SELECT * FROM utilisateur WHERE prenom_user=\"'+user["user"].split(".")[1]+'\"') #WHERE n_etudiant="%s"' %user["user"] )
        fetch = cursor.fetchall()
        if len(fetch) == 0:
            return True
        columns = cursor.column_names
        data = conv_json(fetch, columns)[0]
        return data
    return False


#-----------------------------------#
#                                   #
#        Running the Server         #
#                                   #
# ----------------------------------#

if __name__ == '__main__':
    import uvicorn
    # run uvicorn with ssl
    uvicorn.run(app, host="0.0.0.0", port=8002)
