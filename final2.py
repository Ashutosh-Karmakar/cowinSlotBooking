import requests
import schedule as sc
import time
from datetime import date
from datetime import datetime
import pytz
import smtplib as sm

header = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}

    
def sendMail(d,l,dis):
    port = 587
    server = sm.SMTP('smtp.gmail.com',port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('tukusahoo1999@gmail.com','ashu@1999')
    
    sub = 'in district ' + str(dis) + ' Some Slots are available for vaccination. HURRY UP!!!!!!!!!!!!!!'
    body = d
    if l == 0:
        sub = d + " " + str(dis)
        body = "All Slots Booked"

    msg = f"Subject:{sub}\n\n{body}"
    
    server.sendmail(
        'tukusahoo1999@gmail.com',
        'ashutoshkarmakar72@gmail.com',
        msg
    )
def sendErrorMail(status):
    port = 587
    server = sm.SMTP('smtp.gmail.com',port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    
    server.login('tukusahoo1999@gmail.com','ashu@1999')
    
    sub = 'there is a error in requesting data from API'
    body = "The status code is" + status
        

    msg = f"Subject:{sub}\n\n{body}"
    
    server.sendmail(
        'tukusahoo1999@gmail.com',
        'ashutoshkarmakar72@gmail.com',
        msg
    )



IST = pytz.timezone('Asia/Kolkata')
datetime_ist = datetime.now(IST)
url2 = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?"
districtCode = 446


def mainFunction():
    curDate = datetime_ist.strftime('%d:%m:%Y')
    completeUrl = url2 + 'date='+str(curDate) + '&district_id=' + str(districtCode)
    r = requests.get(completeUrl,headers = header)
    if(r.status_code!=200):
        sendErrorMail(r.status_code)
        quit()
    centers = r.json()['centers']
    database = {}
    for center in centers:
        sessions = center['sessions']
        for session in sessions:
            if int(session['available_capacity']) != 0 and session['min_age_limit'] ==18:
                if(session['date'] not in database):
                    database[session['date']] = {'age':[session['min_age_limit']],'name':[center['name']]}
                else:
                    database[session['date']]['age'].append(session['min_age_limit'])
                    database[session['date']]['name'].append(center['name'])
    # print(database)
    if(len(database) != 0):
        print("sending mail.....")
        final = ""
        for i in database.keys():
            fi = str(i) + ":\r\t" + str(database[i]['name'])
            final = final + fi + "\r\n"
        sendMail(final,1,districtCode)
        print(final)
        print("mail sent ....")
    else:
        print("sending mail.....")
        sendMail("From Today to rest of the 7 days there are no slots in district",0,districtCode)
        print("mail sent ....")

sc.every(1).days.do(mainFunction)

while True:
    sc.run_pending()
    time.sleep(1)