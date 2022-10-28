from __future__ import annotations

import pathlib

from typing import TypedDict, Union, List


class CompletionRequestPosition(TypedDict):
    """
    A position in the source file.
    """
    line: int  # The line number, starting from 0.
    character: int  # The character offset (column) on a line, starting from 0.


class CompletionRequestDoc(TypedDict):
    uri: str
    path: str
    relativePath: str
    source: str
    position: CompletionRequestPosition
    languageId: str
    insertSpaces: str
    tabSize: int
    indentSize: int


class CompletionRequestTextDocument(TypedDict):
    uri: str
    relativePath: str
    languageId: str


class CompletionRequestParams(object):
    """
    The params for the request of getCompletion request to Copilot.
    """

    def __init__(self, doc_file: str, language_id: str, position: CompletionRequestPosition, insert_spaces: bool = True,
                 tab_size: int = 4, indent_size: int = 4):
        """
        The request params for the code completion request to Copilot.
        :param doc_file: the path to the source code file to get completions for
        :param language_id: the language id of the source code file. It should be one of the languages
                            listed in https://github.com/nvim-treesitter/nvim-treesitter#supported-languages
        :param position: the current position of the cursor in the source code file
        :param insert_spaces: whether to use spaces instead of tabs
        :param tab_size: the number of spaces to use for a tab
        :param indent_size: the number of spaces to use for an indent
        """
        self.doc_file = doc_file
        self.language_id = language_id
        self.position = position
        self.insert_spaces = insert_spaces
        self.tab_size = tab_size
        self.indent_size = indent_size

    def to_dict(self, root_dir: Union[None, str] = None) -> dict:
        if root_dir is None:
            root_dir = pathlib.Path(self.doc_file).parent
        return {
            "doc": {
                "uri": pathlib.Path(self.doc_file).as_uri(),
                "path": self.doc_file,
                "relativePath": pathlib.Path(self.doc_file).relative_to(root_dir).__str__(),
                "source": pathlib.Path(self.doc_file).read_text(),
                "position": self.position,
                "languageId": self.language_id,
                "insertSpaces": True,
                "tabSize": self.tab_size,
                "indentSize": self.indent_size,
            },
            "textDocument": {
                "uri": pathlib.Path(self.doc_file).as_uri(),
                "relativePath": pathlib.Path(self.doc_file).relative_to(root_dir).__str__(),
                "languageId": self.language_id,
            },
            "position": self.position,
        }


class CompletionResponseRange(TypedDict):
    start: CompletionRequestPosition
    end: CompletionRequestPosition


class CompletionResponseCandidate(TypedDict):
    uuid: str
    text: str  # the full completion text
    displayText: str  # The text to display in the text editor
    range: CompletionResponseRange  # The range in the source code file to replace with the completion text
    position: CompletionRequestPosition  # The position of the cursor


class CompletionResponse(TypedDict):
    """
    The response of the getCompletion request to Copilot.
    """
    completions: List[CompletionResponseCandidate]  # a list of candidate code completions


class SignInInitiative(TypedDict):
    status: str
    userCode: str
    verificationUri: str
    expiresIn: int
    interval: int
