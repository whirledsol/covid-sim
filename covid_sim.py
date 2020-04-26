#!/usr/bin/env python3
"""
covid-sim.py
Created:
@author: Will Rhodes

"""
import argparse,re,os,csv,datetime,numpy,warnings,matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
from scipy.optimize import OptimizeWarning,fsolve
import matplotlib.dates as mdates
from sir_model import SIR
import calendar

warnings.simplefilter("ignore", OptimizeWarning)
COUNTRY_POPULATIONS = {"China":1433783686, "US":329064917, "Japan":126860301, "United Kingdom":67530172, "Italy":60550075, "Canada":37411047}
COUNTRY_COLORS =  {'China':'orange','US':'blue','Japan':'yellow','United Kingdom':'purple', 'Italy':'green', 'Canada':'red'}
STATE_POPULATIONS = {"California":39512223,"Texas":28995881,"Florida":21477737,"New York":19453561,"Pennsylvania":12801989,"Illinois":12671821,"Ohio":11689100,"Georgia":10617423,"North Carolina":10488084,"Michigan":9986857,"New Jersey":8882190,"Virginia":8535519,"Washington":7614893,"Arizona":7278717,"Massachusetts":6949503,"Tennessee":6833174,"Indiana":6732219,"Missouri":6137428,"Maryland":6045680,"Wisconsin":5822434,"Colorado":5758736,"Minnesota":5639632,"South Carolina":5148714,"Alabama":4903185,"Louisiana":4648794,"Kentucky":4467673,"Oregon":4217737,"Oklahoma":3956971,"Connecticut":3565287,"Utah":3205958,"Puerto Rico":3193694,"Iowa":3155070,"Nevada":3080156,"Arkansas":3017825,"Mississippi":2976149,"Kansas":2913314,"New Mexico":2096829,"Nebraska":1934408,"West Virginia":1792065,"Idaho":1787147,"Hawaii":1415872,"New Hampshire":1359711,"Maine":1344212,"Montana":1068778,"Rhode Island":1059361,"Delaware":973764,"South Dakota":884659,"North Dakota":762062,"Alaska":731545,"District of Columbia":705749,"Vermont":623989,"Wyoming":578759}

logistic = lambda x,l,k,o: l / (1 + numpy.exp(k*(o-x)))

expo = lambda x,a,b: a* numpy.exp(b*x)

FORMULAE = {
    logistic:'$y=\\frac{{{0:.3f}}}{{1+e^{{{1:.3f}({2:.3f}-x)}}}}$',
    expo:'$y={0:.3f}e^{{{1:.3f}x}}$'
}



def start():
    PATH_BASE = os.path.expanduser('~/projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series')
    OUTPUT_BASE = './out/'
    PATH_TIME_CONFIRMED_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_confirmed_global.csv')
    PATH_TIME_DEATHS_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_deaths_global.csv')
    PATH_TIME_RECOVERY_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_recovered_global.csv')
    PATH_TIME_CONFIRMED_US = os.path.join(PATH_BASE,'time_series_covid19_confirmed_US.csv')

    important_states = ['New York','New Jersey','Pennsylvania','California']
   
    custom_trend_us(PATH_TIME_CONFIRMED_US,important_states)

    custom_delta_us_county(PATH_TIME_CONFIRMED_US,'Bucks','Pennsylvania','Confirmed')


    custom_delta_us(PATH_TIME_CONFIRMED_US,important_states,'Confirmed')

    custom_new_us(PATH_TIME_CONFIRMED_US,important_states)

    ##Extrapolation data uninformative - replacing with sir_learner
    #custom_extrapolate_us(PATH_TIME_CONFIRMED_US,important_states)
    
    custom_deathrate_global(PATH_TIME_CONFIRMED_GLOBAL,PATH_TIME_DEATHS_GLOBAL)

    custom_zero_global(PATH_TIME_CONFIRMED_GLOBAL)

    custom_map_us(PATH_TIME_CONFIRMED_US)
    
    #custom_fit_us(PATH_TIME_CONFIRMED_US,OUTPUT_BASE, important_states)
def custom_delta_us_county(path,county,state,label):
    '''
    Shows trend over time for one county
    '''
    x,y = parse_time_us_county(path,county,state)
    graph_delta(x,y,f"{county}, {state}",label)

def custom_delta_us(path,states,label):
    '''
    Shows trend over time for various states
    '''
    for state in states:
        x,y = parse_time_us(path,state)
        graph_delta(x,y,state,label)

def custom_trend_us(path,states,threshold=100):
    '''
    Shows the changes for each day of the week to see if there is a weekly trend
    '''
    for state in states:
        x,y = parse_time_us(path,state)
        y = [v for v in y if v>threshold]
        x = x[-len(y):]
        dy = [0]+[y[i]-y[i-1] for i,v in enumerate(y) if i>0]
        x = [d.weekday() for d in x]

        bins = [[] for i in range(7)]

        for i in range(len(x)):
            bins[x[i]].append(dy[i])
        
        _, ax = plt.subplots()

        ax.boxplot(bins)
        ax.set_title(f'Weekly Trend of New Cases in {state}')
        ax.set_xlabel('Day of Week')
        ax.set_ylabel('New Cases')
        toCalendarDay = lambda x, pos:calendar.day_name[x-1]
        ax.xaxis.set_major_formatter(plt.FuncFormatter(toCalendarDay))
        
        plt.show()

def custom_deathrate_global(path,deathpath):
    '''
    Creates a markdown graph which shows the current deathrate by country
    '''
    cpersent = {}
    drates = {}
    for country,population in COUNTRY_POPULATIONS.items():
        _,y = parse_time_global(path,country)
        _,dy = parse_time_global(deathpath,country)
        latest = max(dy)/max(y)
        cpersent[country] = max(y)/population
        drates[country] = latest
    
    print('|Country|Percent Infected|Death Rate|')
    print('|---|------:|------:|')
    for country,rate in sorted(drates.items(), key=(lambda item: item[1]), reverse=True):
        print('|{0}|{1:0.6f}|{2:0.6f}|'.format(country,cpersent[country],rate))
    print('\n')

def custom_recovery_us(path,recoverypath,important_states):
    '''
    Shows percent of state vs percent of US over time
    '''
    for state in important_states:
        _, ax = plt.subplots()
        
        x,y = parse_time_us(path,state)
        rx,ry = parse_time_us(recoverypath,state)

        date_first = x[y.index([i for i in y if i>0][0])]
        ry = ry[rx.index(date_first):]
        y = [i for i in y if i>0]
        x = [i for i in x if i>=date_first]
        
        ax.set_title('US Cases and Recovery')
        ax.set_xlabel('Date')
        ax.set_ylabel('Incidents (Log Scale)')
        
        ax.plot(x,y,label='Cases',c=numpy.random.rand(3,),linewidth=2)
        ax.plot(x,ry,label='Recovery',c=numpy.random.rand(3,),linewidth=1)
        ax.legend()
        ax.set_yscale('log')
        plt.show()

def custom_new_us(path,check_states=[],min_cases=0):
    '''
    Shows the increase in cases since previous day for various states over time
    '''
    _, ax = plt.subplots()
    for state in check_states:
        _,y = parse_time_us(path,state)
        y = [v-y[i-1] for i, v in enumerate(y) if v>min_cases and i>min_cases]
        x = range(len(y))
        ax.plot(x,y,c=numpy.random.rand(3,),label=state)
    
    ax.set_xlabel('Days since at least {} cases in that state'.format(min_cases))
    ax.set_ylabel('New Cases since Previous Day')
    ax.set_title('New Cases Per Day for Various States')
    ax.legend()
    plt.show()       

def custom_map_us(path):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        _,y = parse_time_us(path,state)
        y = [i/population for i in y if i>0]
        states[state] = max(y) if len(y) > 0 else 0
    us_map(states,'Percentage of State Population Infected',formatter='{0:.6f}')

def custom_fit_us(path,OUTPUT_BASE,check_states=[],min_days=5, min_cases=500):
    '''
    Fits data to curve, saves the best fit, displays base on map. Redder means high rate.
    '''
    states = {}
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    outpath = os.path.join(OUTPUT_BASE,'states_bestfit_{}.csv'.format(timestamp))

    with open(outpath,'w') as f:
        for state,_ in list(STATE_POPULATIONS.items()):
            _,y = parse_time_us(path,state)
            y = [i for i in y if i>min_cases]
            if(len(y)>min_days): #we need >3 days worth of data
                #print(state)
                x = range(len(y)) #create days
                try:
                    params,_ = curve_fit(expo, x, y)
                    states[state] = params[1]

                    if(state in check_states):
                        graph_fit(x,y,expo,'{} Case Growth'.format(state))
                    f.write('{},{},{}\n'.format(state,*params))
                except:
                    raise ValueError('Could not find best fit for {}'.format(state))

    us_map(states,'Case Growth')


def custom_zero_global(path,min_cases=100):
    '''
    Shows cases over time starting the day at least min_cases were hit for each country
    '''
    _, ax = plt.subplots()
    
    for country,population in COUNTRY_POPULATIONS.items():
        _,y = parse_time_global(path,country)
        y = [i/population for i in y if i>min_cases]
        x = range(len(y))
        _,formula = best_fit(x,y,expo,bounds=[0,0.9],label=country)
        label = '{}  {}'.format(country,formula)
        ax.plot(x, y, c=COUNTRY_COLORS[country],label=label)

    ax.set_xlabel('Days since at least {} cases in that country'.format(min_cases))
    ax.set_ylabel('Percent Population Infected')
    ax.set_title('Percent of Country Infected After {} Cases'.format(min_cases))
    ax.legend()
    plt.show()


def custom_extrapolate_us(path,important_states,duration = 90):
    '''
    Extrapolates the current data to fit func
    '''
    bounds = ([0.1,-1,12], [0.7,1,duration])

    _, ax = plt.subplots()
    for i,state in enumerate(important_states):
        x,y = parse_time_us(path,state)
        y = [i/STATE_POPULATIONS[state] for i in y if i>0]
        xd = x[-len(y):]
        x = range(len(y))
        ax.plot(xd,y,c=numpy.random.rand(3,),label=state,linewidth=3)

        params,formula = best_fit(x,y,logistic,bounds,state)
        
        xd = get_date_range(xd[0],duration)
        x = range(duration)
        y = logistic(x,*params)
        
        y = [i for i in y if i<=100]
        x = x[0:len(y)]
        xd = xd[0:len(y)]

        ax.plot(xd,y,c=numpy.random.rand(3,),label=formula,dashes=[6, 2],linewidth=1)

        ax.legend()
        
        ax.set_xlabel('Date')
        axFormatDate(ax)
        
        ax.set_ylabel('Percent of Population Infected')
        ax.yaxis.set_major_formatter(matplotlib.ticker.StrMethodFormatter('{x:.6f}'))
        
        ax.set_title('Extrapolation of Cases in Various States')
    plt.show()





def parse_time_us_county(path,county,state):
    return parse_time(path,county,5,11,value2=state,value2_idx=6)

def parse_time_us(path,state):
    return parse_time(path,state,6,11)

def parse_time_global(path,country):
    return parse_time(path,country,1,4)

def parse_time(path,value,value_idx,date_start_idx,value2=None,value2_idx=None):
    '''
    parse a time series file from the COVID-19 repo
    '''
    with open(path, 'r') as f:
        header = f.readline()
        date_start = header.split(',')[date_start_idx]
        days = len(header.split(','))-date_start_idx
        #print('parsing {} days worth of data'.format(days))

        x = get_date_range(date_start,days)
        y = list(numpy.zeros(days))

        reader = csv.reader(f, delimiter=",")
        for _, row in enumerate(reader):
            if(row[value_idx] == value):
                if(value2 is None or row[value2_idx] == value2):
                    new = row[date_start_idx:]
                    try:
                        y = [int(a or '0') + int(b or '0') for a,b in zip(y, new)]
                    except:
                        print(new)
                        raise ValueError('Could not parse values')
        return x,y


def get_date_range(date_start,length):
    '''
    creates an array of dates
    '''
    base = date_start if isinstance(date_start, datetime.date) else datetime.datetime.strptime(date_start,'%m/%d/%y')
    return [base + datetime.timedelta(days=x) for x in range(length)]


def best_fit(x,y,func=expo,bounds=[-numpy.Inf,numpy.Inf],label='dat data'):
    '''
    attempt to find the best fit params and formula
    '''
    try:
        params,_ = curve_fit(func, x, y, maxfev=10000, bounds = bounds)
        formula = FORMULAE[func].format(*params)
        return params,formula
    except:
        print('Could not find a curve for {}'.format(label))
        return [],''

def graph_fit(x,y,func,title=''):
    '''
    Show the data and best fit curve (using func) and formula too!
    '''
    
    params,formula = best_fit(x,y,func,label=title)
    if(len(params) == 0): return

    _, ax = plt.subplots()
    ax.plot(x,y,c='red',linewidth=2)
    ax.plot(x,func(x,*params),c='blue',linewidth=1)
    formula = FORMULAE[func].format(*params)
    ax.text(0, max(y), formula) 

    ax.set_xlabel('Days with Cases')
    ax.set_ylabel('Number of Confirmed Cases')
    ax.set_title(title)
    plt.show()

def us_map(states,title = '',text_top=5,formatter = '{0:.3f}'):
    '''
    show a us map with state color highlighting
    '''
    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.LambertConformal())

    ax.set_extent([-125, -66.5, 20, 50], ccrs.Geodetic())

    shapename = 'admin_1_states_provinces_lakes_shp'
    states_shp = shpreader.natural_earth(resolution='110m',category='cultural', name=shapename)

    ax.background_patch.set_visible(False)
    ax.outline_patch.set_visible(False)
    ax.set_title(title)
    mn = min(states.values())
    mx = max(states.values())

    #find the min value that we will display text values for
    text_top = min(text_top,len(states.values()))
    text_threshold = list(states.values())
    text_threshold.sort()
    text_threshold = min(text_threshold[-text_top:])

    for state in shpreader.Reader(states_shp).records():

        edgecolor = 'black'

        try:
            value = states[state.attributes['name']]
        except:
            value = mn

        facecolor = cmap(value,mn,mx)
            

        # `state.geometry` is the polygon to plot
        ax.add_geometries([state.geometry], ccrs.PlateCarree(),
                        facecolor=facecolor, edgecolor=edgecolor)

        #add text if value is over threshold
        if value >= text_threshold:
            x = state.geometry.centroid.x        
            y = state.geometry.centroid.y
            ax.text(x, y, formatter.format(value),size=7, color='blue', ha='center', va='center', transform=ccrs.PlateCarree())   
            
    plt.show()


def graph_delta(x,y,location,label,threshold=100):
    '''
    Shows data, first, and second derivative
    '''
    y = [v for v in y if v>threshold]
    x = x[-len(y):]
    dy = [0]+[y[i]-y[i-1] for i,v in enumerate(y) if i>0]
    dy2 = [0]+[dy[i]-dy[i-1] for i,v in enumerate(dy) if i>0]

    _, ax = plt.subplots()
    ax.plot(x,y,label=label,c=numpy.random.rand(3,),linewidth=2)
    ax.plot(x,dy,label=f'Newly {label}',c=numpy.random.rand(3,),linewidth=2)
    ax.plot(x,dy2,label=f'{label} Change',c=numpy.random.rand(3,),linewidth=2)
    
    ax.plot(x,[0]*len(x),c='black',label='0',linewidth=1) #zero line
    ax.legend()
    ax.set_xlabel('Date')
    axFormatDate(ax)
    ax.set_ylabel('Number')
    ax.set_title(f'{label} Trend in {location}')
    #ax.set_yscale('log')

    plt.show()
    
def cmap(value,mn,mx):
    value = numpy.abs(value)
    mn = numpy.abs(mn)
    mx = numpy.abs(mx)
    bg = 1-((value-mn)/(mx-mn)) #pow(scale,1-normalized)/scale
    return [1,bg,bg]

def axFormatDate(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))

if  __name__ =='__main__':start()