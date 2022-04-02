from prolog_api.prolog_engine.create_kb_function import create_kb
from pyswip.prolog import Prolog
from pyswip.easy import *
import tempfile
import csv

# User profile variables
kids_respone = None
prefer_rain_response = None
prefer_temp_response = None
stay_outdoor_response = None
month_response = None 
budget_response = None
family_respone = None
gender_response = None
age_response = None
chroniccondition_response = None
comfortimportance_response = None
currentcountry_response = None
freedomimportance_response = None
empty_vars = {
    "kids_respone": None,
    "prefer_rain_response": None,
    "prefer_temp_response": None,
    "stay_outdoor_response": None,
    "month_response": None,
    "budget_response": None,
    "family_respone": None,
    "gender_response": None,
    "age_response": None,
    "chroniccondition_response": None,
    "comfortimportance_response": None,
    "currentcountry_response": None,
    "freedomimportance_response": None
}

# Converting month numbers to names
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

# Saving the options 
options_budget = {
        1: "affordable",
        2: "double",
        3: "triple",
        4: "any"
    }

# Function to run the Prolog Engine and call the knowledge base creation
def run_prolog(parameters):
    KB = create_kb()
    prolog = Prolog() # Global handle to interpreter
    def update_variables():
        global currentcountry_response
        globals().update(empty_vars)
        globals().update(parameters)
        if currentcountry_response != None:
            currentcountry_response = currentcountry_response.lower()
    update_variables()

    output = None
    data_needed = False
    
    retractall = Functor("retractall")
    known = Functor("known",3)
    
    def ask(requested_data):
        """
        Asks the user a normal 'yes or no' question or a
        'menu' style question. Returns the response of the user.
        
        message: a string containing the message to display to user
        key_words: a list containing the responses that are allowed
        menu: boolean indicating if question is a menu question
        """
        nonlocal data_needed
        nonlocal output

        data_needed = True
        output = requested_data
        return output


    # Define foreign functions for getting user input and writing to the screen
    def write_py(X):
        print(str(X))
        sys.stdout.flush()
        return True

    def read_py(A,V,Y):
        global kids_respone
        if data_needed:
            # Skipping the steps
            return False
        elif isinstance(Y, Variable):
            if str(A) == "stayoutdoors":
                if stay_outdoor_response is None:
                    ask("stay_outdoor_response")
                    return False
                if str(V) == 'short' and stay_outdoor_response == '1':
                    Y.unify('yes')
                elif str(V) == 'long' and stay_outdoor_response == '2':
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "preferrain":
                if prefer_rain_response is None:
                    ask("prefer_rain_response")
                    return False
                if str(V) == 'any' and prefer_rain_response == '1':
                    Y.unify('yes') 
                elif str(V) == 'low' and prefer_rain_response == '2':
                    Y.unify('yes')
                else: 
                    Y.unify('no')
            elif str(A) == "prefertemperature":
                if prefer_temp_response is None:
                    ask("prefer_temp_response")
                    return False
                if str(V) == 'low' and prefer_temp_response == '1':
                    Y.unify('yes') 
                elif str(V) == 'moderate' and prefer_temp_response == '2':
                    Y.unify('yes')
                elif str(V) == 'high' and prefer_temp_response == '3':
                    Y.unify('yes')
                else: 
                    Y.unify('no')
            elif str(A) == "travelmonth":
                if month_response is None:
                    ask("month_response")
                    return False
                if mon_number[int(month_response)].lower() == str(V):
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "budget":
                if budget_response is None:
                    ask("budget_response")
                    return False
                if options_budget[int(budget_response)].lower() == str(V):
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "family":
                if family_respone is None:
                    ask("family_respone")
                    return False
                if family_respone == '1':
                    kids_respone = '2'
                    pass
                if family_respone == '1' and  str(V) == 'false':
                    Y.unify('yes')
                elif family_respone == '2' and  str(V) == 'true':
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "kids":
                if kids_respone is None:
                    ask("kids_respone")
                    return False
                if kids_respone == '1' and  str(V) == 'true':
                    Y.unify('yes')
                elif kids_respone == '2' and  str(V) == 'false':
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "gender":
                if gender_response is None:
                    ask("gender_response")
                    return False
                if gender_response == '1' and  str(V) == 'female':
                    Y.unify('yes')
                elif gender_response == '2' and  str(V) == 'male':
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "age":
                if age_response is None:
                    ask("age_response")
                    return False
                if age_response == str(V):
                    Y.unify('yes')
                else: 
                    Y.unify('no')
            elif str(A) == "chroniccondition":
                if chroniccondition_response is None:
                    ask("chroniccondition_response")
                    return False
                if chroniccondition_response == '1' and str(V) == "true":
                    Y.unify('yes')
                elif chroniccondition_response == '2' and str(V) == "false":
                    Y.unify('yes')
                else: 
                    Y.unify('no')
            elif str(A) == "askcurrentcountry":
                if currentcountry_response == None:
                    ask("currentcountry_response")
                    return False
                if currentcountry_response == str(V):
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "askcomfortimportance":
                if comfortimportance_response is None:
                    ask("comfortimportance_response")
                    return False
                if comfortimportance_response == str(V):
                    Y.unify('yes')
                else:
                    Y.unify('no')
            elif str(A) == "askfreedomimportance":
                if freedomimportance_response is None:
                    ask("freedomimportance_response")
                    return False
                if freedomimportance_response == str(V):
                    Y.unify('yes')
                else:
                    Y.unify('no')
            return True 
        else:
            return False
    
    # Legacy code
    def ask_destination_cities():
        question = """
        Please tell us the cities that you are considering for your trip (up to five cities). Separate your input with a comma, for example, "Tirana, Paris". 

        Currently our system supports the following cities: """ + "\n\n"
        response = input(question).replace(" ", "").lower()
        return response.split(',')

    def present_results(outcome_data, overall_results):
        overall_results = sorted(overall_results)[::-1]
        print("\nQuick order of cities based on your preferences:\n")
        for indx, city in enumerate(overall_results):
            print(f"{indx + 1}. {city[1].title()}")

    write_py.arity = 1
    read_py.arity = 3

    registerForeign(read_py)
    registerForeign(write_py)

    # Create a temporary file with the KB in it
    (FD, name) = tempfile.mkstemp(suffix='.pl', text = "True")
    with os.fdopen(FD, "w") as text_file:
        text_file.write(KB)
    prolog.consult(name) # open the KB for consulting
    os.unlink(name) # Remove the temporary file

    with open('prolog_api/prolog_engine/current_available_cities.csv', 'r') as csvfile:
        current_available_cities = list(csv.reader(csvfile))[0]

    with open('prolog_api/prolog_engine/cities_codes.csv', 'r') as csvfile:
        rows = list(csv.reader(csvfile))
        zipped_data  = zip(rows[0], rows[1])
        cities_codes = dict(zipped_data)

    #Uncomment if you want to get analysis for specific set of cities
    # cities_destinations = ask_destination_cities()
    cities_destinations = current_available_cities
    analysis_outcome = {}
    overall_results = []

    # Assess the avaliable cities in the dataset
    for city_choice in cities_destinations:
        city_choice = city_choice.lower()
        go_to = [s for s in prolog.query(f"recommend({city_choice}, Proability).", maxresult=1)]
        if data_needed:
            globals().update(empty_vars)
            return output
        climate = [s for s in prolog.query(f"suitable({city_choice}, climate, C).", maxresult=1)]
        pe = [s for s in prolog.query(f"suitable({city_choice}, pe, P).", maxresult=1)]
        infra = [s for s in prolog.query(f"suitable({city_choice}, infra, P).", maxresult=1)]
        
        if (len(go_to) != 0):
            confidence = round(go_to[0]['Proability']*100, 2)
            overall_results.append([confidence ,city_choice])
            analysis_outcome[cities_codes[city_choice].upper()] = {
                "Overall" : confidence,
                "City_name" : city_choice,
                "Climate" : round(climate[0]['C']*100, 2),
                "PE" : round(pe[0]['P']*100, 2),
                "Infra" : round(infra[0]['P']*100,2)
            }
        else:
            print("There are no cities")
    
    present_results(analysis_outcome, overall_results)
    globals().update(empty_vars)
    return ([analysis_outcome, overall_results])