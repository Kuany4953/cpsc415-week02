# Week 2 chat client

A command-line program that sends one question to a model through OpenRouter, prints the answer, then prints a final line with the model name and the input and output token counts.

## Running it

    export OPENROUTER_API_KEY="your-key"
    export CHAT_BASE_URL=https://openrouter.ai/api/v1
    export CHAT_MODEL="minimax/minimax-m3"
    python3 chat.py "In one sentence, what is a context window?"

Python 3, standard library only. No CLI flags, no defaults in the source. All three variables must be set or the program names the missing ones and exits non-zero.

## What I corrected in the intent draft

**The filename.** The draft said `chat-client.py`. The lab runs `python3 chat.py`, so building to the draft would have produced a program the handout's own command could not find.

**The missing system message.** The draft described sending only the question. Step 3 requires identifying two roles in the `messages` array and changing the system message, so I added a constraint saying the request carries both a system message and a user message, with the system text in the source rather than an environment variable.

## One line I can explain

`chat.py` line 20: `MAX_TOKENS = 300`

A named constant holding the ceiling on output tokens, passed into the request body on line 64. I changed it three times during the checks and the behavior changed each time.

## The two models

MiniMax M3 and GPT-4o-mini, same question, same system message, no code change between runs. Only `CHAT_MODEL` changed.

Both answered correctly in one sentence. MiniMax M3 cost $0.0000448; GPT-4o-mini cost $0.0000198.

The token counts were not comparable: the identical request tokenized to 177 input tokens on MiniMax M3 and 32 on GPT-4o-mini. This is one question on one run, not a benchmark.

## Things I noticed

With the system message set to "Answer only in rhyming couplets" and `max_tokens` at 300, the program printed `None` and the usage line reported 300 output tokens. MiniMax M3 spent its whole output budget on hidden reasoning without emitting visible text. Raising the limit to 2000 produced the couplets in 261 tokens, against 28 for the same question under a plain system prompt.

Printing the bare word `None` is a rough edge. The program prints whatever is in the content field, and the field was null. A clearer message would say the response was empty.

`urllib` failed with a certificate verification error until I ran Python's `Install Certificates.command`. That installs a certificate bundle into the Python environment; it is not a package the program imports, and `chat.py` remains standard library only.

## Local model

Not attempted.
