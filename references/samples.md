# The sample world

Every template uses the same invented company, customers, suppliers and figures, so the pieces agree with each other. All of it is fiction and all of it must go: `scripts/tacto_check.py` fails a deliverable that still contains one of these names.

| Role | Name | Facts the templates use |
|---|---|---|
| The sender (you) | Northdesk | "Northdesk agents"; 120 customers; hello@northdesk.example |
| Reference customer | Auerberg Guss | iron and aluminium casting; 6 sites in Germany and Czechia; 1,900 people; €210M purchasing volume; 2,700 drawing parts from 140 suppliers; live since March 2026; €310,000 saved in 9 months; material costs on drawing parts 3.4% lower against a target of 2%. Also the workspace in the product screens. |
| Its head of purchasing | Jana Petrovic | quoted in the landing page, success story, article and deck |
| Second customer | Lindqvist Hydraulik | hydraulics; €1.2M in price increases averted; Mats Lindqvist, head of purchasing |
| Third customer | Sentec Antriebe | drive technology; 900 RFQs a year, 70% less time per RFQ |
| Prospect (POV, deck, cover) | Hollweg Präzision | buys 3,870 drawing parts from 214 suppliers; €86M purchasing volume; 7 buyers, 2 sites; 41% of parts above should-cost; €4.2M potential, €1.1M in year one (est.) |
| Suppliers | Brenner Zerspanung, Feldmark Stanztechnik | turned parts and sheet metal; the supplier page, the agent messages, the deck table |
| The part | Bearing housing, stepped, 30458371 | turned from bar, 1.4301; paid 179.20 €, target 170.20 € (5% above target); about 1,095 pieces a year; potential €9,860 |

## When you write your own

- One set of facts per company. A customer has one number of sites, one industry, one result, in every piece of a set. Write them down first, then write the pieces.
- A company has one role. A customer is not also a supplier in the next screen.
- A figure about a real customer comes from that customer or is marked "(est.)". An invented figure is never presented as real.
- No certificate, award or compliance claim unless the sender holds it. The check warns on every one.
- Engineering details must agree: a part turned from bar is not filed under castings; a price 5% above target is not called 18% elsewhere.
