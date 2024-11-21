from eco.bonita.access import Access
from decimal import Decimal
import json

class Process:
    def __init__(self, access:Access):
        self.access = access


    def startProcess(self):
        access = Access()
        access.login()  # Login to get the token

        # Instantiate the Process class with the access object
        return Process(access)

    def getAllProcess(self):
        response = self.access.make_request('GET', 'API/bpm/process?p=0&c=1000')
        return response.json()['data']

    def getProcessName(self, id):
        response = self.access.make_request('GET', f'API/bpm/process/{id}')
        process = response.json()['data']
        return process['name']

    def getProcessId(self, name):
        query = f'API/bpm/process?f=name={name}'
        response = self.access.make_request('GET', query)
        print(response)
        process_id = response.json()[0]['id']
        return process_id

    def getCountProcess(self):
        response = self.access.make_request('GET', 'API/bpm/process?p=0&c=1000')
        return len(response.json()['data'])

    def initiateProcess(self, id):
        response = self.access.make_request('POST', f'API/bpm/process/{id}/instantiation')
        return response.json()

    def checkCase(self, case_id):
        case_response = self.access.make_request('GET', f'API/bpm/case/{case_id}')
        print(f"Estado del caso recién creado: {case_response.status_code}")

    def setVariable(self, taskId, variable, valor, tipo):
        task_response = self.access.make_request('GET', f'API/bpm/userTask/{taskId}')
        caseId = task_response.json()['data']['caseId']
        response = self.access.make_request('PUT', f'API/bpm/caseVariable/{caseId}/{variable}', json={variable: valor, 'type': tipo})
        return response.json()

    def setVariableByCase(self, caseId, variable, valor, tipo):
        # en caso de que sea decimal lo cambio a float (decimal da error)
        if isinstance(valor, Decimal):
            valor = float(valor)
        response = self.access.make_request('PUT', f'API/bpm/caseVariable/{caseId}/{variable}', json={'name':variable,'value': valor, 'type': f"java.lang.{tipo}"})
        return response

    def assignTask(self, taskId, userId):
        response = self.access.make_request('PUT', f'API/bpm/userTask/{taskId}', json={'assigned_id': userId})
        return response.json()

    def detailsTask(self, task_id):
        task_details = self.access.make_request('GET', f'API/bpm/userTask/{task_id}')
        print(f"Detalles de la tarea {task_id}: {task_details.json()}")

    def searchActivityByCase(self, caseId):
        response = self.access.make_request('GET', f'API/bpm/task?f=caseId={caseId}')
        return response.json()

    def completeActivity(self, taskId):
        response = self.access.make_request('POST', f'API/bpm/userTask/{taskId}/execution?assign=true')
        return response

    def getVariable(self, taskId, variable):
        task_response = self.access.make_request('GET', f'API/bpm/userTask/{taskId}')
        caseId = task_response.json()['data']['caseId']
        var_response = self.access.make_request('GET', f'API/bpm/caseVariable/{caseId}/{variable}')
        return var_response.json()['data']

    def getVariableByCase(self, caseId, variable):
        cleaned_caseId = caseId.replace(' ', '')
        var_response = self.access.make_request('GET', f'API/bpm/caseVariable/{cleaned_caseId}/{variable}')
        return var_response.json()['data']
