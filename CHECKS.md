# Checks

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| Question through OpenRouter | An answer and a usage line | Full sentence answer, then `--- model=minimax/minimax-m3 input=177 output=28`. Exit 0. | Pass |
| Usage record matches | Same model; same or close token counts | OpenRouter Logs, Sep 28 06:18 AM: MiniMax M3, 177 input, 28 output, $0.0000448. Identical to what the program printed. Provider shown as GMICloud. | Pass |
| System prompt changed | Answer style changes accordingly | Changed the system message to "Answer only in rhyming couplets." Input tokens dropped 177 to 136, confirming the system message reached the request. At max_tokens=300 the answer came back empty (printed `None`) with all 300 output tokens billed. Raising to 2000 produced actual couplets in 261 output tokens. | Pass |
| max_tokens = 20 | Truncated or empty answer; tokens still billed | Answer cut off mid-sentence at "...can process". 20 output tokens, $0.0000371 billed. Logs row at 06:17 AM confirms. | Pass |
| Model swapped (step 4) | Different model name in usage; answer may differ | Changed only CHAT_MODEL to openai/gpt-4o-mini, no code change. Usage line read `--- model=openai/gpt-4o-mini input=32 output=25`. The same question tokenized to 32 input tokens versus 177 on MiniMax M3. Both returned a correct one-sentence answer. | Pass |
| Local model (optional) | Answer from localhost; no OpenRouter entry | Not attempted. | n/a |
