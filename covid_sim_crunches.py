"""
covid_sim_base.py
quick crunches of the data
@author: whirledsol
"""
import datetime,numpy,matplotlib
from covid_sim_base import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def crunch_map_per_county(c_path,state,days=7, min_cases=100):
    '''
    shows percent increase in past {days} for each county in state
    DISCLAIMER: county names for state need to be defined in covid_sim_base
    '''
    county_data = {}
    for county in COUNTY_NAMES[state]:
        cx,cy = parse_time_county(c_path,county,state)
        cy = [i for i in cy if i>min_cases]
        cy.insert(0,min_cases) #insert to prevent len == 0
        confirmed_f = cy[-1]
        confirmed_i = cy[-days] if len(cy) > days else cy[0]
        county_data[county] = (confirmed_f-confirmed_i)/confirmed_i*100

    toDate = cx[-1].strftime("%b %d, %Y")
    fromDate = cx[-days].strftime("%b %d, %Y")
    title =  f'Percent Increase Per County in {state}\n{fromDate}-{toDate}'
    us_map_county(county_data,state,title,formatter='{0:.2f}%')

def crunch_map_county(c_path,state):
    '''
    shows confirmed counts for all counties in a state by county name
    DISCLAIMER: county names for state need to be defined in covid_sim_base
    '''
    county_data = {}
    for county in COUNTY_NAMES[state]:
        cx,cy = parse_time_county(c_path,county,state)
        county_data[county] = cy[-1]
    us_map_county(county_data, f'Confirmed Cases Per County in {state}')


def crunch_deathrate_us(c_path,d_path,state, min_cases=100):
    '''
    graphs the death rate over time for state
    shows how we are handling pandemic
    hypothesis: should stay level or improve if new treatments found
    '''
    cx,cy = parse_time_us(c_path,state)
    cy = [i for i in cy if i>min_cases]
    cx = cx[-len(cy):]

    dx,dy = parse_time(d_path,state,6,12)
    dy = dy[-len(cy):]

    ry = [dy[i]/cy[i] for i in range(len(cy))]
    
    latest = ry[-1:][0]

    _, ax = plt.subplots()
    ax.set_title('Death Rate in {0}, currently {1:0.3f}'.format(state,latest))
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate')
    
    ax.plot(cx,ry,c=numpy.random.rand(3,),linewidth=2)
    plt.show()

def crunch_deathrate_global(c_path,d_path,country, min_cases=100):
    '''
    graphs the death rate over time for country
    shows how we are handling pandemic
    hypothesis: should stay level or improve if new treatments found
    '''
    cx,cy = parse_time_global(c_path,country)
    cy = [i for i in cy if i>min_cases]
    cx = cx[-len(cy):]

    dx,dy = parse_time_global(d_path,country)
    dy = dy[-len(cy):]

    ry = [dy[i]/cy[i] for i in range(len(cy))]
    
    latest = ry[-1:][0]
    
    _, ax = plt.subplots()
    ax.set_title('Death Rate in {0}, currently {1:0.3f}'.format(country,latest))
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate')
    
    ax.plot(cx,ry,c=numpy.random.rand(3,),linewidth=2)
    plt.show()

def crunch_basic_county(c_path,d_path,county,state,label, min_cases=100):
    '''
    Graphs confirmed and deaths for one county
    '''
    cx,cy = parse_time_county(c_path,county,state)
    cy = [i for i in cy if i>min_cases]
    cx = cx[-len(cy):]

    dx,dy = parse_time(d_path,county,5,12,value2=state,value2_idx=6)
    dx = dx[-len(cy):]
    dy = dy[-len(cy):]

    _, ax = plt.subplots()
    ax.set_title(f'Covid Data in {county}, {state}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number')
    
    ax.plot(cx,cy,label='Confirmed',c=numpy.random.rand(3,),linewidth=2)
    ax.plot(dx,dy,label='Deaths',c=numpy.random.rand(3,),linewidth=2)
    ax.legend()
    ax.set_yscale('log')
    plt.show()

def crunch_new_county(path,county,state,label):
    '''
    Shows trend over time for one county
    '''
    x,y = parse_time_county(path,county,state)
    graph_new(x,y,f"{county}, {state}",label)
    plt.show()

def crunch_new_global(path,country,label):
    '''
    Shows trend over time for various states
    '''
    x,y = parse_time_global(path,country)
    ax = graph_new(x,y,country,label)
    plt.show()

def crunch_trend_us(path,state,threshold=100):
    '''
    Shows the changes for each day of the week to see if there is a weekly trend
    '''
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

def crunch_deathratemd_us(c_path,d_path,important_states):
    '''
    Creates a markdown graph which shows the current deathrate by state
    '''
    cpersent = {}
    drates = {}
    for state in important_states:
        population = STATE_POPULATIONS[state]
        _,y = parse_time_us(c_path,state)
        _,dy = parse_time(d_path,state,6,12)
        latest = max(dy)/max(y)
        cpersent[state] = max(y)/population
        drates[state] = latest
    
    print('|State|Percent Infected|Death Rate|')
    print('|---|------:|------:|')
    for state,rate in sorted(drates.items(), key=(lambda item: item[1]), reverse=True):
        print('|{0}|{1:0.6f}|{2:0.6f}|'.format(state,cpersent[state],rate))
    print('\n')
    
def crunch_deathratemd_global(c_path,d_path):
    '''
    Creates a markdown graph which shows the current deathrate by country
    '''
    cpersent = {}
    drates = {}
    for country,population in COUNTRY_POPULATIONS.items():
        _,y = parse_time_global(c_path,country)
        _,dy = parse_time_global(d_path,country)
        latest = max(dy)/max(y)
        cpersent[country] = max(y)/population
        drates[country] = latest
    
    print('|Country|Percent Infected|Death Rate|')
    print('|---|------:|------:|')
    for country,rate in sorted(drates.items(), key=(lambda item: item[1]), reverse=True):
        print('|{0}|{1:0.6f}|{2:0.6f}|'.format(country,cpersent[country],rate))
    print('\n')

def crunch_new_us(path,states=[],min_cases=0):
    '''
    Shows the increase in cases since previous day for various states over time
    '''
    _, ax = plt.subplots()
    for state in states:
        _,y = parse_time_us(path,state)
        y = [v-y[i-1] for i, v in enumerate(y) if v>min_cases and i>min_cases]
        x = range(len(y))
        ax.plot(x,y,c=numpy.random.rand(3,),label=state)
    
    ax.set_xlabel('Days since at least {} cases in that state'.format(min_cases))
    ax.set_ylabel('New Cases since Previous Day')
    ax.set_title('New Cases Per Day for Various States')
    ax.legend()
    plt.show()       

def crunch_map_perpop_us(path):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        _,y = parse_time_us(path,state)
        y = [i/population for i in y if i>0]
        states[state] = max(y)*100 if len(y) > 0 else 0
    us_map(states,'Percentage of State Population Infected',formatter='{0:.2f}%')

def crunch_map_perpopnew_us(path,min_cases=0):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        x,y = parse_time_us(path,state)
        y = [v-y[i-1] for i, v in enumerate(y) if v>min_cases and i>min_cases]
        y = y[-7:]
        x = x[-7:]
        fromDate = min(x).strftime("%b %d, %Y")
        toDate = max(x).strftime("%b %d, %Y")
        states[state] = sum(y)/population*100 if len(y) > 0 else 0
    us_map(states,f'New Cases as Percent of Population\n{fromDate}-{toDate}',formatter='{0:.2f}%')


def crunch_fit_us(path,OUTPUT_BASE,check_states=[],min_days=5, min_cases=500):
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


def crunch_zero_global(path,min_cases=100):
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


def crunch_extrapolate_us(path,important_states,duration = 90):
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

