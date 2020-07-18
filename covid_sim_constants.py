"""
covid_sim_constants.py
data and values procured from the interwebs
@author: whirledsol
"""


COUNTRY_POPULATIONS = {"China":1433783686, "US":329064917, "United Kingdom":67530172, "Italy":60550075, "Canada":37411047, "Brazil":212516958}
COUNTRY_COLORS =  {'China':'orange','US':'blue','Brazil':'yellow','United Kingdom':'purple', 'Italy':'green', 'Canada':'red'}
STATE_POPULATIONS = {"California":39512223,"Texas":28995881,"Florida":21477737,"New York":19453561,"Pennsylvania":12801989,"Illinois":12671821,"Ohio":11689100,"Georgia":10617423,"North Carolina":10488084,"Michigan":9986857,"New Jersey":8882190,"Virginia":8535519,"Washington":7614893,"Arizona":7278717,"Massachusetts":6949503,"Tennessee":6833174,"Indiana":6732219,"Missouri":6137428,"Maryland":6045680,"Wisconsin":5822434,"Colorado":5758736,"Minnesota":5639632,"South Carolina":5148714,"Alabama":4903185,"Louisiana":4648794,"Kentucky":4467673,"Oregon":4217737,"Oklahoma":3956971,"Connecticut":3565287,"Utah":3205958,"Puerto Rico":3193694,"Iowa":3155070,"Nevada":3080156,"Arkansas":3017825,"Mississippi":2976149,"Kansas":2913314,"New Mexico":2096829,"Nebraska":1934408,"West Virginia":1792065,"Idaho":1787147,"Hawaii":1415872,"New Hampshire":1359711,"Maine":1344212,"Montana":1068778,"Rhode Island":1059361,"Delaware":973764,"South Dakota":884659,"North Dakota":762062,"Alaska":731545,"District of Columbia":705749,"Vermont":623989,"Wyoming":578759}

COUNTY_NAMES = {
    "Pennsylvania":['Adams','Allegheny','Armstrong','Beaver','Bedford','Berks','Blair','Bradford','Bucks','Butler','Cambria','Cameron','Carbon','Centre','Chester','Clarion','Clearfield','Clinton','Columbia','Crawford','Cumberland','Dauphin','Delaware','Elk','Erie','Fayette','Forest','Franklin','Fulton','Greene','Huntingdon','Indiana','Jefferson','Juniata','Lackawanna','Lancaster','Lawrence','Lebanon','Lehigh','Luzerne','Lycoming','McKean','Mercer','Mifflin','Monroe','Montgomery','Montour','Northampton','Northumberland','Perry','Philadelphia','Pike','Potter','Schuylkill','Snyder','Somerset','Sullivan','Susquehanna','Tioga','Union','Venango','Warren','Washington','Wayne','Westmoreland','Wyoming','York'],
    
    "New Jersey":['Atlantic','Bergen','Burlington','Camden','Cape May','Cumberland','Essex','Gloucester','Hudson','Hunterdon','Mercer','Middlesex','Monmouth','Morris','Ocean','Passaic','Salem','Somerset','Sussex','Union','Warren'],
    
    "New York":['Albany','Allegany','Bronx','Broome','Cattaraugus','Cayuga','Chautauqua','Chemung','Chenango','Clinton','Columbia','Cortland','Delaware','Dutchess','Erie','Essex','Franklin','Fulton','Genesee','Greene','Hamilton','Herkimer','Jefferson','Kings','Lewis','Livingston','Madison','Monroe','Montgomery','Nassau','New York','Niagara','Oneida','Onondaga','Ontario','Orange','Orleans','Oswego','Otsego','Putnam','Queens','Rensselaer','Richmond','Rockland','St. Lawrence','Saratoga','Schenectady','Schoharie','Schuyler','Seneca','Steuben','Suffolk','Sullivan','Tioga','Tompkins','Ulster','Warren','Washington','Wayne','Westchester','Wyoming','Yates'],

    "Massachusetts":['Middlesex','Worcester','Essex','Suffolk','Norfolk','Bristol','Plymouth','Hampden','Barnstable','Hampshire','Berkshire','Franklin','Dukes','Nantucket']
}

STATE_FIPS_CODES = {
    'Alabama':'01','Alaska':'02','Arizona':'04','Arkansas':'05','California':'06','Colorado':'08','Connecticut':'09','Delaware':'10','District of Columbia':'11','Florida':'12','Georgia':'13','Hawaii':'15','Idaho':'16','Illinois':'17','Indiana':'18','Iowa':'19','Kansas':'20','Kentucky':'21','Louisiana':'22','Maine':'23','Maryland':'24','Massachusetts':'25','Michigan':'26','Minnesota':'27','Mississippi':'28','Missouri':'29','Montana':'30','Nebraska':'31','Nevada':'32','New Hampshire':'33','New Jersey':'34','New Mexico':'35','New York':'36','North Carolina':'37','North Dakota':'38','Ohio':'39','Oklahoma':'40','Oregon':'41','Pennsylvania':'42','Rhode Island':'44','South Carolina':'45','South Dakota':'46','Tennessee':'47','Texas':'48','Utah':'49','Vermont':'50','Virginia':'51','Washington':'53','West Virginia':'54','Wisconsin':'55','Wyoming':'56'
}
