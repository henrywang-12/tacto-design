# The sample world

Every template uses the same invented company, customers, suppliers and figures, so the pieces agree with each other. All of it is fiction and all of it must go: `scripts/tacto_check.py` fails a deliverable that still contains one of these names.

The pack is dated November 2026. "Current 12 months" on a product screen is December 2025 to November 2026.

| Role | Name | Facts the templates use |
|---|---|---|
| The sender (you) | Northdesk | "Northdesk agents"; 120 customers with about 460 production sites; €12B of spend read; 410,000 drawing parts priced, 37% of them bought above should-cost (the landscape cover); hello@northdesk.example |
| Reference customer (landing page, success story, article, square cover) | Auerberg Guss | a foundry: iron and aluminium casting; 6 sites in Germany and Czechia; 1,900 people; €210M purchasing volume, about €12M of it a year in machined drawing parts; 2,700 drawing parts from 140 suppliers; live since March 2026; €310,000 saved in 9 months, which is 3.4% of the about €9M bought in that time, against a target of 2%; RFQ rounds take 4 days instead of 11 (64% less) |
| Its head of purchasing | Jana Petrovic | one quote, the same words in the landing page, success story, article and deck: "For the first time we know what a part should cost before the supplier tells us. That changed every conversation we have." |
| Second customer | Lindqvist Hydraulik | hydraulics; €1.2M in price increases averted; Mats Lindqvist, head of purchasing, one quote on the landing page |
| Customer whose workspace the product screens show | Sentec Antriebe | drive technology and machine modules, so it buys housings, flanges and builds stations; €96.4M order volume in 2025, €91.8M in 2026; 1,864 active suppliers; 900 RFQs a year sent by agents; Carla Wiesner, head of purchasing, one quote on the landing page |
| Prospect (POV, deck) | Hollweg Präzision | buys 3,870 drawing parts from 214 suppliers; €86M purchasing volume; 7 buyers, 2 sites; 41% of parts above should-cost and €4.2M potential, from a first pass over twelve months of invoices; about €10M of turned parts, paid 11% above should-cost, so €1.1M a year too much (est.); realistic in year one €340K (est.), the 3.4% the reference customer reached; pilot: eight weeks on turned parts, 11 Jan to 5 Mar 2027, asking for drawings and order history because the invoices are already in. Its figures appear only in material made for Hollweg, never on a cover or a public page |
| Suppliers | Brenner Zerspanung, Kessler Drehteile | turning shops, stainless and C45. Brenner is the supplier page (€1.28M order volume, 1.4% of Sentec's spend; nine findings worth €108,548, all on turned parts or on the supplier as a whole) and the agent messages on the landing page; both appear in the deck table |
| The part | Bearing housing, 30458371 | called "Bearing housing" in every list and chip, described as "stepped, 6 holes" only in its own page title; turned from bar, 1.4404, Ø118 × 96, bought from Brenner; paid 212.40 €, target 201.80 € (5% above target, 10.60 € a piece); 930 pieces in four orders from Dec 2025 to Oct 2026, €197,230; finding "Paid price above target", potential €9,860, the newest of Brenner's nine |
| Its neighbours | Spindle nut 30458455, Coupling flange 11935544, Flange, turned 11935069, Bearing cover 30458402 | the same article number, finding and potential on the supplier page and in the part page's table of similar parts |

## When you write your own

- One set of facts per company. A customer has one number of sites, one industry, one size, one result, in every piece of a set. Write them down first, then write the pieces.
- A company has one role and one trade. A customer is not also a supplier in the next screen; a foundry does not buy castings; a turning shop does not supply sheet metal, and the index in its price talk is the metal it turns.
- A person says one thing. The same quote, word for word, wherever that person appears. A second quote needs a second person.
- Sums must work. A saving, a percentage and the spend it applies to have to agree over the same period (3.4% of the about €9M bought in nine months is €310,000). Units times price is the spend. A list that says 18 parts names 18, and a table's rows add up to its total.
- What you promise a prospect is no larger than what the reference customer proved. The gap you found is the potential; year one is the rate someone actually reached.
- A timeline is as long as it says: an eight-week pilot ends eight weeks after it starts, on working days, not over the holidays. Nothing is dated later than the pack itself, and "the last 12 months" ends this month.
- Do not ask for what you say you already have. If the analysis came from invoices, the next step asks for something else.
- The same record shows the same figure wherever it appears. If a part is on two screens, its price, target and finding are identical. A count of what is new is labelled as new, so it cannot be read as the total.
- "Similar" means similar: the same trade and form. A part is not listed among its own similar parts.
- Totals across customers fit the customers you show: 120 customers do not have 2,300 sites if the ones named have two to six.
- A figure about a real customer comes from that customer or is marked "(est.)". An invented figure is never presented as real.
- Nothing that names a customer's or a prospect's weakness goes on a public cover or post. A cover carries a market figure or the customer's own published result.
- No certificate, award or compliance claim unless the sender holds it. The check warns on every one.
