# Daily Standup - 18 december 2025

## Очищенная версия с разделением по ролям

**Участники** (определено по контексту):

- **Ведущий (Lead)** — ведёт daily, задаёт вопросы, распределяет работу
- **Dev 1** — работает над acceptance link, deploy preview
- **Dev 2** — работает над белым экраном после релиза
- **Alex** — работает над Mobilot surveys и ticket 10-9619, учит нидерландский
- **Dev 3** — работает над Terminal Tool, POC → repo
- **Mike** — присоединился позже, будет тестировать Corp ticket

---

## 00:00 — Начало встречи

**Ведущий:** Het scherm knipt de hele tijd, dus jongens, ik denk dat het gelukt
is. Jongens, kan beter, alleen kunnen we nog niet verschuiven. Oh ja,
goedemorgen! Daily in het Nederlands! Want het is donderdag — de leukste dag van
de week.

**Dev 1:** Nou nou. Oh, hij is al weg. Ja, is goed nu toch?

**Ведущий:** Oké, let's go! Emergency... oh nee, dat is gewoon... Mike is er
wel. Die weet natuurlijk niet dat we nu de daily hebben.

_(Roepen naar Mike)_

**Ведущий:** Mike! Melvin! Die zoekt z'n bureau. Hey Mike! Hallo!

**Mike:** Hallo!

**Ведущий:** Laat jou even op de hoogte stellen: de daily is vandaag in het
Nederlands, vanwege de IT all-hands. We proberen langzamer te praten dan
normaal, maar daar heb ik zelf ook moeite mee.

---

## 01:50 — Ticket updates

### Acceptance link na wijzigen

**Dev 1:** De acceptance link staat na wijzigen. Ik ben daar mee bezig. Moet de
Deploy Preview ook in de app gezet worden?

**Ведущий:** Nee, dit gaat los van de app.

**Dev 1:** Want ik heb hem gewijzigd, maar in de app staat hij nog in het
Engels. Hoe test ik dat dan? Het idee is dat de wijziging op de ene plek ook de
andere plek wijzigt.

**Ведущий:** Dat klopt, alleen is het lastiger te testen. Wat je kan doen: je
taalvoorkeur weghalen of op een andere taal zetten in je browser, dan de taal
weghalen uit je applicatie, terugkomen en kijken of hij de taal van de backend
pakt.

**Dev 1:** Oké, dat zou kunnen. Had ik nog niet over nagedacht. Die ticket
eronder zou makkelijker moeten zijn. Ben ik nog niet aan begonnen, maar komt
hierna.

---

### Interface release

**Ведущий:** Interface release — Suus, wat heb je? Je neemt het op, goed om te
weten.

**Suus (off-screen):** _(не слышно)_

**Ведущий:** De interface release ligt bij Suzanne, dus even wachten op haar
feedback.

---

### Straatparkeren-tegel

**Ведущий:** Straatparkeren-tegel ga ik vandaag reviewen.

---

### Wit scherm na release

**Ведущий:** "Na release zien gebruikers wit scherm" — ben je mee bezig?

**Dev 2:** Ja. Ik zag dat er tussen 12 en 4 geen meetings zijn.

**Ведущий:** Voor jou niet, voor mij niet?

**Dev 2:** Nee, nou lekker! Ik ben ermee bezig.

---

### Fetch surveys for Mobilot (FJ-797)

**Alex:** Gisteren heeft iemand de review gedaan. Hij heeft een paar comments
achtergelaten en ook bugs gevonden. Ik denk dat het niet veel werk is. Ik kan
het vandaag afmaken, misschien duurt het een paar uur.

**Ведущий:** Heel goed bezig!

---

### Redesign toaster

**Dev 3:** "Redesign toaster" ben ik vanochtend aan begonnen. Ga ik mee verder.

---

### Opgeslagen taal ophalen na inloggen

**Ведущий:** Daar is feedback op geweest. Ik neem aan dat Vest die aan het
oppakken is, daarom staat hij "In Progress".

---

### Terminal Tool

**Dev 3:** Ik ben gisteren begonnen met het overzetten van de POC naar de nieuwe
repo. Ik ben aan het tweaken, het moet nog getest worden.

**Ведущий:** Misschien kunnen wij hier straks naar kijken. Er hangt nog geen
feature aan. Kennet heeft zijn Epic aangemaakt, dus we kunnen features maken en
overleggen wat we willen. Dan klopt het ook qua uren schrijven.

**Dev 3:** Ik zal nadenken welke componenten erbij komen. We gaan straks toch
naar een bord met labels, dus dan maakt het niet meer uit.

**Ведущий:** Nog iets te zeggen over Todo? Ik denk het niet, we zijn net
begonnen.

---

### Ticket 10-9619

**Alex:** Hier is een kleine notitie over ticket 10-9619. Er is niet veel
voortgang. Ik wilde alles in één keer upgraden, maar dat lukt niet. Dus ik heb
een andere strategie gekozen: nu doe ik het in kleine stapjes, stap voor stap,
kleine incrementen.

**Ведущий:** Helemaal goed. Top!

---

### IO-16002 (Corp ticket)

**Ведущий:** Het staat niet op dit bord, maar IO-16002, de Corp-ticket — die ga
ik vanmiddag met Mike testen.

---

## 07:15 — Afsluiting en vakanties

**Ведущий:** Kerstfeest, iets anders nog voor vandaag? IT all-hands, andere
meetings?

**Dev 1:** Voor mij: afronden voor vakantie. Na vandaag ben ik 2,5 week weg.
Bijna drie weken zelfs!

**Dev 2:** Voor mij geldt hetzelfde. Ik heb niks opgepakt, dus hoef niks af te
ronden. Ik heb alles overgedragen. Het kan zijn dat Rafal en Paul aangehaakt
worden komende twee weken.

**Ведущий:** Denk er ook over na: heb je nog iets nodig?

**Dev 2:** Komende twee weken zijn er Erik en jij. Jij gaat ook dingen afronden,
dan is er niks meer lopend.

**Dev 3:** Nee, ik ben ook niet met iets bezig. Als het niet lukt af te ronden,
is het ook geen ramp.

**Ведущий:** In-Sprint ticket, dus ik heb geen dingen die anderen moeten weten.
De komende twee weken ben ik alleen maandag en dinsdag er, want kerst. Als er
belangrijke dingen zijn, weten jullie me te vinden.

---

## 08:47 — Workload verdeling

**Ведущий:** Veel plezier de komende twee weken! Qua workload voor Vers en Sven:
ik ben nog dingen aan het zoeken. Ik heb in ieder geval één ticket. Als Sven
iets kan oppakken van AppShell, zou dat leuk zijn. Voor Vers heb ik ook nog een
ticket.

**Dev 1:** Ik moet vandaag nog verder zoeken, staat op mijn to-do. Ik zal zorgen
dat jullie een lijstje krijgen.

**Ведущий:** Top! Deel gewoon dingen erbij. Stuur het even in de chat. Sven
heeft trouwens ook vakantie, twee weken niet, dus alleen Vers. Thomas is wel
volledig aanwezig.

---

## 09:39 — Einde

**Ведущий:** Oké, top! Komt helemaal goed. Nice! Dan kunnen we zo lekker gaan.
All-hands, 10 minuten werken, koffie halen!

De meeting duurde 10 minuten.

**Ведущий:** Dank allemaal!

**Iedereen:** Jij ook bedankt!

**Ведущий (tegen Alex):** Tot snel! Nederlands, zeg! Goed, jongen, echt knap!
Wordt steeds beter, echt goed!

---

## Samenvatting

| Ticket                   | Eigenaar       | Status                     |
| ------------------------ | -------------- | -------------------------- |
| Acceptance link wijzigen | Dev 1          | In progress, testen lastig |
| Interface release        | Suzanne        | Wachten op feedback        |
| Straatparkeren-tegel     | Ведущий        | Review vandaag             |
| Wit scherm na release    | Dev 2          | In progress                |
| Mobilot surveys (FJ-797) | Alex           | Bijna klaar, paar uur werk |
| Redesign toaster         | Dev 3          | Vanochtend begonnen        |
| Taal ophalen na inloggen | Vest           | In progress                |
| Terminal Tool            | Dev 3          | POC → repo, tweaken        |
| 10-9619                  | Alex           | Kleine stapjes strategie   |
| IO-16002 (Corp)          | Ведущий + Mike | Testen vanmiddag           |

### Vakantieplanning

- **Dev 1**: 2,5-3 weken weg vanaf vandaag
- **Ведущий**: Alleen ma/di komende 2 weken
- **Sven**: 2 weken vakantie
- **Thomas**: Volledig aanwezig
- **Vers**: Aanwezig (krijgt extra tickets)
