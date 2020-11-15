"""
covid_sim_crunches_tracking.py
quick crunches of the data from covidtracking.com
@author: whirledsol
"""
import datetime
from covid_sim_base import *

def extractTimeseries(data, func):
    '''
    assuming the [{}] data structure from CovidTracking,
    extracts the xs and ys 
    '''
    xs=[]
    ys=[]
    for day in data:
        date = datetime.datetime.strptime(str(day['date']),'%Y%m%d')
        xs.append(date)
        ys.append(func(day))
    return xs, ys



def crunch_perPositive_us(data,state=None):
    '''
    Timeseries of percentage of tests that are positives (excludes pending)
    '''
    if state is not None:
        data = [r for r in data if r['state'] == STATE_ABBREV[state]]
        
    xs,ys = extractTimeseries(data,
        lambda d: int(d['positive'] or 0)/(int(d['totalTestResults'] or 0) + 0.001)
    )
    
    _, ax = plt.subplots()
    ax.plot(xs,ys,c='red',linewidth=2)

    ax.set_xlabel('Date')
    ax.set_ylabel('Percentage')
    ax.set_title(f"Percentage of Positive Cases {('' if state is None else state)}")
    axFormatDate(ax)
    plt.show()



def crunch_perOutcomes_us(data,state=None):
    '''
    Timeseries of percentage of tests that are positives (excludes pending)
    '''
    if state is not None:
        data = [r for r in data if r['state'] == STATE_ABBREV[state]]
      

    xs,pys = extractTimeseries(data,
        lambda d: int(d['positive'] or 0)
    )
    _,hys = extractTimeseries(data,
        lambda d: int(d['hospitalizedCumulative'] or 0)
    )
    _,dys = extractTimeseries(data,
        lambda d: int(d['death'] or 0)
    )

    rge = range(len(pys))
    hys = [hys[i]-dys[i] for i in rge]
    pys = [pys[i]-hys[i] for i in rge]

    _, ax = plt.subplots()
    p1 = ax.bar(xs, pys, width=1)
    p2 = ax.bar(xs, hys, width=1)
    p3 = ax.bar(xs, dys, width=1)

    ax.set_ylabel('Count')
    ax.set_title('Positive Case Outcomes')
    ax.legend((p1[0], p2[0], p3[0]),
    ('Positive', 'Hospitalized','Deaths'))

    axFormatDate(ax)
    plt.show()
    

