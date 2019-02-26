
# coding: utf-8

# In[1]:


# # Parse data from csv of all 600 data entries
# df = pd.read_csv('./entity_file.csv')

# # Lets build some test data
# df2 = pd.DataFrame(data={'id':[df['ID']],
#                         'name':[df['Account Name']],
#                         'geo_long':[df['Longitude']],
#                         'geo_lat':[df['Latitude']],
#                         'access':[df['Accessibility']],
#                         'hrs':[df['Hours']],
                         
#                         'state':[df['State']],
#                         'city':[df['City']],
#                          'zip':[df['Zip Code']],
#                         'street_address':[df['Street Address']],
                        
#                         'lang_list':[df['Languages']],
#                         'amount_left':[df['Current Account Balance']] })
                        
#                         'date':['16-02-2019'],
#                         'out_expenses':[36546],
#                         'in_deposits':[986890],
#                         'loan_bal':[90430],
#                         'loan_int_rate':[2.5],
#                         'next_pmt':[5034]})
# df2 = df2[['id', 'name', 'geo_lat', 'geo_long', 'access', 'hrs', 'state', 'city', 'street_address','zip', 'lang_list', 'amount_left']] #, 'date', 'out_expenses', 'in_deposits', 'loan_bal', 'loan_int_rate', 'next_pmt']]
# df2


# In[2]:


import pandas as pd
import numpy as np
from matplotlib import pyplot as plt


# ## Hackathon Data Analytics

# #### Read in client data

# In[3]:


# Parse data from csv of all 600 data entries
df = pd.read_csv('./entity_file.csv')


# #### Capital One summary info

# In[4]:


# Lets make an entry for capital ones summary of loads
dfCapOne = pd.DataFrame(data={'id':['15071a256c66be5a73e49274'], 
                                'name':['CAPITALONE'],
                                'geo_long':[-77.213120],
                                'geo_lat':[38.924110],
                                'access':[True],
                                'hrs':['24/7'],
                                'state':['VA'],
                                'zip':[22102],
                                'city':['McLean'],
                                'street_name':['Capital One Drive'],
                                'street_number':[1680],
                                'lang_list':[['English']],
                                'total_amount_left':[sum(df['Current Account Balance'])],
                                'date':['16-02-2019'],  })
                              # Check column names below
                              #  'total_out_expenses':[sum(df.out_expenses)],
                              #  'total_in_deposits':[sum(df.in_deposits)],
                              #  'total_loan_bal':[sum(df.loan_bal)],
                              #  'avg_loan_int_rate':[df.loan_int_rate.mean()],
                              #  'total_pmt':[df.next_pmt.sum()]})
#dfCapOne = dfCapOne[['id', 'name', 'geo_lat', 'geo_long', 'access', 'hrs', 'state', 'zip', 'city', 'street_name', 'street_number', 'lang_list', 'total_amount_left', 'date', 'total_out_expenses', 'total_in_deposits', 'total_loan_bal', 'avg_loan_int_rate', 'total_pmt']]
#dfCapOne


# In[132]:


# Cap One summary diagnostics
print("Total scheduled payments for this period: ${}".format(dfCapOne.total_pmt[0]))
print("Total amount loaned out: ${}".format(dfCapOne.total_loan_bal[0]))
print("Estimated amount left after payment")
print("Average loan interest rate: {}%".format(dfCapOne.avg_loan_int_rate[0]))
print("Total amount in client accounts: ${}".format(dfCapOne.total_amount_left[0]))
print()
print("Total client deposits this period: ${}".format(dfCapOne.total_in_deposits[0]))
print("Total client withdrawals this period: ${}".format(dfCapOne.total_out_expenses[0]))


# #### Loan breakdown pie chart

# In[5]:


# Plot loan breakdown
def loanPieChart(entry):
    # Helper function for pie value labels
    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return '${}'.format(absolute)

    # Setup plot
    fig1, ax1 = plt.subplots()
    ax1.axis('equal')
    ax1.set_title("Remaining Loan Breakdown")

    # Setup pie
    labels = 'Remaining Loan\nBalance', 'Next Scheduled\nPayment'
    data = [entry.loan_bal-entry.next_pmt, entry.next_pmt]
    explode = (0, 0.1)
    # Build pie
    wedges, labels, text = ax1.pie(data, explode=explode, labels=labels, autopct=lambda pct:func(pct, data))

    # Place wedge labels
    count = 0
    for label in labels:
        label.set_horizontalalignment('center')

        # Place the remaining loan label
        if (count == 0):
            label.set_position((-1.5,0.3))
            count+=1
        # Place the next payment label
        else:
            label.set_position((1.6,-0.2))
            
    ax1.savefig('piechart_test.png', format='png', dpi=500)


# In[8]:


# Select what entry from the df you want to plot loan info
entry = df.iloc[0]
# Plot the loan info of 'entry'
loanPieChart(entry)


# #### Location of data entries

# In[7]:


def locMap(entry)
    # Location of current record
    import basemap
    import matplotlib.pyplot as plt

    # location of entry
    client_coords = [entry.Latitude[0], entry.Longitude[0]]

    # How much to zoom from coordinates (degrees)
    zoom_scale = 1

    # Setup the bounding box for the zoom and bounds of the map
    bbox = [client_coords[0]-zoom_scale, client_coords[0]+zoom_scale, 
           client_coords[1]-zoom_scale, client_coords[1]+zoom_scale]

    plt.figure(figsize=(12,6))

    # Define the projection, scale, the corners of the map, and the resolution.
    maap = Basemap(projection='merc',llcrnrlat=bbox[0],urcrnrlat=bbox[1],                llcrnrlon=bbox[2],urcrnrlon=bbox[3],lat_ts=10,resolution='i')

    maap.drawparallels(np.arange(bbox[0],bbox[1],(bbox[1]-bbox[0])/5),labels=[1,0,0,0])
    maap.drawmeridians(np.arange(bbox[2],bbox[3],(bbox[3]-bbox[2])/5),labels=[0,0,0,1],rotation=45)
    maap.drawmapboundary(fill_color='dodgerblue')

    # build and plot coordinates onto map
    x,y = maap(my_coords[1],my_coords[0])
    maap.plot(x,y,marker='D',color='r')
    plt.title("Geographic Location of Entry")
    #plt.savefig('coordinate_test.png', format='png', dpi=500)
    plt.show()


# #### Time series data for particular client