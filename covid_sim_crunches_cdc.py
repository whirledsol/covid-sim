"""
covid_sim_crunches.py
quick crunches of the data
@author: whirledsol
"""
import datetime,numpy,matplotlib
from covid_sim_base import *
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import itertools

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


def crunch_deathrate_states(c_path,d_path,state, min_cases=100):
    '''
    graphs the death rate over time for state
    shows how we are handling pandemic
    hypothesis: should stay level or improve if new treatments found
    '''
    cx,cy = parse_time_states(c_path,state)
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

def crunch_probability_county(path,county,state, avg_days=3, infection_period=20, max_people=20):
    '''
    using the last {days} days percentages,
    calculates the probability of succeeding transmission after interactions with n people
    uses binomial probability which is probably wrong
    '''
    d,n = parse_time_county(path,county,state)
    date = d[-1].strftime("%b %d, %Y")
    confirmed_now = numpy.mean(n[-avg_days:])
    confirmed_then = numpy.mean(n[len(n)-infection_period-avg_days: len(n) - infection_period])
    suseptible = confirmed_now - confirmed_then    
    location = f"{county}, {state}"
    population = COUNTY_POPULATIONS[location] if location in COUNTY_POPULATIONS else 1
    p = suseptible/population
    print(confirmed_now,'-',confirmed_then,'=',suseptible,'|',p)
    fact = lambda f: numpy.math.factorial(f)
    binomialp = numpy.vectorize(lambda n: (fact(n)/fact(n-1)) * p * (1-p)**(n-1))
    x = numpy.arange(1,max_people)  
    y = binomialp(x)

    _, ax = plt.subplots()
    ax.set_title(f'Probability of Infection for {county}, {state}\non {date}')
    ax.set_xlabel('Number of People')
    ax.set_ylabel('Probability')
    plt.plot(x,y)
    plt.show()

def crunch_new_county(path,county,state,label):
    '''
    Shows trend over time for one county
    '''
    x,y = parse_time_county(path,county,state)
    graph_new(x,y,f"{county}, {state}",label)
    plt.show()


def crunch_infectper_global(path, country, days=14):
    '''
    Shows trend over time for one county
    '''
    x,y = parse_time_global(path,country)
    population = COUNTRY_POPULATIONS[country] if country in COUNTRY_POPULATIONS else 1
    title =f"Percentage of Country Population Infected ({days} days)\n{country}"
    graph_sum(x,y,title,date_range=days, normalize=lambda x: x/population)
    plt.show()

def crunch_infectper_county(path,county,state,days=14):
    '''
    Shows trend over time for one county
    '''
    x,y = parse_time_county(path,county,state)
    location = f"{county}, {state}"
    population = COUNTY_POPULATIONS[location] if location in COUNTY_POPULATIONS else 1
    title =f"Percentage of County Population Infected ({days} days)\n{location}"
    graph_sum(x,y,title,date_range=days, normalize=lambda x: x/population)
    plt.show()

def crunch_new_global(path,country,label):
    '''
    Shows trend over time for various states
    '''
    x,y = parse_time_global(path,country)
    ax = graph_new(x,y,country,label)
    plt.show()

def crunch_trend_states(path,state,threshold=100):
    '''
    Shows the changes for each day of the week to see if there is a weekly trend
    '''
    x,y = parse_time_states(path,state)
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

def crunch_deathratemd_states(c_path,d_path,important_states):
    '''
    Creates a markdown graph which shows the current deathrate by state
    '''
    cpersent = {}
    drates = {}
    for state in important_states:
        population = STATE_POPULATIONS[state]
        _,y = parse_time_states(c_path,state)
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

def crunch_new_states(path,states=[],min_cases=0):
    '''
    Shows the increase in cases since previous day for various states over time
    '''
    _, ax = plt.subplots()
    for state in states:
        _,y = parse_time_states(path,state)
        y = [v-y[i-1] for i, v in enumerate(y) if v>min_cases and i>min_cases]
        x = range(len(y))
        ax.plot(x,y,c=numpy.random.rand(3,),label=state)
    
    ax.set_xlabel('Days since at least {} cases in that state'.format(min_cases))
    ax.set_ylabel('New Cases since Previous Day')
    ax.set_title('New Cases Per Day for Various States')
    ax.legend()
    plt.show()       

def crunch_map_perpop_states(path):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        _,y = parse_time_states(path,state)
        y = [i/population for i in y if i>0]
        states[state] = max(y)*100 if len(y) > 0 else 0
    us_map(states,'Percentage of State Population Infected',formatter='{0:.2f}%',text_top=len(states))

def crunch_map_perpopnew_states(path,min_cases=0):
    '''
    Shows percent of state affected on map. Redder is bad.
    '''
    states = {}
    for state,population in STATE_POPULATIONS.items():
        x,y = parse_time_states(path,state)
        y = [v-y[i-1] for i, v in enumerate(y) if v>min_cases and i>min_cases]
        y = y[-7:]
        x = x[-7:]
        fromDate = min(x).strftime("%b %d, %Y")
        toDate = max(x).strftime("%b %d, %Y")
        states[state] = sum(y)/population*100 if len(y) > 0 else 0
    us_map(states,f'New Cases as Percent of Population\n{fromDate}-{toDate}',formatter='{0:.2f}%')


def crunch_fit_states(path,OUTPUT_BASE,check_states=[],min_days=5, min_cases=500):
    '''
    Fits data to curve, saves the best fit, displays base on map. Redder means high rate.
    '''
    states = {}
    timestamp = datetime.datetime.now().strftime('%Y%m%d')
    outpath = os.path.join(OUTPUT_BASE,'states_bestfit_{}.csv'.format(timestamp))

    with open(outpath,'w') as f:
        for state,_ in list(STATE_POPULATIONS.items()):
            _,y = parse_time_states(path,state)
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


def crunch_zero_global(path,min_cases=100, population_threshold = 0, extreme_count  =None, keep=[]):
    '''
    Shows cases over time starting the day at least min_cases were hit for each country
    '''
    _, ax = plt.subplots()
    
    data = {}
    for country,population in COUNTRY_POPULATIONS.items():
        if population < population_threshold:
            continue
        _,y = parse_time_global(path,country)
        data[country] = [i/population for i in y if i>min_cases]
    
    if extreme_count is not None:
        data_sorted = sorted(data.items(),key=lambda x:x[1][-1:])
        data = {v[0]:v[1] for i,v in enumerate(data_sorted) if i < extreme_count or i >= len(data_sorted)-extreme_count or v[0] in keep}
        print('Graphing the following',[(k,v[-1:]) for k,v in data.items()])

    marker = itertools.cycle((',', '+', '.', 'o', '*')) 
    for country,y in data.items():
        x = range(len(y))
        _,formula = best_fit(x,y,expo,bounds=[0,0.9],label=country)
        label = '{}  {}'.format(country,formula)
        color = COUNTRY_COLORS[country] if country in COUNTRY_COLORS else numpy.random.rand(3,)
        ax.plot(x, y, c=color,marker=next(marker),label=label)

    ax.set_xlabel('Days since at least {} cases in that country'.format(min_cases))
    ax.set_ylabel('Percent Population Infected')
    ax.set_title('Percent of Country Infected After {} Cases'.format(min_cases))
    ax.legend()
    plt.show()


def crunch_extrapolate_states(path,important_states,duration = 90):
    '''
    Extrapolates the current data to fit func
    '''
    bounds = ([0.1,-1,12], [0.7,1,duration])

    _, ax = plt.subplots()
    for i,state in enumerate(important_states):
        x,y = parse_time_states(path,state)
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

