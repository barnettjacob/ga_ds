
from datetime import date, datetime, timedelta
import copy
import sys
import pandas as pd
import numpy as np
import pymysql
import matplotlib.pyplot as plt
# pd.options.display.mpl_style = 'default'
# print sys.version
# print "Pandas:", pd.version.version


# In[139]:

conn = pymysql.connect(host = 'analytics-db.housetrip.com', port = 3306, user = 'jbarnett', db = 'housetrip_production', passwd = '8NxWM7Nrtbon75T5x1F0g2ReWacgGyjfY')


# In[183]:

sql = ('SELECT r.property_id, r.start_date, r.end_date, r.average_price_per_night, r.minimum_days_of_stay ' 
       'FROM rates r '
       'LEFT JOIN dw_properties p ON p.property_id = r.property_id '
       'WHERE r.end_date > CURDATE() '
       'AND p.status = "Live" '
       'AND r.property_id < 10000'
      )
rates = pd.read_sql(sql, con = conn)


# In[186]:

master_frame = pd.DataFrame(columns = ['date', 'price', 'min_stay', 'property_id'])

properties = pd.DataFrame(pd.unique(rates.property_id.ravel()))

#loop over properties
for j in range(0, len(properties)):

    #property level loop
    prop_id = properties.iloc[j,0]
    this_prop = rates[rates.property_id == prop_id]
    prop_frame = pd.DataFrame(columns = ['date', 'price', 'min_stay', 'property_id'])

    for i in range(0,len(this_prop)):

        start = this_prop.iloc[i,1] #add logic so starts on current day
        end = this_prop.iloc[i,2]
        dates = []
        
        #adjust start so that it is not in the past
        if start < date.today():
            start =  date.today()
        else:
            start = start

        curr = start
        while curr < end:
            dates.append(curr)
            curr += timedelta(days=1)

        rate_days = pd.DataFrame(dates)
        rate_days.columns = ['date']
        rate_days['property_id'] = prop_id
        rate_days['price'] = this_prop.iloc[i,3]
        rate_days['min_stay'] = this_prop.iloc[i,4]

        prop_frame = pd.concat([prop_frame, rate_days])
    
    master_frame = pd.concat([master_frame, prop_frame])
    print prop_id
# prop_frame


# In[ ]:



