"""
covid_sim_base.py
common functions
@author: whirledsol
"""
import csv,datetime,numpy,matplotlib,calendar,json,requests
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.optimize import curve_fit
import cartopy.crs as ccrs
import cartopy.io.shapereader as shpreader
import cartopy.feature as cfeature
from covid_sim_constants import *

logistic = lambda x,l,k,o: l / (1 + numpy.exp(k*(o-x)))
expo = lambda x,a,b: a* numpy.exp(b*x)

FORMULAE = {
    logistic:'$y=\\frac{{{0:.3f}}}{{1+e^{{{1:.3f}({2:.3f}-x)}}}}$',
    expo:'$y={0:.3f}e^{{{1:.3f}x}}$'
}

def queryApi(endpoint, parameters={}):
    res = requests.get(endpoint, params=parameters)
    if res.status_code != 200:
        raise Exception(f'Request failed with status {res.status_code}')
    return json.loads(res.content)

def parse_time_county(path,county,state):
    return parse_time(path,county,5,11,value2=state,value2_idx=6)

def parse_time_states(path,state):
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


def us_map_county(county_data, state, title,text_top=5,formatter = '{0:.3f}', county_data_file='./assets/us_counties_2018/cb_2018_us_county_20m.shp'):
    '''
    shows a US map with counties! Hot dog!
    '''

    try:
        reader = shpreader.Reader(county_data_file)
    except Exception as ex:
        print(f'Ensure {county_data_file} is installed.')
        raise ex

    counties = list(reader.records())
    
    plt.figure(figsize=(10, 6))
    ax = plt.axes(projection=ccrs.PlateCarree())
    
    #get min and max
    mn = min(county_data.values())
    mx = max(county_data.values())
    edgecolor = 'black'
    
    counties = [x for x in counties if x.attributes['STATEFP'] == STATE_FIPS_CODES[state]]
    
    #find the min value that we will display text values for
    text_top = min(text_top,len(county_data.values()))
    text_threshold = list(county_data.values())
    text_threshold.sort()
    text_threshold = min(text_threshold[-text_top:])

    #itterate
    for county in counties:
        
        try:
            value = county_data[county.attributes['NAME']]
        except:
            continue

        facecolor = cmap(value,mn,mx)
        
        ax.add_geometries([county.geometry], ccrs.PlateCarree(),
                        facecolor=facecolor, edgecolor=edgecolor)
        
        #add text if value is over threshold
        if value >= text_threshold:
            x = county.geometry.centroid.x        
            y = county.geometry.centroid.y
            ax.text(x, y, formatter.format(value),size=7, color='blue', ha='center', va='center', transform=ccrs.PlateCarree())   
    
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
    edgecolor = 'black'

    #find the min value that we will display text values for
    text_top = min(text_top,len(states.values()))
    text_threshold = list(states.values())
    text_threshold.sort()
    text_threshold = min(text_threshold[-text_top:])

    for state in shpreader.Reader(states_shp).records():
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


def graph_new(x,y,location,label,threshold=100):
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

    return ax
    
def graph_sum(x,y,title,threshold=100, date_range=14, normalize=None):
    '''
    Shows data, first, and second derivative
    '''
    y = [v for v in y if v>threshold]
    dy = [0]+[y[i]-y[i-1] for i,v in enumerate(y) if i>0]
    sy = [numpy.sum(dy[(i-date_range):i]) for i,v in enumerate(dy) if i>=date_range]
    x = x[-len(sy):]

    if normalize:
        sy = [normalize(v) for v in sy]

    _, ax = plt.subplots()
    ax.plot(x,sy,c=numpy.random.rand(3,),linewidth=2)
    
    ax.plot(x,[0]*len(x),c='black',label='0',linewidth=1) #zero line
    ax.legend()
    ax.set_xlabel('Date')
    axFormatDate(ax)
    ax.set_ylabel('Number')
    ax.set_title(title)
    #ax.set_yscale('log')

    return ax
    
def cmap(value,mn,mx):
    mn = 0 if mn < 0 else mn
    mx = 0 if mx < 0 else mx
    value = 0 if value < 0 else value
    bg = 1-((value-mn)/((mx-mn)+0.000000001)) #pow(scale,1-normalized)/scale
    return [1,bg,bg]


def axFormatDate(ax):
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%Y'))
