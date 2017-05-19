import sqlite3
import json
import codecs

#geodump.py takes the address and the geodata from our database geodata.sqlite
#and retreive its coordinates and write them in the json file where.js
#where the information can be read by html

conn = sqlite3.connect('geodata.sqlite')
cur = conn.cursor()

cur.execute('SELECT * FROM Locations')
#load or make new json file in utf-8 format
fhand = codecs.open('where.js','w','utf-8')
fhand.write("myData = [\n")
count=0
for row in cur:
    #load the second element(geodata) from each tuple
    data=str(row[1])
    try: js = json.loads(str(data))
    except: continue

    #if not properly load, skip to the next iteration
    if not('status' in js and js['status']=='OK'): continue

    lat=js["results"][0]["geometry"]["location"]["lat"]
    lng=js["results"][0]["geometry"]["location"]["lng"]
    #again, skip to the next iteration if there is no data for long and lat
    if lat == 0 or lng ==0: continue
    where = js['results'][0]['formatted_address']
    where = where.replace("'","")

    try:
        print where, lat, lng

        count+=1
        #add onto existing list
        if count >1: fhand.write(",\n")
        output = "["+str(lat)+","+str(lng)+", '"+where+"']"
        fhand.write(output)
    except: continue

fhand.write("\n];\n")
cur.close()
fhand.close()
print count, "records written to where.js"


