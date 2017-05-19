import urllib
import sqlite3
import json
import time

#geoload.py creates a connection to the google geocode api
#retrieve some geodata as json and store in sqlite

apikey="AIzaSyANLISebyvHyGHYEYhCH2L3qmbCyosgJWY"
server = "http://maps.googleapis.com/maps/api/geocode/json?"

#connection to the sqlite local data base
conn=sqlite3.connect('geodata.sqlite')
cur=conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata TEXT)''')

#where.data is a file that has the address of various locations
inputfile = open('where.data')
count=0
    for line in inputfile:
        #break if we reach accress limit
        if count > 200: break
        address=line.strip()
        cur.execute("SELECT geodata FROM Locations Where address=?", (buffer(address),))

        #check if the address is already in the database, so we don't waste our access
        try:
            data=cur.fetchone()[0]
            print "Found in database ",address
            continue
        except:
            pass

        print 'Resolving', address
        #we use the url following google geocode api guideline
        url = server+urllib.urlencode({'sensor':'false', 'address': address})
        print 'Retrieving', url
        #connect to the address
        uh = urllib.urlopen(url, context=None)
        data=uh.read()
        print 'Retrieved', len(data), 'characters', data[:20].replace('\n',' ')
        count += 1
        try:
            #load the geodata in json
            js=json.loads(str(data))
        except:
            continue

        if 'status' not in js or (js['status']!='OK' and js['status']!='ZERO_RESULTS'):
            print '=====Failed to Retrieve====='
            print data
            continue

        cur.execute('''INSERT INTO Locations(address, geodata) VALUES (?,?)''',(buffer(address),buffer(data)))
        conn.commit()
        if count %10==0:
            print('Pausing for a bit...')
            time.sleep(5)