/*
-- column names
.headers on  
.mode csv 
--write the query result into this file
.once trainSet5.csv  */


SELECT  a.GAP, c.ID, a.DATE, a.SLOTID,
        b.WEATHER,b.PM25,b.TEMPERATURE, 
        e.TJ_LEVEL1,e.TJ_LEVEL2,e.TJ_LEVEL3,e.TJ_LEVEL4,d.*
FROM  (SELECT START_DISTRICT_ID AS DISTRICT_HASH , DATE, SLOTID, count(ORDER_ID) AS GAP 
		  	    FROM Orders where DRIVER_ID = "NULL" group by START_DISTRICT_ID, DATE, SLOTID) AS a
LEFT JOIN (SELECT DATE, SLOTID, WEATHER, AVG(PM25) AS PM25, AVG(TEMPERATURE) AS TEMPERATURE 
		   	     FROM Weather  group by DATE, SLOTID ) AS b  ON a.DATE=b.DATE and a.SLOTID=b.SLOTID 
LEFT JOIN DistMapping AS c ON a.DISTRICT_HASH = c.DISTRICT_HASH	 
LEFT JOIN Traffic AS e ON a.DISTRICT_HASH = e.DISTRICT_HASH 
                         and a.DATE = e.DATE and a.SLOTID = e.SLOTID
LEFT JOIN POI_NEW AS d ON a.DISTRICT_HASH = d.DISTRICT_HASH;	 