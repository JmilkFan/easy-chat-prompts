import yaml

import chat.utils.json_file_curd as json_tools
from chat.openai_client import OpenAIClient

class PromptsVirtualenv(object):

    def __init__(self):
        self._venv_json = "./venv/.prompts_venv.json"
        json_tools.init_json_file(self._venv_json)
        self.openai_cli = OpenAIClient()

    def list_venvs_info(self, _):
        return json_tools.read_json_file(self._venv_json)

    def get_venv_info(self, argv):
        venv_name = argv[0]
        data = json_tools.read_json_file(self._venv_json)
        return json_tools.get_value(data, venv_name)

    def add_venv(self, argv):
        venv_name = argv[0]
        venv_file_path = argv[1]
        data = json_tools.read_json_file(self._venv_json)
        json_tools.add_key_value(data, venv_name, venv_file_path)
        json_tools.write_json_file(data, self._venv_json)
        return data

    def delete_venv(self, argv):
        venv_name = argv[0]
        data = json_tools.read_json_file(self._venv_json)
        json_tools.delete_value(data, venv_name)
        json_tools.write_json_file(data, self._venv_json)
        return data
    
    def enter_venv(self, argv):
        venv_name = argv[0]
        try:
            yaml_file_path = f'./venv/{self.get_venv_info(argv)}'
            with open(yaml_file_path) as f:
                venv_yaml = yaml.load(f, Loader=yaml.FullLoader)

            resp = self.openai_cli.prompt_request(venv_yaml[2]['pre_prompt'])
            return self.openai_cli.parser_response(resp)

        except Exception as e:
            print("Enter venv error.")
            raise
    
    def normal_chat(self, content):
        resp = self.openai_cli.chat_request(content)
        return self.openai_cli.parser_response(resp)

    def register_funs_as_keywords(self, keywords):
        keywords['list_venvs'] = self.list_venvs_info
        keywords['get_venv'] = self.get_venv_info
        keywords['add_venv'] = self.add_venv
        keywords['delete_venv'] = self.delete_venv
        keywords['enter_venv'] = self.enter_venv


if __name__ == '__main__':
    venv = PromptsVirtualenv()
    venv.add_venv('test', 'test.yaml')
    print('list: ', venv.list_venvs_info())
    print('get:', venv.get_venv_info('test'))

    venv.delete_venv('test')
    print('list: ', venv.list_venvs_info())
