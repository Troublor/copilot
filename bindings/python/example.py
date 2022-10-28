import os
from typing import Any

from service import CopilotService, CompletionRequestParams


def main():
    service = CopilotService(os.path.dirname(__file__))

    service.sign_out()

    def cb(msg: Any):
        print(msg)
        input("Press Enter to continue...")
        print("Checking authorization status...")

    service.sign_in(cb)

    param = CompletionRequestParams(__file__, "python",
                                    {"line": 18, "character": 55})
    resp = service.get_completions(param)
    print(resp)
    service.shutdown()


if __name__ == "__main__":
    main()
