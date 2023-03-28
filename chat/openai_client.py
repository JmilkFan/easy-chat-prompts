import openai
import configparser
import time

config = configparser.ConfigParser()
config.read('./conf/config.ini')

class OpenAIClient(object):

    def __init__(self):
        super(OpenAIClient, self).__init__()
        openai.api_key = config.get('OpenAI', 'API_SECRET_KEY')
        self.max_retry = 3
        self.retry_delay = 5
        self.timeout = 10

    def _make_request(self, role, content):
        print("*************************************")
        print("request role: ", role)
        print("request content: ", content)
        print("*************************************")

        if role not in ['user', 'system', 'assistant']:
            print(f'role [{role}] not found.')
            raise

        retry_count = 0
        while retry_count < self.max_retry:
            try:
                response = openai.ChatCompletion.create(
                    model=config.get('OpenAI', 'MODEL'),
                    messages=[{"role": role, "content": content}],
                    max_tokens=2048,
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

    def chat_request(self, content):
        role = "user"
        return self._make_request(role, content)

    def prompt_request(self, content):
        role = "system"
        return self._make_request(role, content)

    # TODO(fguiju): Context request mode.
    def context_request(self):
        pass


    def parser_response(self, response):
        result = []
        choices = response.choices
        for cho in choices:
            result.append(
                {
                    'index': cho['index'],
                    'role': cho['message']['role'],
                    'content': cho['message']['content']
                }
            )
        return result


if __name__ == '__main__':
    cli = OpenAIClient()
    resp = cli.chat_request(content='hello!')
    print("Test response: ", cli.parser_response(resp))
