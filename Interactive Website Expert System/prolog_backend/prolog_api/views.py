from numpy import delete
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from prolog_api.prolog_engine import run_prolog
from multiprocessing import Process
from django_q.tasks import async_task, result
import csv


month_response_options = []
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

for month in mon_number:
    month_response_options.append({"answerText": mon_number[month], "value": str(month)})

with open('prolog_api/prolog_engine/country_names.csv', 'r') as csvfile:
        country_names = list(csv.reader(csvfile))[0]

with open('prolog_api/prolog_engine/country_codes.csv', 'r') as csvfile:
        country_codes = list(csv.reader(csvfile))[0]

currentcountry_response_options = []
for indx in range(len(country_names)):
    currentcountry_response_options.append({'answerText': country_names[indx], 'value': country_codes[indx]})


question = {
            "kids_respone":{
                "name": "kids_respone",
                "questionText": "Are there kids traveling with you?",
                "answerOptions": [{ "answerText": 'Yes', "value": "1" }, { "answerText": 'No', "value": "2"}]
                },
            "month_response":{
                "name": "month_response",
                "questionText": "What month are you planning to travel?",
                "answerOptions": month_response_options
                },
            "currentcountry_response":{
                "name": "currentcountry_response",
                "questionText": "Where are you currently living?",
                "answerOptions": currentcountry_response_options
                },
            "prefer_rain_response": {
                "name": "prefer_rain_response",
                "questionText": "Do you prefer rainy weather?",
                "answerOptions":  [{ "answerText": "I don't mind rain", "value": "1" }, { "answerText": 'I prefer dry weather', "value": "2"}]
                },
            "prefer_temp_response":{
                "name": "prefer_temp_response",
                "questionText": "What temperature levels do you prefer? ",
                "answerOptions": [{ "answerText": "Cold Temperature (T < 15°C)", "value": "1" },
                                { "answerText": 'Moderate Temperature (15°C < T < 25°C )', "value": "2"},
                                { "answerText": 'High Temperature (25°C < T)', "value": "3"}]
                },
            "stay_outdoor_response":{
                "name": "stay_outdoor_response",
                "questionText": "How long are you planning to spend in outdoor areas?",
                "answerOptions": [{ "answerText": "Little time", "value": "1" },
                                { "answerText": 'Long time', "value": "2"}]
                },
            "budget_response":{
                "name": "budget_response",
                "questionText": "On average, how much more are you willing to spend (in your trip) relative to where you live?",
                "answerOptions": [{ "answerText": "Similar budget or cheaper", "value": "1" },
                                {"answerText": 'Less than double of what I spend on average', "value": "2"},
                                 {"answerText": 'Less than triple of what I spend on average', "value": "3"},
                                 {"answerText": 'Flexible', "value": "4"}]
                },
            "family_respone":{
                "name": "family_respone",
                "questionText": " Are you traveling with a Family or alone? ",
                "answerOptions": [{ "answerText": "Alone", "value": "1" },
                                {"answerText": 'With a Family', "value": "2"}]
                },
            "gender_response":{
                "name": "gender_response",
                "questionText": "What is your gender?",
                "answerOptions": [{ "answerText": "Female", "value": "1" },
                                {"answerText": 'Male', "value": "2"}]
                },
            "age_response":{
                "name": "age_response",
                "questionText": "What age group do you belong to?",
                "answerOptions": [{ "answerText": "18 - 34", "value": "1" },
                                {"answerText": '35 - 44', "value": "2"},
                                {"answerText": '45 - 54', "value": "3"},
                                {"answerText": '55 - 64', "value": "4"},
                                {"answerText": '65+', "value": "5"}]
                },
            "chroniccondition_response":{
                "name": "chroniccondition_response",
                "questionText": "Do you have any chronic conditions that might need medical attention during your Trip?",
                "answerOptions": [{ "answerText": "Yes", "value": "1" },
                                {"answerText": 'No', "value": "2"}]
                },
            "comfortimportance_response":{
                "name": "comfortimportance_response",
                "questionText": "Some people prefer to explore new cultures and countries, regardless of the level of comfort. What is the level of comfort (in terms of infrastructure) that you are looking (minimum) for in your trip compared where you live ?",
                "answerOptions": [{ "answerText": "I care about adventure rather than a comfortable trip", "value": "1" },
                                {"answerText": 'Slightly less comfortable', "value": "2"},
                                {"answerText": 'More comfortable or similar level', "value": "3"}
                                ]
                },
            "freedomimportance_response":{
                "name": "freedomimportance_response",
                "questionText": "On scale from 1 to 5, how much do you care about the civil and political freedom of your destination country?",
                "answerOptions": [{ "answerText": "1", "value": "1" },
                                {"answerText": '2', "value": "2"},
                                {"answerText": '3', "value": "3"},
                                {"answerText": '4', "value": "4"},
                                {"answerText": '5', "value": "5"}]
                },
        }

class next_question(APIView):
    def get(self, request):
        request_data = dict(request.session)
        prolog_task = async_task(run_prolog, request_data, ack_failure=True)
        next_step = result(prolog_task, wait=-1)
        if isinstance(next_step, str):
            return Response({"status": "success", "data": {"type": "question", "data":question[next_step]}}, status=status.HTTP_200_OK)
        else:
            request.session.flush()
            return Response({"status": "success", "data": {"type": "results", "data":next_step}}, status=status.HTTP_200_OK)

    def post(self, request):
        request.session[request.data['questionName']] = request.data['value']
        request_data = dict(request.session)
        prolog_task = async_task(run_prolog, request_data, ack_failure=True)
        next_step = result(prolog_task, wait=-1)
        if isinstance(next_step, str):
            return Response({"status": "success", "data": {"type": "question", "data":question[next_step]}}, status=status.HTTP_200_OK)
        else:
            request.session.flush()
            return Response({"status": "success", "data": {"type": "results", "data":next_step}}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        request.session.flush()
        return self.get(request)