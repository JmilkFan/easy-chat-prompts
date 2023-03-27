import configparser
import yaml
import openai
import time
import json
import os

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.lexers import PygmentsLexer
from pygments.styles import get_style_by_name
from pygments.lexers.python import Python3Lexer
from pygments.token import Token


# 全局配置信息
config = configparser.ConfigParser()
config.read('config.ini')
api_key = config.get('OpenAI', 'API_SECRET_KEY')
ai_mode = config.get('OpenAI', 'MODEL')


class OpenAIClient(object):

    def __init__(self):
        super(OpenAIClient, self).__init__()
        openai.api_key = api_key
        self.max_retry = 5
        self.retry_delay = 5
        self.timeout = 10

    def make_request(self, content):
        print("request content: ", content)
        retry_count = 0
        while retry_count < self.max_retry:
            try:
                response = openai.ChatCompletion.create(
                    model=ai_mode,
                    messages=[{"role": "system", "content": content}],
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7,
                    timeout=self.timeout
                )
                return response
            except Exception as e:
                print(f"Failed to connect to API server, detail error as {e}, retrying in {self.retry_delay} seconds ({retry_count+1}/{self.max_retry})")
                time.sleep(self.retry_delay)
                retry_count += 1
        print("Failed to complete request")

    def parser_response(self, response):
        content = response.choices[0]['message']['content']
        print(content)


class PromptsVirtualenv(object):

    def __init__(self):
        self.venv_json = "prompts_venv.json"
        self.openai_cli = OpenAIClient()

    def list_venvs_info(self, _):
        with open(self.venv_json, "r") as f:
            data = json.load(f)
        print("venvs_info: ", data)

    def get_venv_info(self, argv):
        name = argv[1]
        with open(self.venv_json, "r") as f:
            data = json.load(f)
        if name in data.keys():
            print(data[name])
        else:
            print(f"venv [{name}] not found.")

    def add_venv(self, argv):
        name = argv[1]
        file_path = argv[2]
        if os.path.exists(file_path):
            with open(self.venv_json, "r") as f:
                data = json.load(f)
            data[name] = file_path

            with open(self.venv_json, "w") as f:
                json.dump(data, f)
        else:
            print(f"YAML file [{file_path}] not found.")

    def delete_venv(self, argv):
        name = argv[1]
        with open(self.venv_json, "r") as f:
            data = json.load(f)

        if name in data.keys():
            data.pop(name)
            with open(self.venv_json, "w") as f:
                json.dump(data, f)
        else:
            print(f"venv [{name}] not found.")


    def enter_venv(self, argv):
        name = argv[1]
        with open(self.venv_json, "r") as f:
            data = json.load(f)
        if name in data.keys():
            file_path = data[name]

            with open(file_path) as f:
                venv_yaml = yaml.load(f, Loader=yaml.FullLoader)

            resp = self.openai_cli.make_request(venv_yaml[2]['pre_prompt'])
            self.openai_cli.parser_response(resp)
        else:
            print(f"venv [{name}] not found.")

    def ask_chatgpt(self, prompt):
        resp = self.openai_cli.make_request(prompt)
        self.openai_cli.parser_response(resp)


class ChatShell(object):

    def __init__(self):

        self.proms_venv = PromptsVirtualenv()

        # REPL keywords and functions mapping.
        self.keywords = {
            'list_venvs': self.proms_venv.list_venvs_info,
            'get_venv': self.proms_venv.get_venv_info,
            'add_venv': self.proms_venv.add_venv,
            'del_venv': self.proms_venv.delete_venv,
            'enter_venv': self.proms_venv.enter_venv,
        }

    
    def loop(self):
        completer = WordCompleter(self.keywords.keys())
        history = FileHistory('.history')
    
        while True:
            input = prompt(
                'My Python REPL > ', 
                lexer=PygmentsLexer(Python3Lexer), 
                completer=completer, 
                history=history, 
                auto_suggest=AutoSuggestFromHistory())

            argv = input.split()

            # Call ChatGPT
            if argv[0] == 'ask':
                self.proms_venv.ask_chatgpt(input)
                continue

            # Normal output
            if argv[0] not in self.keywords:
                print(f'You entered: {input}')
                continue
        
            # Virtualenv process
            self.keywords[argv[0]](argv)


def main():
    shell = ChatShell()
    shell.loop()


if __name__ == '__main__':
    main()














