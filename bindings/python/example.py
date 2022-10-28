from service import CopilotService, CompletionRequestParams


def main():
    service = CopilotService("/Users/troublor/troubterm")
    param = CompletionRequestParams("/Users/troublor/troubterm/commands/disable.ts", "typescript",
                                    {"line": 26, "character": 9})
    resp = service.get_completions(param)
    print(resp)
    service.shutdown()
    resp = service.get_completions(param)


if __name__ == "__main__":
    main()
