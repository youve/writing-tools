# Writing Tools

These are some utilities I've created to aid in the writing process.

## Phrase Counter

`phraseCounter.py` My phrase counter is better than any other phrase counter online because:

* Word counters give you a useless list like "The", "in", "and", "a", "of".
* It finds all repeated phrases, not just ones of an exact length.
* It delivers the result sorted by both length and frequency.
* It doesn't give you redundant information. If it tells you that you repeated "Mary had a little lamb" twice, it won't tell you about "Mary had a little" or "had a little lamb" because you already know about those.

For example, the first two stanzas of Mary Had a Little Lamb:

```
5 words    mary had a little lamb  2 times
4 words    mary went mary went     2 times
4 words    little lamb little lamb 2 times
4 words    everywhere that mary went   2 times
1 words    was                   2 times
```

## Character sketch prompt

`mixnmatch.py` generates character based writing prompts in the form `Write about the most $adjective $person.` Examples: The calmest anthropologist, the drabest childcare worker, the most responsible tax inspector.