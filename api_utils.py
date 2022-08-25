import requests
import json

from PIL import Image
import requests
from io import BytesIO

class OpenAPI():
    def __init__(self, token):
        self.beta_url = 'https://labs.openai.com/api'
        self.base_url = 'https://api.openai.com/v1'
        self.token = token
        
    def getHeaders(self):
        return {
            "Authorization": "Bearer " + self.token
        }
    
    def postHeaders(self):
        return {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json"
        }
    
class CompletionsAPI(OpenAPI):
    def __init__(self, token):
        super().__init__(token)
        self.model = 'text-davinci-002'
        self.max_tokens = 256
        self.temperature = 0.7
        
        
    def getPromptResult(self, prompt):
        payload = json.dumps({'model':self.model, 'prompt': prompt , 'max_tokens':self.max_tokens, 'temperature':self.temperature})
        url = self.base_url + '/completions'
        p = requests.post(
            url,
            headers=self.postHeaders(),
            data=payload
        )
        p.raise_for_status()
        return p.json()['choices'][0]['text']

class TasksAPI(OpenAPI):
    def __init__(self, token):
        super().__init__(token)
        self.url = self.beta_url + '/labs/tasks'
        
    def createTask(self, prompt):
        payload = json.dumps({'task_type': 'text2im', 'prompt': {'caption': prompt, 'batch_size':4}})
        url = self.url
        p = requests.post(
            url,
            headers=self.postHeaders(),
            data=payload
        )
        p.raise_for_status()
        return p.json()['id']
    
    def getStatus(self, task_id):
        url = self.url + '/' + task_id
        r = requests.get(
            url,
            headers=self.getHeaders()
        )
        r.raise_for_status()
        return r.json()['status']
    
    def getImagePaths(self, task_id):
        url = self.url + '/' + task_id
        r = requests.get(
            url,
            headers=self.getHeaders()
        )
        r.raise_for_status()
        resp = r.json()['generations']['data']
        return [i['generation']['image_path'] for i in resp]
    
    def downloadImage(self, img_path):
        response = requests.get(img_path)
        return Image.open(BytesIO(response.content))