# Importing Libraries and Variables
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from prolog_api.prolog_engine import run_prolog
from django_q.tasks import async_task, result
from .variables_data import question

# Handling the API Request
class next_question(APIView):
    def get(self, request, reset = False):
        if reset:
            request.session.flush()
        # Extract the session data
        request_data = dict(request.session)
        # Run a prolog task with the session data
        prolog_task = async_task(run_prolog, request_data, ack_failure=True)
        # Wait the response from the prolog
        next_step = result(prolog_task, wait=-1)
        # Check the type of response returned another question or the results? 
        if isinstance(next_step, str):
            return Response({"status": "success", "data": {"type": "question", "data":question[next_step]}}, status=status.HTTP_200_OK)
        else:
            request.session.flush()
            return Response({"status": "success", "data": {"type": "results", "data":next_step}}, status=status.HTTP_200_OK)

    def post(self, request):
        # Get the new data to be added to the current session
        request.session[request.data['questionName']] = request.data['value']
        # Get the current session data
        request_data = dict(request.session)
        # Run a prolog task with the session data
        prolog_task = async_task(run_prolog, request_data, ack_failure=True)
        # Wait the response from the prolog
        next_step = result(prolog_task, wait=-1)
        # Check the type of response returned another question or the results? 
        if isinstance(next_step, str):
            return Response({"status": "success", "data": {"type": "question", "data":question[next_step]}}, status=status.HTTP_200_OK)
        else:
            # Reset the sessoin data if the results are back
            request.session.flush()
            return Response({"status": "success", "data": {"type": "results", "data":next_step}}, status=status.HTTP_200_OK)
    
    def delete(self, request):
        # Reset the session data and send the first question
        return self.get(request, reset=True)