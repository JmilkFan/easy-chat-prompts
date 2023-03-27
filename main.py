import configparser
import openai
import cmd
import yaml
from requests.exceptions import ProxyError
import time


class ChatShell(cmd.Cmd):
    intro = 'Welcome to the ChatShell. Type help or ? to list commands.\n'
    prompt = 'ChatShell > '

    def __init__(self, config_file):
        super(ChatShell, self).__init__()
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.api_key = self.config.get('OpenAI', 'API_SECRET_KEY')
        openai.api_key = self.api_key
        self.prompts_venv_file = "easy-chat.yaml"
        self.max_retry = 5
        self.retry_delay = 5
        self.timeout = 10

    def do_ask(self, line):
        templates = []
        with open(self.prompts_venv_file) as f:
            prom_venv = yaml.load(f, Loader=yaml.FullLoader)
        
        name = prom_venv[0]['name']
        print("name: ", name)
        description = prom_venv[1]['description']
        print("description: ", description)

        pre_prompt = prom_venv[2]['pre_prompt']
        response = self.make_request(content=pre_prompt)

        self.parser_response(response)

    def make_request(self, content):
        print("content: ", content)
        retry_count = 0
        while retry_count < self.max_retry:
            try:
                response = openai.ChatCompletion.create(
                    model=self.config.get('OpenAI', 'MODEL'),
                    messages=[{"role": "system", "content": content}],
                    max_tokens=1024,
                    n=1,
                    stop=None,
                    temperature=0.7,
                    timeout=self.timeout
                )
                return response
            except ProxyError as e:
                print(f"Failed to connect to proxy, retrying in {self.retry_delay} seconds ({retry_count+1}/{self.max_retry})")
                time.sleep(self.retry_delay)
                retry_count += 1
            except Exception as e:
                print(f"Failed to connect to API server, retrying in {self.retry_delay} seconds ({retry_count+1}/{self.max_retry})")
                time.sleep(self.retry_delay)
                retry_count += 1

        print("Failed to complete request")
        return ""

    def parser_response(self, response):
        content = response.choices[0]['message']['content']
        print(content)

    def do_quit(self, line):
        return True

if __name__ == '__main__':
    ChatShell('config.ini').cmdloop()
