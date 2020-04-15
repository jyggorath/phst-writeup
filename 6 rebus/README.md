# Rebus
10 points

### Table of contents
1. [The Task](#the-task)
2. [Solution](#solution)

## The Task
I forgot to copy the task text for this "challenge" before the CTF was taken down. In short, this is what the task consisted of:

For every challenge solved, a "rebusord" (Norwegian for "rebus word") was made available. The rebus word consisted of something like: `echo = "a3f6ce4eb662e4797a39b"` or `bravo = "19de0b5a1eeef635c2b4fec6e7c7"`. After having solved all the main challenges, an extra challenge appeared, called "Rebus". It presented the contester with instructions somewhat like this:
```
url = "https://www.phst.no/" + alfa + bravo + charlie + delta + echo + ".html"
```

## Solution
Putting it all together resulted in the following URL:

`https://www.phst.no/0c405bdf5899c3db8ba0d1909f919de0b5a1eeef635c2b4fec6e7c7664150457e1f2ccc339903074978df7930e256789cb87ea67358a3f6ce4eb662e4797a39b.html`

The page at that URL looks like this:

![screenshot.png](screenshot.png?raw=true)

Translated into English, the text reads:

>Congratulations! 🙋‍♀️
>
>🏆 You completed all the tasks! 🏆
> 
>It seems Pen Gwyn 🐧 from PST's Christmas calendar managed to sneak into the Easter BUNNY and steal the eggs. Hope you appreciated the Easter nuts and that you learned something! 🤗
>
>If you're interested in other exciting challenges, perhaps you will consider applying to some of our available job positions?
>
>Visit https://pst.no/jobb to view available job positions at the PST.
>
>RATHER SECRET flag: PHST{You completed the SHAbus, very nice work!}

(Easter nut is a Norwegian term for an Easter tradition which involves quizzes/brain teasers)

**The flag is:** `PHST{Du klarte SHAbussen, veldig bra jobba!}`