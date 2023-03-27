# easy-chat-prompts
让 ChatGPT 的应用变得简单且高效。

## 项目定位

1. 让 ChatGPT 成为先进生产力。
2. 建立一个可持续发展的学习交流社区。
3. 项目分层：
    - 基础设施层：让 ChatGPT 更易用；
    - 开发社区层：让 Prompts virtualenv 应用案例更多样；

# Python 编程语言

作为一个本地化工具，使用 Python 具有更加简单的学习和使用体验。

# 关于贡献者

可以从 API 层面深入到 ChatGPT 的底层 API 技术支撑，只有对其有充分的了解，才可能开发出更优秀的工具。

# 需求收敛

1. 从配置文件中读取 ChatGPT API SECRET KEY：将秘钥保存在配置文件中，以便快速、简单地修改和管理秘钥。
2. 提供交互式解析器（REPL）作为操作界面：REPL 可以让用户与 ChatGPT 交互，并获得即时的反馈。
3. 实现一个提示符虚拟环境系统（prompts virtualenv 管理器）：每个虚拟环境对应一个提示词交互空间。
4. 用户可以创建、编辑或删除一个 prompt-venv：promt-venv 的本质是一个 YAML 文件，包括 3 个必要的元素：name（唯一标识符）、pre_prompt（预设提示语）、new_prompts（学习到的提示语）和一个可选的元素 description（描述信息）。
5. 用户可以查看或切换到已经存在的 prompt-venvs，这些 prompt-venvs 在使用的过程中会不断学习，以此变得更加聪明。
6. prompt-venv yamls 应该可以互相 include，利用 ChatGPT 的多模态，融合复杂的交叉场景。