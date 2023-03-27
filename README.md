# easy-chat-prompts

让 ChatGPT 的应用变得简单且高效。

## 项目定位

1. 让 ChatGPT 成为先进生产力。
2. 建立一个可持续发展的学习交流社群。
3. 项目分层：
    - 基础设施层：让 ChatGPT 更易用；
    - 开发社区层：让 Prompts virtualenv 应用案例更多样；

## 需求收敛

1. **实现一个交互式解析器（REPL）作为操作界面**：REPL 可以让用户与 ChatGPT 交互，并获得即时的反馈。
3. **实现一个提示符虚拟环境系统（prompts virtualenv）**：每个 venv 对应一个提示操作空间。
4. **用户可以创建、编辑或删除一个 Prompt-venv**：Promt-venv 的本质是一个 YAML 文件，包括 3 个必要的元素：
    1. name（唯一标识符）；
    2. pre_prompt（预设提示语）；
    3. new_prompts（学习到的提示语）
5. **用户可以查看或切换到一个已经存在的 Prompt-venv**：Prompt-venvs 在使用的过程中会不断学习新的 Prompts，以此来变得更聪明。
6. **Prompt-venv yamls 应该可以互相 include**：利用 ChatGPT 的多模态，融合复杂的交叉场景。