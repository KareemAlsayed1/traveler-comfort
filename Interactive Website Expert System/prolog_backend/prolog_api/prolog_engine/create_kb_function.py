import pandas as pd
import os
import csv
import copy
import math
import random
import os.path


def create_kb():
    if os.path.exists('prolog_api/prolog_engine/knowledge_base.txt'):
        with open('prolog_api/prolog_engine/knowledge_base.txt') as f:
            KB = f.read()
        return KB
    

    # Data Processing & Generation

    #Importing the European Captials
    european_capitals = []
    current_available_cities = []
    city_codes = {}
    with open('prolog_api/prolog_engine/cities_data/input_cities.csv') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)
        for row in reader:
            european_capitals.append(row[1])
            
    european_capitals.remove("Minsk")
    european_capitals.remove("Pristina")

    #Extracting Temperatures
    world_tempratures = pd.read_csv('prolog_api/prolog_engine/cities_data/city_temperature.csv')
    cities_available_data = world_tempratures['City'].unique()
    cities_average_temps = {}
    def convert_to_celsius(Fahrenheit):
        return (Fahrenheit - 32) * 5.0/9.0
    mon_number = {  1:'January',
                    2:'February',
                    3:'March',
                    4:'April',
                    5:'May', 
                    6:'June', 
                    7:'July',
                    8:'August',
                    9:'September',
                    10:'October',
                    11:'November',
                    12:'December'}

    empty_dict_months = {'January': None,
                        'February': None,
                        'March': None,
                        'April': None,
                        'May': None, 
                        'June': None, 
                        'July': None,
                        'August': None,
                        'September': None,
                        'October': None,
                        'November': None,
                        'December': None}

    # Filtering out cities with missing data
    for city in european_capitals:
        if city in cities_available_data:
            cities_average_temps[city] = copy.deepcopy(empty_dict_months)
            current_available_cities.append(city)

    ### Mapping Cities to Countries
    cities_mapping = "country(kiev, ukr).\n"
    world_cities = pd.read_csv('prolog_api/prolog_engine/cities_data/world_cities.csv')
    mapping_country_codes = {"Ukraine" : "UKR"}

    for city in current_available_cities:
        if city in world_cities.city_ascii.values:
            ava_data = world_cities[world_cities['city_ascii'] == city]
            ava_data = ava_data[ava_data["capital"].isin(["primary", "admin"])]
            if len(ava_data) == 1:
                cities_mapping += f"country({city.lower()}, {ava_data.loc[ava_data.index, 'iso3'].item().lower()}).\n"
                mapping_country_codes[ava_data.loc[ava_data.index, 'country'].item()] = ava_data.loc[ava_data.index, 'iso3'].item()
                city_codes[city.lower()] = ava_data.loc[ava_data.index, 'iso3'].item().lower()

    ### Purchasing Power Data
    purchasing_power_data = pd.read_csv('prolog_api/prolog_engine/cities_data/purchasing_power.csv')
    purchasing_power = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        if code in purchasing_power_data.Code.values:
            ava_data = purchasing_power_data[purchasing_power_data['Code'] == code]
            ava_data = ava_data[ava_data["Year"] == 2020]
            purchasing_power += f"purchasingpower({code.lower()}, {round(ava_data.loc[ava_data.index, 'PP'].item(), 3)}).\n"
    
    ### Freedom Index Data
    freedom_index_data = pd.read_csv('prolog_api/prolog_engine/cities_data/freedom_index.csv')
    freedom_index = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        if code in freedom_index_data.Country.values:
            ava_data = freedom_index_data[freedom_index_data['Country'] == code]
            ava_data = ava_data[ava_data["Indicator"] == "Freedom Status"]
            ava_data = ava_data["2021"].item()
            freedom_index += f"freedom({code.lower()}, {round (ava_data/3, 2)}).\n"
    
    ### Safety Index Data
    indices_data = pd.read_csv('prolog_api/prolog_engine/cities_data/indices_data.csv')
    safety_index_data = indices_data[indices_data["Code"] == "A.02"]
    safety_index_data = safety_index_data[safety_index_data["Attribute"] == "Value"]
    safety_index_data = safety_index_data[safety_index_data["Edition"] == 2019]
    safety_index = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        safety_index += f"safety({code.lower()}, {float(safety_index_data[code].item()) / 7}).\n"
    
    ### Health Care Index Data
    health_index_data = indices_data[indices_data["Code"] == "A.03"]
    health_index_data = health_index_data[health_index_data["Attribute"] == "Value"]
    health_index_data = health_index_data[health_index_data["Edition"] == 2019]
    health_index = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        health_index += f"healthcare({code.lower()}, {float(health_index_data[code].item()) / 7}).\n"
    
    ### ICT Index Data
    ict_index_data = indices_data[indices_data["Code"] == "A.05"]
    ict_index_data = ict_index_data[ict_index_data["Attribute"] == "Value"]
    ict_index_data = ict_index_data[ict_index_data["Edition"] == 2019]
    ict_index = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        ict_index += f"ict({code.lower()}, {ict_index_data[code].item()}).\n"
    
    ### Ground Infrastructure Data
    ginfra_index_data = indices_data[indices_data["Code"] == "C.11"]
    ginfra_index_data = ginfra_index_data[ginfra_index_data["Attribute"] == "Value"]
    ginfra_index_data = ginfra_index_data[ginfra_index_data["Edition"] == 2019]
    ginfra_index = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        ginfra_index += f"ginfra({code.lower()}, {ginfra_index_data[code].item()}).\n"
    
    ### Climate Data
    # Calculating data per month
    for city in cities_average_temps:
        years = world_tempratures.loc[(world_tempratures['City'] == city)]['Year'].unique()
        avg_months = {}
        for year in years:
            for month in range(1, 13):
                avg_temp = world_tempratures.loc[(world_tempratures['City'] == city)
                                                &(world_tempratures['Month'] == month)
                                                &(world_tempratures['Year'] == year)]['AvgTemperature'].mean()
                if avg_temp != -99 and not math.isnan(avg_temp):
                    if mon_number[month] in avg_months:
                        avg_months[mon_number[month]].append(avg_temp)
                    else:
                        avg_months[mon_number[month]] = [avg_temp]
        for month in avg_months:
            cities_average_temps[city][month] = convert_to_celsius(int(sum(avg_months[month])/len(avg_months[month])))
        avg_months = {}

    # Generate Prolog Scripts for temperatures
    tempratures_prolog = ""
    for city in cities_average_temps:
        for month in cities_average_temps[city]:
            if cities_average_temps[city][month] >= 23:
                tempratures_prolog += f"temperature({city.lower()}, high, {month.lower()})."
            elif cities_average_temps[city][month] >= 14:
                tempratures_prolog += f"temperature({city.lower()}, moderate, {month.lower()})."
            else:
                tempratures_prolog += f"temperature({city.lower()}, low, {month.lower()})."
            tempratures_prolog += '\n'
            
    # Creating dummy precipitation data for cities
    random.seed (15)
    precipitation_prolog = ""
    for city in cities_average_temps:
        random_pick = random.random()
        if random_pick > 0.5:
            precipitation_prolog += f"precipitation({city.lower()}, high)."
        else:
            precipitation_prolog += f"precipitation({city.lower()}, low)."
        precipitation_prolog += '\n'

    ### Generating options for Multivalued answers
    country_options = ""
    for country in mapping_country_codes:
        code = mapping_country_codes[country]
        country_options += f"currentcountry({code.lower()}):- askcurrentcountry({code.lower()}).\n"

    comfortimportance_options = ""
    for option in range(1,4):
        comfortimportance_options += f"comfortimportance({option}):- askcomfortimportance({option}).\n"

    freedomimportance_options = ""
    for option in range(1, 6):
        freedomimportance_options += f"freedomimportance({option}):- askfreedomimportance({option}).\n"

    ## Messages & Options (Legacy)
    msg_welcome = """

    __       __            __                                                    __ 
    |  \  _  |  \          |  \                                                  |  \
    | $$ / \ | $$  ______  | $$  _______   ______   ______ ____    ______        | $$
    | $$/  $\| $$ /      \ | $$ /       \ /      \ |      \    \  /      \       | $$
    | $$  $$$\ $$|  $$$$$$\| $$|  $$$$$$$|  $$$$$$\| $$$$$$\$$$$\|  $$$$$$\      | $$
    | $$ $$\$$\$$| $$    $$| $$| $$      | $$  | $$| $$ | $$ | $$| $$    $$       \$$
    | $$$$  \$$$$| $$$$$$$$| $$| $$_____ | $$__/ $$| $$ | $$ | $$| $$$$$$$$       __ 
    | $$$    \$$$ \$$     \| $$ \$$     \ \$$    $$| $$ | $$ | $$ \$$     \      |  \
    \$$      \$$  \$$$$$$$ \$$  \$$$$$$$  \$$$$$$  \$$  \$$  \$$  \$$$$$$$       \$$ \n

    This Program will help you to get a customized recommendation for city to have an amazing trip!
    """
    msg_rain = """

    , // ,,/ ,.// ,/ ,// / /, // ,/, /, // ,/,
    /, // ,/,_|_// ,/ ,, ,/, // ,/ /, //, /,/
    /, /,.-'   '-. ,// ////, // ,/,/, // ///
    , ,/,/         \ // ,,///, // ,/,/, // ,
    ,/ , ^^^^^|^^^^^ ,// ///  /,,/,/, ///, //
    / //     |  O    , // ,/, //, ///, // ,/
    ,/ ,,     J\/|\_ |+'(` , |) ^ ||\|||\|/` |
    /,/         |   || ,)// |\/-\|| ||| |\] .
    / /,,       /|    . ,  ///, . /, // ,//, /
    , /        \ \    ). //, ,( ,/,/, // ,/,

    Do you prefer rainy weather?

    1: I don't mind rain
    2: I prefer dry weather

    """

    msg_temperature = '''
                .     :     .
                .  :    |    :  .
                .  |   |   |  ,
                \  |     |  /
            .     ,-'"""`-.     .
                "- /  __ __  \ -"
                |==|  I  |==|
            - --- | _`--^--'_ | --- -
                |'`.     ,'`|
                _- \  "---"  / -_
            .     `-.___,-'     .
                /  |     |  \
                .'  |   |   |  `.
                :    |    :
                .     :     .
                
    What temperature levels do you prefer? 

    1: Cold Temperature (T < 15°C)
    2: Moderate Temperature (15°C < T < 25°C )
    3: High Temperature (25°C < T)
    '''

    msg_outdoor = """

                    \  |  /         ___________
        ____________  \ \_# /         |  ___      |       _________
    |            |  \  #/          | |   |     |      | = = = = |
    | |   |   |  |   \\#           | |`v'|     |      |         |
    |            |    \#  //       |  --- ___  |      | |  || | |
    | |   |   |  |     #_//        |     |   | |      |         |
    |            |  \\ #_/_______  |     |   | |      | |  || | |
    | |   |   |  |   \\# /_____/ \ |      ---  |      |         |
    |            |    \# |+ ++|  | |  |~~~~~~| |      | |  || | |
    |            |    \# |+ ++|  | |  |~~~~~~| |      | |  || | |
    ~~|    (~~~~~) |~~~~~#~| H  |_ |~|  | |||| | |~~~~~~|         |
    |    ( ||| ) |     # ~~~~~~    |  | |||| | |      | ||||||| |
    ~~~~~~~~~~~~~________/  /_____ |  | |||| | |      | ||||||| |
                                    ~~~~~~~~~~~~~      | ||||||| |
    How long are you planning to spend in outdoor areas?

    1: Little time
    2: Long time
    """

    msg_month = """
                                                        
                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                            
                ▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒                            
                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                            
                ░░░░░░░░██░░░░██░░░░██░░░░██░░                            
                ░░░░░░░░██░░██░░██░░████░░██░░                            
                ░░░░░░░░██░░██░░██░░████████░░                            
                ░░██░░░░██░░██████░░██░░████░░                            
                ░░░░████░░░░██░░██░░██░░░░██░░                            
                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                            
                ░░░░░░░░░░░░░░▒▒▒▒░░░░░░░░░░░░                            
                ░░░░░░░░░░░░▒▒▒▒▒▒░░░░░░░░░░░░                            
                ░░░░░░░░░░░░░░▒▒▒▒░░░░░░░░░░░░                            
                ░░░░░░░░░░░░░░▒▒▒▒░░░░░░░░░░░░                            
                ░░░░░░░░░░░░░░▒▒▒▒░░░░░░░░░░░░                            
                ░░░░░░░░░░░░░░▒▒▒▒░░░░░░░░░░░░                            
                ░░░░░░░░░░░░▒▒▒▒▒▒▒▒░░░░░░░░░░                            
                ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░                            
                                                                                            
    What month are you planning to travel?

    please enter a month between 1 - 12
    """

    msg_budget = """
    On average, how much more are you willing to spend (in your trip) relative to where you live?

    1: Similar budget or cheaper
    2: Less than double of what I spend on average
    3: Less than triple of what I spend on average
    4: Flexible
    """

    msg_family = """
    Are you traveling with a Family or alone? 

    1: Alone
    2: With a Family
    """

    msg_kids = """
    Are there kids traveling with you?

    1: Yes
    2: No
    """

    msg_gender = """
    What is your gender?

    1: Female
    2: Male
    """

    msg_age = """
    What age group do you belong to? 

    1: 18 - 34
    2: 35 - 44
    3: 45 - 54
    4: 55 - 64
    5: 65+
    """

    msg_chroniccondition = """
    Do you have any chronic conditions that might need medical attention during your Trip?

    1: Yes
    2: No
    """

    msg_comfortimportance = """
    Some people prefer to explore new cultures and countries, regardless of the level of comfort. What is the level of comfort (in terms of infrastructure) that you are looking (minimum) for in your trip compared where you live ? 

    1: I care about adventure rather than a comfortable trip
    2: Slightly less comfortable
    3: More comfortable or similar level 
    """

    msg_currentcountry = """
    Where are you currently living?

    Currently, we support the following list of countries """ + str(list(mapping_country_codes.keys()))

    msg_freedomimportance = """
    On scale from 1 to 5, how much do you care about the civil and political freedom of your destination country?

    Please give a number between 1 and 5, where
    1 --> I don't really care about that factor
    5 --> That's an important factor to me 
    """
    options_budget = {
        1: "affordable",
        2: "double",
        3: "triple",
        4: "any"
    }

    ### Askables
    askables = """

preferrain(X) :- ask(preferrain, X).
prefertemperature(X) :- ask(prefertemperature, X).
stayoutdoors(X) :- ask(stayoutdoors, X).
travelmonth(X) :- ask(travelmonth, X).
budget(X) :- ask(budget, X).
gender(X) :- ask(gender, X).
family(X) :- ask(family, X).
kids(X) :- ask(kids, X).
age(X) :- ask(age, X).
chroniccondition(X) :- ask(chroniccondition, X).
askcurrentcountry(X) :- ask(askcurrentcountry, X).
askcomfortimportance(X) :- ask(askcomfortimportance, X).
askfreedomimportance(X) :- ask(askfreedomimportance, X).
    """

    #### Asking clauses
    asking_clauses = """

multivalued(none).



ask(A, V):-
known(yes, A, V), % succeed if true
!.	% stop looking

ask(A, V):-
known(_, A, V), % fail if false
!, 
fail.

% If not multivalued, and already known, don't ask again for a different value.
ask(A, V):-
\+multivalued(A),
known(yes, A, V2),
V \== V2,
!.

ask(A, V):-
read_py(A,V,Y), % get the answer
asserta(known(Y, A, V)), % remember it
Y == yes. % succeed or fail

ask(A, V):-
not multivalued(A),
known(yes, A, V2),
V \== V2,
!,
fail.
    """

    ### Climate
    #### Outdoor 
    outdoor_rules = """

suitable(C, outdoor, 1) :- 
    stayoutdoors(short); 
    (precipitation(C, high), preferrain(any));
    precipitation(C, low).
suitable(C, outdoor, 0) :- 
    stayoutdoors(long),
    precipitation(C, high), preferrain(low).  
    """

    #### Temperature
    temperature_rules = """

suitable(C, temperature, 1) :- temperature(C, L, M), prefertemperature(L), travelmonth(M).
suitable(C, temperature, 0.5) :- temperature(C, high, M), prefertemperature(moderate), travelmonth(M).
suitable(C, temperature, 0.5) :- temperature(C, low, M), prefertemperature(moderate), travelmonth(M).
suitable(C, temperature, 0.5) :- temperature(C, moderate, M), prefertemperature(high), travelmonth(M).
suitable(C, temperature, 0) :- temperature(C, low, M), prefertemperature(high), travelmonth(M).
suitable(C, temperature, 0.5) :- temperature(C, moderate, M), prefertemperature(low), travelmonth(M).
suitable(C, temperature, 0) :- temperature(C, high, M), prefertemperature(low), travelmonth(M).
    """

    #### General Climate Rule
    climate_rule = """

suitable(C, climate, P) :- suitable(C, temperature, T),
                        suitable(C, outdoor, O), 
                        outdoorimporantance(Oi),
                        tempratureimportance(Ti),
                        totalweather(To),
                        P is ((Ti * T) + (Oi * O)) / To.
    """

    ### Infrastructure & Accessibility
    #### ICT
    ict_rules = """

ictvalue(C, P):- country(C, T),
                currentcountry(H), 
                ict(T, TV), 
                ict(H, HV),
                1 > TV/HV,
                P is TV/HV.

ictvalue(C, 1):- country(C, T),
                currentcountry(H), 
                ict(T, TV), 
                ict(H, HV),
                1 =< TV/HV.

suitable(C, ict, Ptotal):- ictvalue(C, P), 
                        comfortimportance(Pi), 
                        Ptotal is 1 - ((1 - P)/(4 - Pi)).
    """

    #### Ground Infrastructure

    ground_infra_rules = """
ginfravalue(C, P):- country(C, T),
                    currentcountry(H), 
                    ginfra(T, TV), 
                    ginfra(H, HV),
                    1 > TV/HV,
                    P is TV/HV.

ginfravalue(C, 1):- country(C, T),
                    currentcountry(H), 
                    ginfra(T, TV), 
                    ginfra(H, HV),
                    1 =< TV/HV.
                    
suitable(C, ginfra, Ptotal):- ginfravalue(C, P),
                            comfortimportance(Pi),
                            Ptotal is 1 - ((1 - P)/(4 - Pi)).
    """

    #### Health Care System
    health_rules = """

healthimportance(5):- chroniccondition(true); kids(true); age(5).
healthimportance(1):- age(1), kids(false), chroniccondition(false).
healthimportance(2.5):- age(2), kids(false), chroniccondition(false).
healthimportance(3):- age(3), kids(false), chroniccondition(false).
healthimportance(4.5):- age(4), kids(false), chroniccondition(false).

suitable(C, health, Ph):-  country(C, T),
                        healthcare(T, P), 
                        healthimportance(Pi),
                        Ph is 1 - ((1 - P)/(6 - Pi)).
    """

    #### Infra General Rule
    infra_rule = """

suitable(C, infra, Ptotal):- suitable(C, health, P1),
                            suitable(C, ginfra, P2),
                            suitable(C, ict, P3),
                            Ptotal is P1*P2*P3.
    """

    ### Political & Economic consideration
    #### Purchasing Power
    purchasing_power_rules = """

affordabilityvalue(C, P):- country(C, T),
                    currentcountry(H), 
                    purchasingpower(T, TV), 
                    purchasingpower(H, HV),
                    P is TV/HV.

affordability(C, affordable):- affordabilityvalue(C, P), P =< 1.
affordability(C, double):- affordabilityvalue(C, P), P =< 2, 1 < P.
affordability(C, triple):- affordabilityvalue(C, P), P =< 3, 2 < P.
affordability(C, expensive):- affordabilityvalue(C, P), P > 3.


suitable(C, budget, 0.25):- budget(affordable), affordability(C, expensive).
suitable(C, budget, 0.5):- budget(double), affordability(C, expensive).
suitable(C, budget, 0.5):- budget(affordable), affordability(C, triple).
suitable(C, budget, 0.75):- budget(affordable), affordability(C, double).
suitable(C, budget, 0.75):- budget(double), affordability(C, triple).
suitable(C, budget, 0.75):- budget(triple), affordability(C, expensive).
suitable(C, budget, 1):- budget(any);
                        budget(S), affordability(C, S); 
                        budget(double), affordability(C, affordable); 
                        budget(triple), affordability(C, affordable); 
                        budget(triple), affordability(C, double).
    """

    #### Safety Index
    safety_rules = """

safetyimportance(2.5) :- family(true), kids(true).
safetyimportance(2) :- family(true).
safetyimportance(1.5) :- gender(female).
safetyimportance(1) :- gender(male).

suitable(C, safety, Ps):- country(C, T),
                        safety(T, P),
                        safetyimportance(Pi),
                        Ps is 1 - ((1 - P)/(3.5 - Pi)).
    """

    #### Freedom Index
    freedom_rules = """

suitable(C, freedom, Pf):- country(C, T),
                        freedom(T, P), 
                        freedomimportance(Pi),
                        Pf is 1 - ((1 - P)/(6 - Pi)).
    """

    #### General PE rule
    pe_rule = """

suitable(C, pe, Ptotal) :- suitable(C, budget, P1),
                        suitable(C, safety, P2),
                        suitable(C, freedom, P3),
                        Ptotal is P1*P2*P3.
    """

    ### Overall City Assessment
    general_rule = """

recommend(C, Ptotal) :- suitable(C, climate, P1),
                        suitable(C, pe, P2),
                        suitable(C, infra, P3),
                        Ptotal is (P1 + P2 + P3)/3.
    """
    # The master Knowledge Base text
    KB = """
%  Tell prolog that known/3 will be added later by asserta
:- dynamic known/3.

% Mapping Cities to countries
"""+ cities_mapping +"""
% Precipitation Information\n 
""" + precipitation_prolog + """
% Temperature Information\n 
"""+tempratures_prolog +"""
% Purchasing Power Information
"""+ purchasing_power +"""
% Safety Index Data
%% Metrics Between one and zero
"""+ safety_index +"""
% Freedom Index Data
%% Metrics between one and zero
"""+ freedom_index +"""
% Healthcare Index Data
"""+ health_index +"""
% ICT Index Data
"""+ ict_index +"""
% Ground Infrastructure Data
"""+ ginfra_index +"""

% The code below implements the prompting to ask the user:
"""+ askables +"""

% Current Country Options:
"""+ country_options +"""

% Comfort Level Importance
"""+ comfortimportance_options +"""

% Freedom Level Importance
"""+ freedomimportance_options +"""

% Hypothitical City 
precipitation(wonder, high). 
temperature(wonder, high, january).
country(wonder, land).
purchasingpower(land, 0.2).

% Importance Rating
outdoorimporantance(1).
tempratureimportance(3).
totalweather(T) :- outdoorimporantance(V1),
                tempratureimportance(V2),
                T is V1 + V2.

% Dynamic Model
%% Outdoor
"""+ outdoor_rules +"""   
%% Temperature
"""+ temperature_rules +"""
%% Overall Climate Assessments
"""+ climate_rule +"""
% Infrastructure & Accessibility
%% ICT
"""+ ict_rules +"""                       
%% Ground Infrastructure
"""+ ground_infra_rules +"""
%% Health Care System
"""+ health_rules +"""
"""+ infra_rule +"""
% Political & Economic consideration
%% Purchasing Power
"""+ purchasing_power_rules +"""
%% Safety Index
%% Safety Importance is between 1 and 3 compared to the other factors
"""+ safety_rules +"""
% Freedom Index
"""+ freedom_rules +"""
% Overall Political & Economic Assessment
% suitable(C, pe, Ptotal) :- suitable(C, budget, P1),
%                           suitable(C, safety, P2),
%                           safetyimportance(Pi2),
%                           Ptotal is ((Pi2*P2 + P1)/(1+Pi2)).
"""+ pe_rule +"""

% Overall City Assessments
"""+ general_rule +"""

% Asking clauses
"""+ asking_clauses +""" 

    """
    # Generating files to cache the date processing
    with open('prolog_api/prolog_engine/knowledge_base.txt', 'w') as f:
        f.write(KB)
    
    with open('prolog_api/prolog_engine/current_available_cities.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows([current_available_cities])
    
    with open('prolog_api/prolog_engine/country_codes.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows([list(mapping_country_codes.values())])
    
    with open('prolog_api/prolog_engine/country_names.csv', 'w') as f:
        write = csv.writer(f)
        write.writerows([list(mapping_country_codes.keys())])
    
    with open('prolog_api/prolog_engine/cities_codes.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(city_codes.keys())
        write.writerow(city_codes.values())
    
    return KB