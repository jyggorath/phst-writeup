# Langfredag
20 points

### Table of contents
1. [The Task](#the-task)

## The Task
>Bruk av hjemmekontor
>Mange påskekyllingbetjenter jobber hjemmefra i disse dager. Rådfør deg med IT-avdelingen om du er i tvil om ditt utstyr. Det er viktig å sjekke at utstyret er sikkerhetsoppdatert og hvem som har fysisk adgang til hjemmekontoret ditt. Sjekk at hjemmenettverket ditt er sikkert konfigurert og benytt sterke og unike passord. Vær forsiktig med hvor du benytter tjenestetelefon. I noen fremmede makters eggeterritorier kan det være lett for disse makternes etterretningstjenester å ta seg inn i mobiltelefoner og nettbrett. En påskekyllingbetjents telefon kan gi god innsikt i PHSTs virke, og inneholde sensitiv informasjon.
>
>I et utenlandsk mobilnett vil all kommunkasjon til og fra enheten kunne avlyttes, uten at brukeren av mobiltelefonen kan oppdage det. PHST anser det som rimelig temmelig sannsynlig at slik kapasitet er etablert på permanent basis i mobilnettverkene og internett i fremmede makters eggedistrikt. PHST tilbyr sikkerhetsbriefer til påskekyllingbetjenter og andre offentlige tjenestepersoner i forkant av reiser til høyrisikoområder.
>
>Påskeegg bør ikke settes ut i områder under fremmede makters kontroll.
>
>Påskeharens Sikkerhetstjeneste er godt igang med å undersøke hva som kan ha skjedd med påskeeggene. Vi vet ikke hvor de er enda, men vi har fått et bilde av en samarbeidende tjeneste der eggene muligens oppbevares.
>
>Kan du se om du finner noe av interesse i bildet?
>
>Flaggformat: PHST{noe av interesse}

[Attachment: paskeegg_langfredag.png]()

## Solution
### Not stego
As the first task turned out to be simple stego, this next one will typically be something completely different. Also, as the image this time seems to have clues and details in it, I decided to not try stego right away, and instead investigate what the image shows visually.

### Resistor color codes
The paper in the picture reads "Resistor Color Code". Googling that, I found [this great resource](https://www.electronics-tutorials.ws/resistor/res_2.html)

The eggs in the picture have three colors each, and appearently, the three first colors on a resistor form three digits (cropped image):

![resistorgraph.png]()