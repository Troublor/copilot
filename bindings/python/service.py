import subprocess
from typing import Callable

import semver
import os
import pylspclient
import pathlib

from model import CompletionRequestParams, CompletionResponse, SignInInitiative


class CopilotService(object):
    """
    Copilot service
    """

    @staticmethod
    def _check_dependency():
        """
        Check if the dependency is installed.
        The Copilot LSP server requires Node.js 16.x.x.
        The node executable should be in the PATH.
        :raises: Exception if the dependency is not satisfied.
        """
        p = subprocess.Popen(["node", "-v"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        if err:
            raise Exception(f"Node.js is not executable: {err.decode('utf-8')}")
        ver = out.decode("utf-8").strip().replace("v", "")
        if not (semver.compare("16.0.0", ver) <= 0 and semver.compare(ver, "17.0.0")) < 0:
            raise Exception(f"Node.js version {ver} is not supported. Please install Node.js 16")

    def __init__(self, root_path: str,
                 copilot_agent_path: str = None):
        """
        Initialize the Copilot service.
        :param root_path: the root directory that Copilot LSP server runs on. Usually this should be the root directory
                          of the project for which Copilot suggests code completions.
        :param copilot_agent_path: optional, the path to the Copilot LSP server (agent.js).
                                   Defaults to the bundled Copilot LSP
        """
        self.root_path = root_path
        self.workspace_folders = None
        self.copilot_agent_path = copilot_agent_path

        self._check_dependency()
        lsp_cmd = ["node", self.copilot_agent_path if self.copilot_agent_path is not None else os.path.join(
            os.path.dirname(__file__), "..", "..", "copilot", "dist", "agent.js")]
        p = subprocess.Popen(lsp_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.p = p
        json_rpc_endpoint = pylspclient.JsonRpcEndpoint(p.stdin, p.stdout)
        self.lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint,
                                                    timeout=10,
                                                    method_callback=self._callback,
                                                    notify_callback=self._callback)
        self.lsp_client = pylspclient.LspClient(self.lsp_endpoint)

        self._initialize()

    def _initialize(self):
        self.lsp_client.initialize(self.p.pid, self.root_path, pathlib.Path(self.root_path).as_uri(), None,
                                   self._client_capabilities, "off",
                                   self.workspace_folders)
        self.lsp_client.initialized()

    def shutdown(self):
        """
        Shutdown the Copilot service.
        """
        self.lsp_client.shutdown()
        self.p.terminate()

    def get_completions(self, completion_request_params: CompletionRequestParams) -> CompletionResponse:
        """
        Get code completions.
        :param completion_request_params: a CompletionRequestParams object that specifies the source code file
                                          to suggest code completions for.
        :return: CompletionResponse object, containing all the candidate code completions.
        """
        return self.lsp_endpoint.call_method("getCompletions", **completion_request_params.to_dict(self.root_path))

    def sign_in(self, callback: Callable[[SignInInitiative], None]):
        """
        Sign in to Copilot.
        :param callback: a function that takes a SignInInitiative object as input. Users of Copilot should authorize
                         Copilot at https://github.com/login/device using the userCode given in the SignInInitiative
                         object. When the callback returns, the Copilot must be already authorized since the Copilot LSP
                         server will check the sign-in status after the callback returns. After signing in, there is
                         no need to re-sign in even if the program is restarted.
        """
        resp = self.lsp_endpoint.call_method("signInInitiate", **dict())
        callback(resp)
        return self.lsp_endpoint.call_method("signInConfirm", **dict())

    def sign_out(self):
        """
        Sign out the current user of Copilot.
        :return:
        """
        self.lsp_endpoint.call_method("signOut", **dict())

    def signed_in(self) -> bool:
        """
        Check if a user is already signed in to Copilot.
        :return:
        """
        resp = self.lsp_endpoint.call_method("checkStatus", **{'options': {'localChecksOnly': True}})
        return resp['status'] == 'OK' or resp['status'] == 'MaybeOK'

    def _callback(self, key: str, data: dict):
        pass

    @property
    def _client_capabilities(self):
        return {
            "window": {
                "showDocument": {
                    "support": False
                },
                "workDoneProgress": True,
                "showMessage": {
                    "messageActionItem": {
                        "additionalPropertiesSupport": False
                    }
                }
            },
            "callHierarchy": {
                "dynamicRegistration": False
            },
            "textDocument": {
                "implementation": {
                    "linkSupport": True
                },
                "typeDefinition": {
                    "linkSupport": True
                },
                "completion": {
                    "contextSupport": False,
                    "completionItemKind": {
                        "valueSet": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14,
                            15,
                            16,
                            17,
                            18,
                            19,
                            20,
                            21,
                            22,
                            23,
                            24,
                            25
                        ]
                    },
                    "dynamicRegistration": False,
                    "completionItem": {
                        "preselectSupport": False,
                        "deprecatedSupport": False,
                        "documentationFormat": [
                            "markdown",
                            "plaintext"
                        ],
                        "snippetSupport": False,
                        "commitCharactersSupport": False
                    }
                },
                "signatureHelp": {
                    "signatureInformation": {
                        "activeParameterSupport": True,
                        "documentationFormat": [
                            "markdown",
                            "plaintext"
                        ],
                        "parameterInformation": {
                            "labelOffsetSupport": True
                        }
                    },
                    "dynamicRegistration": False
                },
                "hover": {
                    "contentFormat": [
                        "markdown",
                        "plaintext"
                    ],
                    "dynamicRegistration": False
                },
                "codeAction": {
                    "codeActionLiteralSupport": {
                        "codeActionKind": {
                            "valueSet": [
                                "",
                                "Empty",
                                "QuickFix",
                                "Refactor",
                                "RefactorExtract",
                                "RefactorInline",
                                "RefactorRewrite",
                                "Source",
                                "SourceOrganizeImports",
                                "quickfix",
                                "refactor",
                                "refactor.extract",
                                "refactor.inline",
                                "refactor.rewrite",
                                "source",
                                "source.organizeImports"
                            ]
                        }
                    },
                    "isPreferredSupport": True,
                    "dataSupport": True,
                    "resolveSupport": {
                        "properties": [
                            "edit"
                        ]
                    },
                    "dynamicRegistration": False
                },
                "references": {
                    "dynamicRegistration": False
                },
                "documentHighlight": {
                    "dynamicRegistration": False
                },
                "synchronization": {
                    "willSave": False,
                    "willSaveWaitUntil": False,
                    "didSave": True,
                    "dynamicRegistration": False
                },
                "rename": {
                    "prepareSupport": True,
                    "dynamicRegistration": False
                },
                "documentSymbol": {
                    "hierarchicalDocumentSymbolSupport": True,
                    "dynamicRegistration": False,
                    "symbolKind": {
                        "valueSet": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14,
                            15,
                            16,
                            17,
                            18,
                            19,
                            20,
                            21,
                            22,
                            23,
                            24,
                            25,
                            26
                        ]
                    }
                },
                "declaration": {
                    "linkSupport": True
                },
                "publishDiagnostics": {
                    "tagSupport": {
                        "valueSet": [
                            1,
                            2
                        ]
                    },
                    "relatedInformation": True
                },
                "definition": {
                    "linkSupport": True
                }
            },
            "workspace": {
                "applyEdit": True,
                "workspaceFolders": True,
                "workspaceEdit": {
                    "resourceOperations": [
                        "rename",
                        "create",
                        "delete"
                    ]
                },
                "symbol": {
                    "hierarchicalWorkspaceSymbolSupport": True,
                    "dynamicRegistration": False,
                    "symbolKind": {
                        "valueSet": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12,
                            13,
                            14,
                            15,
                            16,
                            17,
                            18,
                            19,
                            20,
                            21,
                            22,
                            23,
                            24,
                            25,
                            26
                        ]
                    }
                },
                "configuration": True
            }
        }
