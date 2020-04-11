# Påskeaften
20 poeng

### Table of contents
1. [The Task](#the-task)
2. [Solution](#solution)
	1. [Emoji reference](#emoji-reference)
	2. [DNS](#dns)
	3. [The hint: DNS LOC](#the-hint-dns-loc)

## The Task
>Påskeegg på avveie: PHST har mistanke om at et dusin påskeegg er på avveie. Det er grunn til å mistenke at fremmede makters hackere står bak.
>
>Påskeharens Sikkerhetstjeneste er godt igang med å undersøke hva som kan ha skjedd med påskeeggene. Det viser seg at skurkene har vært inne på serverene til Påske HAREN og lagt igjen flere spor. Ett av disse leder til en adresse 1F423.com.
>
>Kan du se om du finner noe mystisk med adressen?
>
>Flaggformat: PHST{noe mystisk}
>
>(Unlock Hint for 5 points)

## Solution
### Emoji reference
1f423 appears to refer to the "hatching_chick" emoji: 🐣. However this turned out to not be relevant for the rest of the task, and most likely just an easter egg (no pun intended).

### DNS
The domain 1F423.com [is registered](https://who.is/whois/1f423.com), but doesn't appear to have an IP address assiciated with it. DNS lookups returns little info, ANY requests are blocked and returns the reference to [RFC8482](https://tools.ietf.org/html/rfc8482). Going through all the usuall DNS record types yield only hits on NS, SOA and TXT:

```
NS	1f423.com	anastasia.ns.cloudflare.com
NS	1f423.com	cameron.ns.cloudflare.com
SOA	1f423.com	anastasia.ns.cloudflare.com	dns.cloudflare.com
TXT	1f423.com	These aren't the droids you're looking for
```

Based on the TXT record I tried probing for various sub domains using Star Wars references, but found nothing.

### The hint: DNS LOC
Hitting a dead end, I spent 5 points and got the hint. It was simply: "RFC1876".

[RFC1876 is a standard for "Expressing Location Information in the Domain Name System"](https://tools.ietf.org/html/rfc1876). This DNS record type was not listed on any of the lookup-tool websites I visited, and I hadn't heard of it before. Sending a request for LOC record did indeed yield a set of coordinates:

```
user@host:~/phst$ host -t loc 1f423.com
1f423.com location 60 47 34.900 N 11 6 3.600 E 0.00m 0.00m 0.00m 0.00m
user@host:~/phst$
```

After changing the format of the coordinates into something Google Maps can read ("60°47'34.9"N 11°06'03.6"E"), I got the following location:

![vikingskipet.png](vikingskipet.png?raw=true)

**The flag is:** `PHST{Vikingskipet}`