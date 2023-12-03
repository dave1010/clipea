# Clipea 📎🟢

[![Install with pip](https://img.shields.io/badge/Install_with-pip-blue)](https://pypi.org/project/clipea-cli/)
[![PyPI](https://img.shields.io/pypi/v/clipea-cli.svg)](https://pypi.org/project/clipea-cli/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/clipea-cli)](https://pypi.org/project/clipea-cli/)
[![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/dave1010/clipea/python-app.yml)](https://github.com/dave1010/clipea/actions)


**Like Clippy but for the CLI. A blazing fast AI helper for your command line.**

Clipea is a streamlined, cheap and hackable tool that integrates GPT with your console.
It's like Github's [Copilot for CLI](https://githubnext.com/projects/copilot-cli) but it's cheaper, faster and doesn't get in your way.

Tell Clipea what you want to do and it'll give you a shell command, asking you if you want to run it. Clipea works even better with Zsh, as it adds the shell command to your console as a pending command, just as if you had typed it yourself!

![clipea-gif](https://github.com/dave1010/clipea/assets/50682/9aae6c64-2d09-4e7f-9d86-4d82dd4bc076)

Clipea was born out of [Hubcap](https://github.com/dave1010/hubcap), an experimental autonomous agent.
Clipea is less dangerous and actually designed to be a usable productivity tool, rather than just a tech demo.

Advantages over copying and pasting from ChatGPT:

* Speed. No need to switch to your browser and back
* Shell integration, like filename completion
* Automatically knows things like your shell and OS

> [!CAUTION]
> AI isn't perfect. Clipea might suggest a dangerous command. Be careful.

## 🚀 Quick Start

    pipx install clipea-cli
    clipea setup
    clipea alias

## 🪄 Usage

Once installed, just ask Clipea for a command:

    clipea convert test.mp4 to a gif

Type `y<enter>` to run the command. Anything else or `<ctrl-c>` to cancel.

Or, if you have the Zsh integration (highly recommended), it's even easier:

    ?? how many gig free do i have

Just press `<enter>` to run the command or `<backspace>` if you want to edit it.

Clipea works best when you give it a task to complete, rather than a question: LLMs love explaining things whenever you're not sure.

### ❓❓ Using the Zsh shell integration (recommended)

The Zsh integration is more than just a quick alias.
It allows Clipea to put the command in your input buffer, ready to run, just as if you'd typed it yourself.

    # setup
    clipea alias

    # usage
    ?? how many gig free do i have

Benefits:

* Quicker to type
* Shows up in your shell history
* Allows editing with normal shell commands like `<ctrl-c>` to cancel or `<ctrl-a>` to go to the start of the line
* Runs the command as a child process of your shell, rather than a child of Clipea

Behind the scenes this is using zsh's [`print -z`](https://gist.github.com/YumaInaura/2a1a915b848728b34eacf4e674ca61eb#print--z).

### 🧙 Advanced usage and tips

#### GPT-4 mode

Just start the query with a "4". Remember that OpenAI charge lots more for GPT-4.
Generally the standard GPT-3.5 is fine for commandline stuff.

    ?? 4 create a text file explaining quantum mechanics in a haiku in the style of a pirate

#### Getting data from stdin

You can also send in data via stdin. Clipea limits you to 8192 bytes, so the LLM isn't overwhelmed.

    ls -F | ?? explain this project setup

Most of the time it's best to give Clipea a filename to create a command for, rather than the actual file contents.

    cat package.json | ?? how many packages here     # GPT isn't great at counting
    ?? count how many packages are in package.json   # GPT is good at suggesting commands

#### Environment

Clipea gets given some environment limited information like your OS, shell and path.
This allows it to give better responses.

    ?? wheres my shell config
    ?? install curl
    ?? compare README.md to my clipboard

#### Custom Prompt

You can customize your prompt by creating a prompt file in your home directory.

    ~/.config/clipea/system-prompt.txt

You might wanna start by copying the default prompt:

    cp $(dirname $(readlink -f $(which clipea)))/system-prompt.txt ~/.config/clipea/system-prompt.txt

Then edit `~/.config/clipea/system-prompt.txt` to your liking, but be aware that environment info is always added to the end of the prompt.

### ⤴️ Feedback and editing

Just use your shell history by pressing the `<up>` arrow key. Your cursor will be at the end of
the last line, ready to edit it.

For example: typing `?? list js files recursively` may give

    $ find . -name "*.js"

Then to edit, press `<up>` then ` ignore node modules` to get something like

    $ find . -name "*.js" -not -path "./node_modules/*"

Clipea doesn't have any context of what it said before, though this may be added in the future if there's use cases it helps with.

### More examples

#### System Operations

    ?? open my shell login script in my editor
    ?? Extract package.tar.gz
    ?? Install something that converts pdf to text
    ?? Make a 30 char password

#### File Operations

    ?? Find files bigger than 10mb
    ?? Rename all txt files space to underscore
    ?? Convert file.avi to gif
    ?? Decrypt data.txt.gpg

#### Text Files and Coding

    ?? Highlight URLs in index.html
    ?? Show me just the headings from README.md
    ?? count loc recursively
    ?? Find replace all PHP files in project that call eval function with safe_eval
    ?? git fetch, rebase master, safely force push
    ?? turn orders.csv into sqlite
    ?? count payments in orders.db

#### Web and Network Tasks

    ?? open bbc news
    ?? check the spf record for example.com
    ?? What port is my webserver listening on
    ?? Check cors headers for api.example.com
    ?? Where is nginx writing logs
    ?? Quick http server

## 📦 Installation and setup

### Manual installation

Python >=3.10 is required.

You can use the provided `setup.py`. ([setuptools docs](https://setuptools.pypa.io/en/latest/deprecated/easy_install.html))

You can install it quickly like so:

    python3 setup.py sdist
    pip install dist/clipea-{version}.tar.gz

Or development mode:

    pip install -e .

### With PyPi

    pipx install clipea-cli

### Zsh Shell integration and Alias

> [!TIP]
> The `??` shell alias is highly recommended if you use zsh

    clipea alias

## Internals

Clipea is written in Python (3.10+).

Clipea uses [llm](https://github.com/simonw/llm) to interact with large language models.

By default it will use OpenAI's GPT-3.5 model but can be configured to other models, such as Llama.
Running `clipea setup` will talk you through getting OpenAI keys.

## ❗ Warnings

### Safety

> [!CAUTION]
> Always read and check what Clipea suggests before accepting it.

![destroy all humans](https://github.com/dave1010/clipea/assets/50682/afa819bd-a8cc-4968-973f-9b99ceaab5b4)

### Privacy

Clipea uses OpenAI's APIs by default, though can be set to use any LLM that `llm` supports.

Only very basic environment info like your OS and editor is sent to the LLM.
Run `clipea env` to see the data the LLM gets.

### Cost

As a very rough example, using the default GPT-3.5, 100 Clipea queries to OpenAI cost $0.02.
Set a quota and keep an eye on costs to make sure.

## Acknowledgements

Big thanks to @edouard-sn for the port to Python.

## Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/antwxne"><img src="https://avatars.githubusercontent.com/u/59999873?v=4?s=100" width="100px;" alt="Antoine D."/><br /><sub><b>Antoine D.</b></sub></a><br /><a href="#review-antwxne" title="Reviewed Pull Requests">👀</a></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

## License

MIT License

Copyright (c) 2023 Dave Hulbert
