# Copilot

GitHub Copilot uses OpenAI Codex to suggest code and entire functions in
real-time right from your editor. Trained on billions of lines of public
code, GitHub Copilot turns natural language prompts including comments and
method names into coding suggestions across dozens of languages.

To learn more, visit
[https://github.com/features/copilot](https://github.com/features/copilot).

## Objective

This repo collects bindings of Copilot to various languages.

The current supported language bindings are:

- [Python](bindings/python)

The goal is to provide a programmable interface to Copilot, so that automated tools can be built on top of it.

Bindings for different languages are provided in separate subdirectories of [bindings](bindings).

## Usage

Please refer to the README in each language binding for usage instructions.

## Technology behind

The binding to Copilot leverages the [LSP](https://microsoft.github.io/language-server-protocol/) of Copilot that is
originally provided by [copilot.vim](https://github.com/github/copilot.vim).

The binding is implemented as a service that acts as a client to the Copilot's LSP server.

