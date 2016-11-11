import sqlite3
import sys
import os

#dbname = 'cityData.db'
def initdb(dbname):
    db = sqlite3.connect(dbname)
    #os.system('rm cityData.db')
    print "Database opened successfully!"
    
    db.executescript('''
           DROP TABLE IF EXISTS {tn1} ;
           CREATE TABLE {tn1}
          (DISTRICT_HASH TEXT PRIMARY KEY NOT NULL,
           ID            INT              NOT NULL)'''\
          .format(tn1 ='DistMapping'))

    db.executescript('''
           DROP TABLE IF EXISTS {tn2};
           CREATE TABLE {tn2}
          (ORDER_ID          TEXT NOT NULL,
           DRIVER_ID         TEXT,
           PASSENGER_ID      TEXT,
           START_DISTRICT_ID TEXT  NOT NULL,
           DEST_DISTRICT_ID  TEXT  NOT NULL,
           PRICE             DOUBLE,
           TIME              DATETIME NOT NULL,
           DATE              INT      NOT NULL,
           SLOTID            INT      NOT NULL)'''\
          .format(tn2 ='Orders'))

    db.executescript('''
           DROP TABLE IF EXISTS {tn3};
           CREATE TABLE {tn3}
          (DISTRICT_HASH TEXT NOT NULL,
           CLASS_HIGH    INT  NOT NULL,
           CLASS_LOW     INT  NOT NULL,
           NUM           INT  NOT NULL)'''\
          .format(tn3 ='POI'))

    db.executescript('''
           DROP TABLE IF EXISTS {tn4};
           CREATE TABLE {tn4}
          (DISTRICT_HASH TEXT  NOT NULL,
           TJ_LEVEL1     INT   NOT NULL,
           TJ_LEVEL2     INT   NOT NULL,
           TJ_LEVEL3     INT   NOT NULL,
           TJ_LEVEL4     INT   NOT NULL,
           TJ_TIME       DATETIME,
           DATE          INT   NOT NULL,
           SLOTID        INT   NOT NULL)'''\
          .format(tn4 = 'Traffic'))

    db.executescript('''
           DROP TABLE IF EXISTS {tn5};
           CREATE TABLE {tn5}
          (TIME        DATETIME  NOT NULL,
           WEATHER     INT       NOT NULL,
           TEMPERATURE DOUBLE    NOT NULL,
           PM25        DOUBLE    NOT NULL,
           DATE        INT       NOT NULL,
           SLOTID      INT       NOT NULL)'''\
          .format(tn5 = 'Weather'))


    db.commit()
    print "Create tables...DONE!"
    db.close()
