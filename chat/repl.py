import sys
import yaml

from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter

from rich.console import Console
from rich.markdown import Markdown
import rich.traceback

from chat.prompts_venv import PromptsVirtualenv

console = Console()
rich.traceback.install()   # 异常追踪


class ChatREPL(object):

    def __init__(self):
        self.venv = PromptsVirtualenv()

        self.keyword_func_mappings = {}
        self.venv.register_funs_as_keywords(self.keyword_func_mappings)

        self.current_repl_mode = "CLI"  # default
        self.current_venv = ""

        self.session = PromptSession(
            history=FileHistory('.repl_history'),   # 历史记录
            completer=WordCompleter(self.keyword_func_mappings.keys()), # 关键字自动补全
            auto_suggest=AutoSuggestFromHistory()   # 基于历史记录的热词提示
        )

    def _parser_cli_input(self, usr_input):
        words = usr_input.split()
        keyword = words[0]

        if keyword not in self.keyword_func_mappings.keys():
            console.print(f"[{keyword}] is not a keyword.")
            raise

        if len(words) >= 2:
            argv = words[1:]
        else:
            argv = []

        return keyword, argv

    def loop(self):
        while True:
            repl_mode_prompt_str_mappings = {
                'CLI': 'easy-chat (CLI) > ',                   # CLI mode 用于执行管理操作
                'CHAT': f'easy-chat (CHAT) [{self.current_venv}] > '  # CHAT mode 用于开始聊天
            }

            try:
                user_input = self.session.prompt(
                    repl_mode_prompt_str_mappings[self.current_repl_mode],
                    multiline=False)
            except KeyboardInterrupt:
                continue  # Control-C pressed. Try again.
            except EOFError:
                break     # Control-D pressed.
        
            if not user_input:
                continue  # Empty input.

            if self.current_repl_mode == 'CLI':
                key, argv = self._parser_cli_input(user_input)
                result = self.keyword_func_mappings[key](argv)
                markdown = Markdown(result[0]['content'])
                console.print(markdown, style="bold blue")

                self.current_repl_mode = 'CHAT'
                self.current_venv = argv[0]

            elif self.current_repl_mode == 'CHAT':
                result = self.venv.normal_chat(user_input)
                markdown = Markdown(result[0]['content'])
                console.print(markdown, style="bold blue")


def main():
    repl = ChatREPL()
    repl.loop()

if __name__ == '__main__':
    main()
