"""
covid_sim_constants.py
data and values procured from the interwebs
@author: whirledsol
"""


COUNTRY_POPULATIONS = {
    'US':329064917,
    'Canada':37411047,
    'Brazil':212516958,
    'Russia': 145934462,
    'Germany': 83783942,
    'United Kingdom': 67886011,
    'France': 65273511,
    'Italy': 60461826,
    'Spain': 46754778,
    'Ukraine': 43733762,
    'Poland': 37846611,
    'Romania': 19237691,
    'Netherlands': 17134872,
    'Belgium': 11589623,
    'Czechia': 10708981,
    'Greece': 10423054,
    'Portugal': 10196709,
    'Sweden': 10099265,
    'Hungary': 9660351,
    'Belarus': 9449323,
    'Austria': 9006398,
    'Serbia': 8737371,
    'Switzerland': 8654622,
    'Bulgaria': 6948445,
    'Denmark': 5792202,
    'Finland': 5540720,
    'Slovakia': 5459642,
    'Norway': 5421241,
    'Ireland': 4937786,
    'Croatia': 4105267,
    'Moldova': 4033963,
    'Bosnia and Herzegovina': 3280819,
    'Albania': 2877797,
    'Lithuania': 2722289,
    'North Macedonia': 2083374,
    'Slovenia': 2078938,
    'Latvia': 1886198,
    'Estonia': 1326535,
    'Montenegro': 628066,
    'Luxembourg': 625978,
    'Malta': 441543,
    'Iceland': 341243,
    'Channel Islands': 173863,
    'Isle of Man': 85033,
    'Andorra': 77265,
    'Faeroe Islands': 48863,
    'Monaco': 39242,
    'Liechtenstein': 38128,
    'San Marino': 33931,
    'Gibraltar': 33691,
    'Holy See': 801
    }
COUNTRY_COLORS =  {'China':'orange','US':'blue','Brazil':'yellow','United Kingdom':'purple', 'Italy':'green', 'Canada':'red'}
STATE_POPULATIONS = {"California":39512223,"Texas":28995881,"Florida":21477737,"New York":19453561,"Pennsylvania":12801989,"Illinois":12671821,"Ohio":11689100,"Georgia":10617423,"North Carolina":10488084,"Michigan":9986857,"New Jersey":8882190,"Virginia":8535519,"Washington":7614893,"Arizona":7278717,"Massachusetts":6949503,"Tennessee":6833174,"Indiana":6732219,"Missouri":6137428,"Maryland":6045680,"Wisconsin":5822434,"Colorado":5758736,"Minnesota":5639632,"South Carolina":5148714,"Alabama":4903185,"Louisiana":4648794,"Kentucky":4467673,"Oregon":4217737,"Oklahoma":3956971,"Connecticut":3565287,"Utah":3205958,"Puerto Rico":3193694,"Iowa":3155070,"Nevada":3080156,"Arkansas":3017825,"Mississippi":2976149,"Kansas":2913314,"New Mexico":2096829,"Nebraska":1934408,"West Virginia":1792065,"Idaho":1787147,"Hawaii":1415872,"New Hampshire":1359711,"Maine":1344212,"Montana":1068778,"Rhode Island":1059361,"Delaware":973764,"South Dakota":884659,"North Dakota":762062,"Alaska":731545,"District of Columbia":705749,"Vermont":623989,"Wyoming":578759}
COUNTY_POPULATIONS = {"Bucks, Pennsylvania":626370, "Mercer, New Jersey":367430, "Middlesex, New Jersey":825062 }
COUNTY_NAMES = {
    "Pennsylvania":['Adams','Allegheny','Armstrong','Beaver','Bedford','Berks','Blair','Bradford','Bucks','Butler','Cambria','Cameron','Carbon','Centre','Chester','Clarion','Clearfield','Clinton','Columbia','Crawford','Cumberland','Dauphin','Delaware','Elk','Erie','Fayette','Forest','Franklin','Fulton','Greene','Huntingdon','Indiana','Jefferson','Juniata','Lackawanna','Lancaster','Lawrence','Lebanon','Lehigh','Luzerne','Lycoming','McKean','Mercer','Mifflin','Monroe','Montgomery','Montour','Northampton','Northumberland','Perry','Philadelphia','Pike','Potter','Schuylkill','Snyder','Somerset','Sullivan','Susquehanna','Tioga','Union','Venango','Warren','Washington','Wayne','Westmoreland','Wyoming','York'],
    
    "New Jersey":['Atlantic','Bergen','Burlington','Camden','Cape May','Cumberland','Essex','Gloucester','Hudson','Hunterdon','Mercer','Middlesex','Monmouth','Morris','Ocean','Passaic','Salem','Somerset','Sussex','Union','Warren'],
    
    "New York":['Albany','Allegany','Bronx','Broome','Cattaraugus','Cayuga','Chautauqua','Chemung','Chenango','Clinton','Columbia','Cortland','Delaware','Dutchess','Erie','Essex','Franklin','Fulton','Genesee','Greene','Hamilton','Herkimer','Jefferson','Kings','Lewis','Livingston','Madison','Monroe','Montgomery','Nassau','New York','Niagara','Oneida','Onondaga','Ontario','Orange','Orleans','Oswego','Otsego','Putnam','Queens','Rensselaer','Richmond','Rockland','St. Lawrence','Saratoga','Schenectady','Schoharie','Schuyler','Seneca','Steuben','Suffolk','Sullivan','Tioga','Tompkins','Ulster','Warren','Washington','Wayne','Westchester','Wyoming','Yates'],

    "Massachusetts":['Middlesex','Worcester','Essex','Suffolk','Norfolk','Bristol','Plymouth','Hampden','Barnstable','Hampshire','Berkshire','Franklin','Dukes','Nantucket'],
    
    'Texas': ['Anderson','Andrews','Angelina','Aransas','Archer','Armstrong','Atascosa','Austin','Bailey','Bandera','Bastrop','Baylor','Bee','Bell','Bexar','Blanco','Borden','Bosque','Bowie','Brazoria','Brazos','Brewster','Briscoe','Brooks','Brown','Burleson','Burnet','Caldwell','Calhoun','Callahan','Cameron','Camp','Carson','Cass','Castro','Chambers','Cherokee','Childress','Clay','Cochran','Coke','Coleman','Collin','Collingsworth','Colorado','Comal','Comanche','Concho','Cooke','Coryell','Cottle','Crane','Crockett','Crosby','Culberson','Dallam','Dallas','Dawson','Deaf Smith','Delta','Denton','DeWitt','Dickens','Dimmit','Donley','Duval','Eastland','Ector','Edwards','Ellis','El Paso','Erath','Falls','Fannin','Fayette','Fisher','Floyd','Foard','Fort Bend','Franklin','Freestone','Frio','Gaines','Galveston','Garza','Gillespie','Glasscock','Goliad','Gonzales','Gray','Grayson','Gregg','Grimes','Guadalupe','Hale','Hall','Hamilton','Hansford','Hardeman','Hardin','Harris','Harrison','Hartley','Haskell','Hays','Hemphill','Henderson','Hidalgo','Hill','Hockley','Hood','Hopkins','Houston','Howard','Hudspeth','Hunt','Hutchinson','Irion','Jack','Jackson','Jasper','Jeff Davis','Jefferson','Jim Hogg','Jim Wells','Johnson','Jones','Karnes','Kaufman','Kendall','Kenedy','Kent','Kerr','Kimble','King','Kinney','Kleberg','Knox','Lamar','Lamb','Lampasas','La Salle','Lavaca','Lee','Leon','Liberty','Limestone','Lipscomb','Live Oak','Llano','Loving','Reeves','Lubbock','Lynn','McCulloch','McLennan','McMullen','Madison','Marion','Martin','Mason','Matagorda','Maverick','Medina','Menard','Midland','Milam','Mills','Mitchell','Montague','Montgomery','Moore','Morris','Motley','Nacogdoches','Navarro','Newton','Nolan','Nueces','Ochiltree','Oldham','Orange','Palo Pinto','Panola','Parker','Parmer','Pecos','Polk','Potter','Presidio','Rains','Randall','Reagan','Real','Red River','Reeves','Refugio','Roberts','Robertson','Rockwall','Runnels','Rusk','Sabine','San Augustine','San Jacinto','San Patricio','San Saba','Schleicher','Scurry','Shackelford','Shelby','Sherman','Smith','Somervell','Starr','Stephens','Sterling','Stonewall','Sutton','Swisher','Tarrant','Taylor','Terrell','Terry','Throckmorton','Titus','Tom Green','Travis','Trinity','Tyler','Upshur','Upton','Uvalde','Val Verde','Van Zandt','Victoria','Walker','Waller','Ward','Washington','Webb','Wharton','Wheeler','Wichita','Wilbarger','Willacy','Williamson','Wilson','Winkler','Wise','Wood','Yoakum','Young','Zapata','Zavala']
}

STATE_FIPS_CODES = {
    'Alabama':'01','Alaska':'02','Arizona':'04','Arkansas':'05','California':'06','Colorado':'08','Connecticut':'09','Delaware':'10','District of Columbia':'11','Florida':'12','Georgia':'13','Hawaii':'15','Idaho':'16','Illinois':'17','Indiana':'18','Iowa':'19','Kansas':'20','Kentucky':'21','Louisiana':'22','Maine':'23','Maryland':'24','Massachusetts':'25','Michigan':'26','Minnesota':'27','Mississippi':'28','Missouri':'29','Montana':'30','Nebraska':'31','Nevada':'32','New Hampshire':'33','New Jersey':'34','New Mexico':'35','New York':'36','North Carolina':'37','North Dakota':'38','Ohio':'39','Oklahoma':'40','Oregon':'41','Pennsylvania':'42','Rhode Island':'44','South Carolina':'45','South Dakota':'46','Tennessee':'47','Texas':'48','Utah':'49','Vermont':'50','Virginia':'51','Washington':'53','West Virginia':'54','Wisconsin':'55','Wyoming':'56'
}


STATE_ABBREV = {'Alabama':'AL','Alaska':'AK','Arizona':'AZ','Arkansas':'AR','California':'CA','Colorado':'CO','Connecticut':'CT','Delaware':'DE','Florida':'FL','Georgia':'GA','Hawaii':'HI','Idaho':'ID','Illinois':'IL','Indiana':'IN','Iowa':'IA','Kansas':'KS','Kentucky':'KY','Louisiana':'LA','Maine':'ME','Maryland':'MD','Massachusetts':'MA','Michigan':'MI','Minnesota':'MN','Mississippi':'MS','Missouri':'MO','Montana':'MT','Nebraska':'NE','Nevada':'NV','New Hampshire':'NH','New Jersey':'NJ','New Mexico':'NM','New York':'NY','North Carolina':'NC','North Dakota':'ND','Ohio':'OH','Oklahoma':'OK','Oregon':'OR','Pennsylvania':'PA','Rhode Island':'RI','South Carolina':'SC','South Dakota':'SD','Tennessee':'TN','Texas':'TX','Utah':'UT','Vermont':'VT','Virginia':'VA','Washington':'WA','West Virginia':'WV','Wisconsin':'WI','Wyoming':'WY'}