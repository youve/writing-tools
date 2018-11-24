These are some utilities I've created to aid in the writing process.

`mixnmatch.py` generates character based writing prompts in the form `Write about the most $adjective $person.` Examples: The calmest anthropologist, the drabest childcare worker, the most responsible tax inspector.

`phraseCounter.py` unlike word counters that tell you that "the" is the most common word in your writing, which is what you would expect for any English text, phraseCounter looks for repetitions of longer phrases in a text file, your clipboard contents, or a text you have typed in. Then it tells you the top 10 longest phrases that occurred the most often, skipping substrings of phrases it has already told you about because they are redundant.

For example, the first two stanzas of "Mary Had a Little Lamb" produce this result:

5 words    mary had a little lamb  2 times
4 words    mary went mary went     2 times
4 words    little lamb little lamb 2 times
4 words    everywhere that mary went   2 times
1 words    was                   2 times