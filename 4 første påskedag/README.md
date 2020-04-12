# Første påskedag
20 points

### Table of contents
1. [The Task](#the-task)
2. [Solution](#solution)
	1. [The PCAP](#the-pcap)
	2. [SSL key log](#ssl-key-log)
	3. [Finding the document](#finding-the-document)

## The Task
>Oppdatert påskevurdering: Det er MULIG at det blir en god påske. Situasjonen rundt påskeeggene er fortsatt uavklart. Ytterligere 50 påskeegg er forduftet. I tillegg er Påske HAREN sykemeldt. For å utelukke fjærallergi må PHSTs påskeeggproduksjonsanlegg renses umiddelbart for alle fjær og alle påskekyllingbetjenter bes utøve ekstra renslighet de kommende dagene.
>
>PHST har mottatt informasjon fra samarbeidende påsketjeneste om en pågående rekognoseringskampanje mot dem.
>
>Varselet gjelder én datamaskin, og det opplyses om at det i tillegg til rekognoseringsaktiviteten SANNSYNLIGVIS er minst én aktør til som har fått fotfeste på maskinen
>
>På grunn av klementin i syslog-serveren, er loggene fra applikasjonene dessverre borte. Det eneste datagrunnlaget som er igjen er en kort pakkedump fra IDS'et.
>
>Klarer du å finne ut av hva slags informasjon aktøren har fått tak i?
>
>Flaggformat: PHST{Tittel i dokument}

[Attachment: mistenkelig.pcap](mistenkelig.pcap)

## Solution
### The PCAP
Looking at the capture data in Wireshark, these are the first early assumptions that can be made:
* The main "client" on the network appears to be 192.168.136.129
* The traffic consists mainly of TLS encrypted HTTPS traffic, in addition to "background traffic" (e.g. SSDP, NTP, ARP). Also there's DNS (and MDNS and LLMNR)
* The external hosts in the HTTPS traffic appears to be linked to Twitter, Google, yr.no and nrk.no.

### SSL key log
After looking through and filtering out traffic, something stands out. The "main client" has TCP communication with another host in the network, on what appears to be a custom port: 192.168.136.131:31337.

Contrary to the HTTPS traffic, these TCP packets contain plaintext. And *very interesting* plaintext as well:

![keytraffic.png](keytraffic.png?raw=true)

The presence of keywords such as CLIENT_HANDSHAKE_TRAFFIC_SECRET peaked my interest. A quick Google search revealed that this is data from [logging of SSL/TLS keys in Chrome/Firefox/cURL](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/NSS/Key_Log_Format).

This is what the full TCP stream looks like:

![keytcpstream.png](keytcpstream.png?raw=true)

More googling revealed that this information can be used to decrypt the HTTPS traffic. Here's a quick guide for how to do this:
1. Save the entire TCP stream in a text file.
2. Right click on any TLS packet (that is part of the HTTPS traffic) where the "Info" field contains something like "Application Data, Application Data", select **Protocol Preferences** and then **(Pre)-Master-Secret log filename...** [(screenshot)](howto_decrypt_1.png).
3. Browse to and select the file saved in stage 1 for **(Pre)-Master-Secret log filename** [(screenshot)](howto_decrypt_2.png).
4. Voilà [(screenshot)](howto_decrypt_3.png).

### Finding the document
As stated earlier, the HTTPS traffic is primarily to Twitter, Google, yr.no and nrk.no. After decrypting the HTTPS traffic, it is appearent that all this originates from the user visiting and browsing yr.no. The Google traffic is Google search traffic from the autocomplete when he/she first types the address, as well as Google Analytics, and the requests to Twitter and nrk.no are both related to yr.no as well.

Combing through the browsing looking for something that could look like a flag did not imediatly yield any results. When faced with such issues, I have learned to go back and re-read the task description. Doing so, I found the following clue:
>Flaggformat: PHST{Tittel i dokument}
*(English: Flag format: PHST{Title in document})*

So I'm looking for the title of a document. Initially this had me starting to look for values in HTML title tags, but as most of the web resources requested is images and javascript and so on (not HTML), I went through the traffic looking at the mime types of the responses. As I did so, I found a request/response with mime type application/pdf: <https://www.yr.no/place/Norway/Innlandet/Hamar/Vikingskipet/forecast.pdf>

Submitting "forecast.pdf" as flag was wrong, but submitting the title *within* the document worked.

**The flag is:** `PHST{Weather forecast for Vikingskipet}`