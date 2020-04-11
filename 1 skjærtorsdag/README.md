# Skjærtorsdag
10 points

### Table of contents
1. [The task](#the-task)
2. [Solution](#solution)
	1. [Stego](#stego)
	2. [Caesar cipher](#caesar-cipher)

## The task
>Etter sin daglige luftetur oppdaget Påske HAREN at alle påskeeggene han hadde gjort klar til utdeling var blitt stjålet. Da han så de sist var de i kurven trygt sortert, organisert og klar til utdeling, men plutselig var de ikke der lenger. Senere fikk Påske HAREN tilsendt et bilde. Kanskje det ble tatt av den som stjal eggene? 🥚🐇
>
>Kan du analysere bildet og se om det er noe muffens? 🧁
>
>Flaggformat: PHST{muffens}

[Attachment: skjrtorsdag.png](skjrtorsdag.png)

## Solution
### Stego
View the file in a text or hex editor. The flag is located at the very end, just before the file trailer.

![stego.png](stego.png?raw=true)

Or you can just `strings` the file, and grep on '{'/'}' (which we know will be in the flag).

```
user@host:~/phst$ strings skjrtorsdag.png | grep "{"
[...(1884 lines of gibberish omitted)...]
/{+z5
eN{h
?{!o
{i7(5|L
CUFG{Qrer_snatre_zrt_nyqev!!}
user@host:~/phst$
```

### Caesar cipher
`CUFG{Qrer_snatre_zrt_nyqev!!}` is clearly a flag, but also clearly scrambled in some way. Let's rule out the simplest solution first.

![caesar.png](caesar.png?raw=true)

And what do you know, it was ROT13.

**The flag is:** `PHST{Dere_fanger_meg_aldri!!}`