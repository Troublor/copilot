from __future__ import annotations

import pathlib

from typing import TypedDict, Union, List


class CompletionRequestPosition(TypedDict):
    line: int
    character: int


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
    def __init__(self, doc_file: str, language_id: str, position: CompletionRequestPosition, insert_spaces: bool = True,
                 tab_size: int = 4, indent_size: int = 4):
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
    text: str
    displayText: str
    range: CompletionResponseRange
    position: CompletionRequestPosition


class CompletionResponse(TypedDict):
    completions: List[CompletionResponseCandidate]
