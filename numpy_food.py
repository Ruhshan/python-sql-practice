
# coding: utf-8

# In[15]:

import sqlite3

import numpy as np

# Creating connection to a .sqlite3 db. This will create the file when the script runs for the first time
conn = sqlite3.connect('db_big.sqlite3')
# Taking the cursor
c = conn.cursor()


# In[2]:

c.execute('''select inspection.facility_zip, violation.points, strftime("%Y-%m",inspection.activity_date) from inspection join  violation on
inspection.serial_number = violation.serial_number
where inspection.activity_date between date('2015-07-01') and date('2017-12-31')
''')

data = c.fetchall()


# In[3]:

# Converting to database result to numpy array
data = np.asarray(data)


# In[4]:

#deriving unique post codes in all data
all_post_codes = np.unique(data[:,0])

all_post_codes_with_violations = np.empty((3005,2), dtype=object)


# In[5]:

# Calculating total violations for all postcodes
for i in range(len(all_post_codes)):
    total_violations = len(data[np.where(data[:,0] == all_post_codes[i])][:,1].astype(np.int32))
    
    na=np.array([all_post_codes[i], total_violations])
    
    all_post_codes_with_violations[i] = na
    
total_violations = all_post_codes_with_violations[:,1].astype(np.int)
sorted_violations = np.sort(total_violations)[-10:]


# In[6]:

# finding postcodes associated with top violations

top_postcodes = []

for violation in sorted_violations:
    p = all_post_codes_with_violations[np.where(all_post_codes_with_violations[:,1]==str(violation))]
    top_postcodes.append(p[0][0])


# In[7]:

# Monthly violations for top 10 postcodes
from matplotlib import pyplot as plt

dates = np.unique(data[:,2])
#postcode = '90650'

fig, axs = plt.subplots(nrows=5, ncols=2, figsize=(15, 15), sharex='col')

plt.setp(axs, xticks=range(30), xticklabels=dates)

for ax, post_code in zip(axs.flat,top_postcodes):
    postcode = post_code
    violations = np.empty(30)
    c1 = data[:,0] == postcode 
    for i in range(len(dates)):
        c2 = data[:,2] == dates[i]
        data_by_date = data[c1 & c2]
        violations[i] = len(data_by_date)
        
    ax.bar(range(30),violations)
    ax.set_title('Postcode:{} | Count:{}'.format(postcode, int(np.sum( violations))))
    ax.set(ylabel='Violations')

    
axs[4][0].set(xlabel="Months")
axs[4][1].set(xlabel="Months")
for tick in axs[4][0].get_xticklabels():
    tick.set_rotation(90)
    
for tick in axs[4][1].get_xticklabels():
    tick.set_rotation(90)

plt.show()


# In[8]:

# Calculating variances for all post codes
all_post_codes_with_variance = np.empty((3005,2), dtype=object)

for i in range(len(all_post_codes)):
    violation_counts = np.empty(30)
    postcode = all_post_codes[i]
    #c1 = data[:,0] == postcode
    this_postcodes = data[np.where(data[:,0] == postcode)]
    for j in range(len(dates)):
#         c2 = data[:,2] == dates[j]
        for_this_date = this_postcodes[np.where(this_postcodes[:,2] == dates[j])]
        violation_count = len(for_this_date)
        violation_counts[j]=violation_count
    highest = np.max(violation_counts)
    lowest = np.min(violation_counts)
    
    all_post_codes_with_variance[i] = np.array([postcode, highest-lowest])        
    


# In[9]:

# Getting postcodes for top 10 variances
top_variances = np.sort(all_post_codes_with_variance[:,1].astype(np.float32))[-10:]

top_postcodes_by_variance = []

for variance in top_variances:
    p = all_post_codes_with_variance[np.where(all_post_codes_with_variance[:,1]==str(variance))]
    top_postcodes_by_variance.append(p[0][0])


# In[10]:

# Monthly violations for top postcodes with variance
from matplotlib import pyplot as plt2

dates = np.unique(data[:,2])
#postcode = '90650'

fig, axs = plt2.subplots(nrows=5, ncols=2, figsize=(15, 15), sharex='col')

plt2.setp(axs, xticks=range(30), xticklabels=dates)

for ax, post_code in zip(axs.flat,top_postcodes_by_variance):
    postcode = post_code
    violations = np.empty(30)
    c1 = data[:,0] == postcode 
    for i in range(len(dates)):
        c2 = data[:,2] == dates[i]
        data_by_date = data[c1 & c2]
        violations[i] = len(data_by_date)
        
    ax.bar(range(30),violations)
    variance = np.max(violations) - np.min(violations)
    ax.set_title('Postcode:{} | Variance: {}'.format(postcode, variance))
    ax.set(ylabel='Violations')

    
axs[4][0].set(xlabel="Months")
axs[4][1].set(xlabel="Months")
for tick in axs[4][0].get_xticklabels():
    tick.set_rotation(90)
    
for tick in axs[4][1].get_xticklabels():
    tick.set_rotation(90)


plt2.show()


# In[11]:

data[data[:,1]=='CA'].shape


# In[16]:

# Average violation all postcode combined
from collections import OrderedDict
violations_per_month = {}
for i in range(len(dates)):
    date = dates[i]
    condition = data[:,2] == date
    data_by_date = data[condition]
    try:
        violations_per_month[date[5:]].append(len(data_by_date))
    except:
        violations_per_month[date[5:]] = [len(data_by_date)]

average_violations_per_month = OrderedDict()

for month in sorted(violations_per_month.keys()):
    avg = np.average(violations_per_month[month])
    average_violations_per_month[int(month)] = avg


# In[87]:

from matplotlib import pyplot as plt3

plt3.figure(figsize=(15,10))
plt3.bar(np.arange(12), average_violations_per_month.values())

plt3.xticks(np.arange(12), ('Jan', 'Feb', 'Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                                                 'Oct', 'Nov', 'Dec'))
plt3.xlabel('Months')
plt3.ylabel('Average violations')
plt3.title('Average Violations Per Month')
plt3.show()


# In[18]:

# Querying Violations for McDonalds and Burger king

c.execute('''select strftime("%m",inspection.activity_date) d, inspection.program_name
from inspection join  violation on inspection.serial_number = violation.serial_number
where inspection.activity_date between date('2015-07-01') and date('2017-12-31') 
and inspection.program_name like "%mcdonalds%" or  inspection.program_name like "%burger king%" ''')

data = c.fetchall()

data = np.asarray(data)


# In[77]:

# Calculating violations for Macdonalds and Burger King

months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

mac_bur_violatons = []
for month in months:
    mcdonald_count = 0
    burgerking_count = 0
    
    month_data = data[np.where(data[:,0] == month)]
    
    for md in month_data:
        if 'MCDONALDS' in md[1]:
            mcdonald_count+=1
        else:
            burgerking_count+=1
    mac_bur_violatons.append([mcdonald_count, burgerking_count])
mac_bur_violatons = np.asarray(mac_bur_violatons)


# In[88]:

# Plotting Macdonald's and Burger King violations

import matplotlib.pyplot as plt4

x = np.arange(12)

plt4.figure(figsize=(15,10))
plt4.bar(x-0.4, mac_bur_violatons[:,0],width=0.4,color='b',align='center', label='McDonalds')
plt4.bar(x, mac_bur_violatons[:,1],width=0.4,color='g',align='center', label='Burger King')

plt4.xticks(np.arange(12), ('Jan', 'Feb', 'Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep',
                                                 'Oct', 'Nov', 'Dec'))
plt4.legend()
plt4.show()

