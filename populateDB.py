import sqlite3
import sys
import re
import glob


def fill_dist(db, tablename, mydir):
#    db.execute("DELETE TABLE IF EXISTS {tn}".format(tn=tablename))
    fhdl = open(mydir+'cluster_map/cluster_map', "r")
    for line in fhdl:
        # hash \t mapping
        entry = line.split('\t')
        query = '''
                INSERT INTO {tn}
                VALUES(?,?)
                '''.format(tn=tablename)
        db.execute(query, (entry[0], entry[1]))
    db.commit()
    print "Populate Table: 'DistMapping'...DONE"


def fill_orders(db, tablename, mydir):
#    db.execute("DELETE TABLE IF EXISTS {tn}".format(tn=tablename))
    '''
    fnamebase = 'order_data_2016-01-'
    for i in range(1, 22):
        if i < 10:
            fname = fnamebase+'0'+str(i)
        else:
            fname = fnamebase+str(i)

        fhdl = open(mydir+'order_data/'+fname, "r")
    '''
    files = glob.glob(mydir+'order_data/order*')
    for f in files:
        with open(f, 'r') as fhdl:
            for line in fhdl:
                # hash \t mapping
                entry = line.split('\t')
                dt = entry[6].split(' ')
                (h, m, s) = dt[1].split(':')
                slotid = (int(h)*60+int(m))/10
                query = '''
                    INSERT INTO {tn}
                    VALUES(?,?,?,?,?,?,?,?,?)
                    '''.format(tn=tablename)
            
                db.execute(query, (entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6], dt[0],slotid))
    db.commit()
    print "Populate Table: 'Orders'...DONE"

def fill_poi(db, tablename, mydir):
#    db.execute("DELETE TABLE IF EXISTS {tn}".format(tn=tablename))
    fhdl = open(mydir+'poi_data/poi_data', "r")
    for line in fhdl:
        # hash \t mapping
        entry = re.split('\t|\n', line)
#        print entry
        for i in range(1, len(entry)-1): # -1 is needed because the last element of 'entry' is '\n'
            # use "re" module to handle two delimiters
            poi = entry[i].split('#')
            if len(poi) == 1:
                classHigh = 0
                poii = poi[0].split(':')
            else:
                classHigh = poi[0]
                poii = poi[1].split(':')

            if len(poii) == 1:
                num = poii[0]
                classLow = 0
            else:
                classLow = poii[0]
                num = poii[1]
            query = '''
                    INSERT INTO {tn}
                    VALUES(?,?,?,?)
                    '''.format(tn=tablename)
            db.execute(query, (entry[0], classHigh, classLow, num))
    db.commit()
    print "Populate Table: 'POI'...DONE"

def fill_traffic(db, tablename, mydir):
#    db.execute("DELETE TABLE IF EXISTS {tn}".format(tn=tablename))
    '''
    fnamebase = 'traffic_data_2016-01-'
    for i in range(1, 22):
        if i < 10:
            fname = fnamebase+'0'+str(i)
        else:
            fname = fnamebase+str(i)

        fhdl = open(mydir+'traffic_data/'+fname, "r")
    '''
    files = glob.glob(mydir+'traffic_data/traffic*')
    for f in files:
        with open(f, 'r') as fhdl:
            for line in fhdl:
                # hash \t mapping
                entry = re.split('\t|\r', line)
                query = '''
                    INSERT INTO {tn}
                    VALUES(?,?,?,?,?,?,?,?)
                    '''.format(tn=tablename)
                lvl1 = entry[1].split(':')
                lvl2 = entry[2].split(':')
                lvl3 = entry[3].split(':')
                lvl4 = entry[4].split(':')
                dt = entry[5].split(' ')
                (h, m, s) = dt[1].split(':')
                slotid = (int(h)*60+int(m))/10
#                print slotid
                db.execute(query, (entry[0], lvl1[1], lvl2[1], lvl3[1], lvl4[1], entry[5], dt[0], slotid))
    db.commit()
    print "Populate Table: 'Traffic'...DONE"    

def fill_weather(db, tablename, mydir):
#    db.execute("DELETE TABLE IF EXISTS {tn}".format(tn=tablename))
    '''
    fnamebase = 'weather_data_2016-01-'
    for i in range(1, 22):
        if i < 10:
            fname = fnamebase+'0'+str(i)
        else:
            fname = fnamebase+str(i)

        fhdl = open(mydir+'weather_data/'+fname, "r")
    '''

    files = glob.glob(mydir+'weather_data/weather*')
    for f in files:
        with open(f, 'r') as fhdl:
            for line in fhdl:
                # hash \t mapping
                #            entry = re.split('\t|\r', line)
                entry = line.split('\t')
                query = '''
                    INSERT INTO {tn}
                    VALUES(?,?,?,?,?,?)
                    '''.format(tn=tablename)

                dt = entry[0].split(' ')
                (h, m, s) = dt[1].split(':')
                slotid = (int(h)*60+int(m))/10
                db.execute(query, (entry[0], entry[1], entry[2], entry[3], dt[0], slotid))
    db.commit()
    print "Populate Table: 'Weather'...DONE"

#if __name__ == "__main__":
def populatedb(dbname, dirname):
    db = sqlite3.connect(dbname)
    mydir = dirname
    if mydir[-1] != '/':
        mydir = mydir+'/'

    fill_dist(db, 'DistMapping', mydir)
    fill_orders(db, 'Orders', mydir)
    fill_poi(db, 'POI', mydir)
    fill_traffic(db, 'Traffic', mydir)
    fill_weather(db, 'Weather', mydir)
    db.close()
