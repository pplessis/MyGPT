from requests import post, exceptions
from platform import system, machine, python_version
class ApiGPT ():
    API_KEY = ''
    NEWLINE = '\n'

    def __init__(self, PromptTemplate : str = '' ) :
        self.api_key = ApiGPT.API_KEY
        self.model = "gpt-3.5-turbo"
        self.api_url = "https://api.openai.com/v1/chat/completions"

        self.temperature = 0.7
        self.streamMode = False
        self.promptTemplate = PromptTemplate

        self.max_tokens = 1000
        self.messagesHistory = []

    @property
    def GetHeader (self) -> dict :

        myHeaders = {
         "User-Agent": f'ollama-python/({machine()} {system().lower()}) Python/{python_version()}'
        , "Accept": 'application/json'
        , "Accept-Encoding": 'gzip, deflate'
        ,"Content-Type": 'application/json'
        ,'charset':'utf-8'
        }

        return myHeaders
    def GetOllama (self, Prompt: str) -> dict :
        """_summary_

Explanation of Parameters:
model: The name of the model you are serving (e.g., llama2, custom-model-name).
prompt: The text input or query you want the model to respond to.
temperature (optional): Controls randomness in responses. Lower values (e.g., 0.2) make responses more deterministic; higher values (e.g., 0.8) make them more creative.
max_tokens (optional): Limits the number of tokens in the generated response.
top_p (optional): Adjusts nucleus sampling (probability mass for token selection).
top_k (optional): Limits token selection to the top-k most probable tokens.

        Args:
            Prompt (str): _description_

        Returns:
            dict: _description_
        """


        data = {
            "model":  self.model,
            "prompt": Prompt,

            "stream": self.streamMode,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
         }

        return data
    
    @staticmethod
    def DefinePrompt ( Variables: dict, Prompt: str = '' ) -> str:
        Prompt = Prompt

        returnHTMLCompleted = Prompt

        if (len( Variables) > 0 ):
            for key, replacement in Variables.items():
                returnHTMLCompleted = returnHTMLCompleted.replace( key, (str)(replacement) )

        return returnHTMLCompleted

    def GetResponse(self, MyVariables: dict, MyPrompt:str='') :
        currentPrompt = ''
        returnValue = ''
        response = ''

        if len(MyPrompt) == 0 :
           currentPrompt = self.DefinePrompt( Variables = MyVariables, Prompt=self.promptTemplate)
        else:
           currentPrompt = self.DefinePrompt(Variables = MyVariables, Prompt=MyPrompt)

        try:
            data = self.GetOllama(currentPrompt)
            self.messagesHistory.append(data)

            responseAI = post(self.api_url, headers=self.GetHeader, json=data)

            if responseAI.status_code == 200:
                response =  responseAI.json().get('response', {})
                #returnValue = response.replace( self.NEWLINE, '').replace('"', '')
            else:
                raise Exception(f"API request failed with status code {responseAI.status_code}")

        except exceptions.RequestException as e:
            print (f"Error: {e}")

        except Exception as e:
            print (f"An error occurred: {e}")

        return response
