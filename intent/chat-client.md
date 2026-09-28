# Intent: chat-client

## Goal
A command-line program that takes one question as an argument, sends it to a chat model through a configurable HTTP endpoint (typically OpenRouter), prints the model's answer, then prints a final line with the model name and the input and output token counts. One question, one answer, then it exits. No back-and-forth conversation.

## Who it is for
You, as a learning exercise. You want to see how to call an LLM API from scratch using only the standard library. Without it, you would open a browser and paste the question into a chat UI.

## Constraints
- Python, standard library only (no pip, no third-party packages). The project rule already enforces this.
- All provider configuration comes from environment variables: `CHAT_MODEL`, `CHAT_BASE_URL`, `OPENROUTER_API_KEY`. No CLI flags, no hardcoded defaults.
- Nothing about the provider should appear in the source. The code is a generic OpenAI-compatible chat completions client; pointing the env vars at a different endpoint should make it work without code changes.
- The token counts the program prints must match what the provider's usage record (OpenRouter's Activity page) shows for that request. The provider's record is the check; the program's own numbers are not evidence.
- Deadline: end of this lab week.
-The request sends two messages: a system message and the user's question. The system message is written in the source, not read from an environment variable, so changing it means editing the file.

## Not in scope
- Streaming. The full response is returned in one HTTP call and printed at once.
- Multi-turn conversation or message history. One user message, one assistant message, done.
- Function calling, image inputs, or other multimodal content. Text in, text out.
- A config file, saved state, or log file. The program only reads env vars and calls the API.
- More than one provider at a time. The program talks to whatever `CHAT_BASE_URL` points at, one destination per run.

## Success looks like
- Run `python3 chat.py "What is 2+2?"` with valid env vars set → stdout has the model's answer, then a final summary line with the model name, input tokens, and output tokens. Exit code 0.
- Unset `OPENROUTER_API_KEY` → the program exits non-zero with a message naming the missing variable.
- Set `CHAT_MODEL` to a name the provider doesn't know → the API error body is printed to stderr and exit is non-zero.
- Point `CHAT_BASE_URL` at a different OpenAI-compatible endpoint (with matching `CHAT_MODEL` and key) → it works without code changes.
- Manually verify on the provider's Activity page that the input and output token counts the program printed match the row for that request.

## Open questions
- Exact format of the summary line (e.g. `model=<name> input=<n> output=<m>` vs. a more verbose form). Settled in the spec.
- Whether to send any optional provider-specific request headers. Tentative answer: no, per the "nothing about the provider in the source" rule. Confirm in the spec.
- How to handle an empty-string `OPENROUTER_API_KEY` — treat as missing, or let the API reject it? Settled in the spec.
- Whether to set any request parameters other than `model` and `messages` (e.g. `temperature`, `max_tokens`). Tentative answer: no — leave everything else at provider defaults. Confirm in the spec.
- How to format the question: a single positional CLI argument, or join all positional args with spaces? Tentative answer: a single positional arg, errors if zero or more than one is given. Confirm in the spec.

### Decisions you deferred to me, recorded as agreed
- **Error handling.** The lab did not specify what the program does on failure. I proposed: on a non-2xx response, print the HTTP status code and the raw response body to stderr, then exit non-zero; on a connection error or timeout, print the exception message to stderr and exit non-zero; no retries. You agreed after I explained it.

**Approved by:** Kuany Kuany, 28/09/2026
