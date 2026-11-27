# The sample world

Every template uses the same invented company, customers, suppliers and figures, so the pieces agree with each other. All of it is fiction and all of it must go: `scripts/tacto_check.py` fails a deliverable that still contains one of these names.

| Role | Name | Facts the templates use |
|---|---|---|
| The sender (you) | Northdesk | "Northdesk agents"; 120 customers; hello@northdesk.example |
| Reference customer (landing page, success story, article, cover) | Auerberg Guss | a foundry: iron and aluminium casting; 6 sites in Germany and Czechia; 1,900 people; €210M purchasing volume, about €9M of it machined drawing parts; 2,700 drawing parts from 140 suppliers; live since March 2026; €310,000 saved in 9 months, which is 3.4% lower material cost on drawing parts against a target of 2%; RFQ rounds take 4 days instead of 11 (64% less) |
| Its head of purchasing | Jana Petrovic | quoted in the landing page, success story, article and deck |
| Second customer | Lindqvist Hydraulik | hydraulics; €1.2M in price increases averted; Mats Lindqvist, head of purchasing |
| Customer whose workspace the product screens show | Sentec Antriebe | drive technology and machine modules, so it buys housings, flanges and builds stations; €96.4M order volume in 2025, €91.8M in 2026; 1,864 active suppliers; 900 RFQs a year sent by agents |
| Prospect (POV, deck) | Hollweg Präzision | buys 3,870 drawing parts from 214 suppliers; €86M purchasing volume; 7 buyers, 2 sites; 41% of parts above should-cost; €4.2M potential, €1.1M in year one (est.); pilot: eight weeks, turned parts only |
| Suppliers | Brenner Zerspanung, Kessler Drehteile | turning shops. Brenner is the supplier page (€1.28M order volume, 0.7 to 1.4% of Sentec's spend), the agent messages and the article; both appear in the deck table |
| The part | Bearing housing, stepped, 30458371 | turned from bar, 1.4404, Ø118 × 96; paid 212.40 €, target 201.80 € (5% above target, 10.60 € a piece); 930 pieces a year, €197,230; potential €9,860 |

## When you write your own

- One set of facts per company. A customer has one number of sites, one industry, one size, one result, in every piece of a set. Write them down first, then write the pieces.
- A company has one role and one trade. A customer is not also a supplier in the next screen; a foundry does not buy castings; a turning shop does not supply sheet metal.
- Sums must work. A saving, a percentage and the spend it applies to have to agree (3.4% of about €9M is €310,000). Units times price is the spend. A list that says 18 parts names 18.
- A timeline is as long as it says: an eight-week pilot ends eight weeks after it starts.
- The same record shows the same figure wherever it appears. If a part is on two screens, its price, target and finding are identical.
- A figure about a real customer comes from that customer or is marked "(est.)". An invented figure is never presented as real.
- Nothing that names a customer's weakness goes on a public cover or post. Analyses stay anonymous unless the customer agreed.
- No certificate, award or compliance claim unless the sender holds it. The check warns on every one.
