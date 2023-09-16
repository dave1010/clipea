# Clipea 📎🟢

**Like Clippy but for the CLI. A blazing fast AI helper for your command line.**

Clipea is a barebones, cheaper and hackable [Copilot for CLI](https://githubnext.com/projects/copilot-cli).

It has similar roots to [Hubcap](https://github.com/dave1010/hubcap) but is less dangerous and actually designed to be a usable productivity tool, rather than just a tech demo.

Tell Clipea what you want to do and it'll give you a shell command, asking you if you want to run it. Clipea works even better with Zsh, as it adds the shell command to your console as a pending command, just as if you had typed it yourself!

❗ **Warning:** AI isn't perfect. Clipea might suggest a dangerous command. Be careful.

## Usage

### Without the Zsh shell integration

    clipea convert test.mp4 to a gif

Type `y<enter>` to run the command. Anything else or `<ctrl-c>` to cancel.

### With the Zsh shell integration (Recommended)

    ?? how many gig free do i have

Type `<enter>` to run the command. The command is editable in your shell buffer, ready to run, so you can do
usual things like `<ctrl-c>` to cancel or `<ctrl-a>` to go to the start of the line

### Feedback and editing

Just use your shell history by pressing the `<up>` arrow key. Your cursor will be at the end of
the last line, ready to edit it.

For example: typing `?? list js files recursively` may give
    
    $ find . -name "*.js"

Then to edit, press `<up>` then ` ignore node modules` to get something like

    $ find . -name "*.js" -not -path "./node_modules/*"

### More examples

    ?? count loc recursively
    ?? open my shell login script in my editor
    ?? git fetch, rebase master, safely force push
    ?? open bbc news

GPT-4 mode: just start the query with a "4". Remember that OpenAI charge lots more for GPT-4.
Generally the standard GPT-3.5 is fine for commandline stuff.

    ?? 4 create a text file explaining quantum mechanics in a haiku in the style of a pirate

You can also send in data via stdin. Clipea limits you to 8192 bytes, so the LLM isn't overwhelmed.

    ls -F | ?? explain this project setup

Generally it's best to give Clipea a filename to process, rather than the actual file contents.

    ?? count how many packages are in package.json

Clipea gets given some environment information like your OS, shell and path.
This allows it to give better responses.

    ?? wheres my shell config
    ?? install curl
    ?? compare README.md to my clipboard

## Installation and setup

Mac:

    brew install clipea #TODO

Linux or manual Mac install:

    git clone https://github.com/dave1010/clipea.git
    cd clipea
    ./clipea setup

1. Clone the repo and add it to your $PATH
2. `pip install llm`
3. `./clipea deps`


## Zsh Shell integration

Clipea takes advantage of zsh's `print -f`, which allows it to output commands on the commandline.

This requires running `source clipea.zsh`.

Clipea can set up a handy `??` alias that runs this for you.

    source clipea alias
    source ~/.zshrc

## How it works

Clipea uses [llm](https://github.com/simonw/llm) to interact with large language models.

Install dependencies:

    pip install llm

Set up your LLM. Eg [OpenAI](https://platform.openai.com/account/api-keys) or [another model](https://llm.datasette.io/en/stable/other-models.html).

    llm keys set openai

## Privacy

Clipea uses `llm`, which can be set to use OpenAI's LLMs or your own local one.

Only very basic environment info like your OS and editor is sent to the LLM.

Run `clipea env` to see the data the LLM gets.

## Cost

As a very rough example, using the default GPT-3, 100 Clipea queries to OpenAI cost $0.02.
Set a quota and keep an eye on costs to make sure.

## TODO

* First use wizard: disclaimer, user preferences, setup
* Explain command (eg type `<ctrl-a>?? ex <enter>` but watch out for pipes)
* Continue mode:
  * sometimes the LLM wants to send more content. Doesn't work with the shell itegration. 
  * could save the LLM output to a file and then stream it again if you run `??` by itself
* Run against https://github.com/Significant-Gravitas/Auto-GPT-Benchmarks