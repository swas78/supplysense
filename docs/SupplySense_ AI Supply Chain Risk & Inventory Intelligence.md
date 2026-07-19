# Tanishkka

**Should-Have Features (from the problem statement)**

**Data & Monitoring**

1. Multi-source data ingestion — suppliers, warehouses, purchase orders, inventory systems, logistics providers, external data  
2. Real-time inventory monitoring across multiple warehouses/distribution centers (Multi-warehouse inventory monitoring dashboard)  
3. Shipment delay detection with downstream business impact estimation and reasoning

**Prediction & Intelligence**  
 4\. Stock shortage / overstock prediction using historical demand and inventory trends ((rule-based \+ LLM explanation))  
 5\. Abnormal demand spike detection (seasonality, promotions, external events)  
 6\. Continuous supplier reliability scoring (delivery performance, lead times, quality, fulfillment rate history)  
**Decision Support & Recommendations**  
 7\. Alternate supplier/warehouse recommendations during disruption  
 8\. Inventory allocation prioritization under constrained stock  
 9\. Procurement recommendations based on forecasted demand (reorder quantity \+ deadline)  
**Reporting & Interface**  
 10\. Unified real-time dashboard combining inventory shortages, supplier risk scores, shipment delays, warehouse utilization, demand forecasts, service-level impact  
 11\. Auto-generated executive summaries with mitigation strategies  
 12\. Natural language querying interface for ops teams (the core differentiator)

**Polish / Stretch Features (only with hours to spare)**

1. Interactive filtering (by warehouse, product category, date range)  
2. Historical trend charts (demand over time, supplier score over time)  
3. Simulated alerts (mock "Slack alert sent" / "Email sent to procurement" toast)  
4. Visual/branding polish pass  
5. Multi-turn memory in the NL query box (only if everything above is already done)

**Additional Features to Consider (and why)**

| Feature | Why it adds value |
| :---- | :---- |
| **Root-cause / causal chain analysis** | Ops teams don't just need "what's wrong" — they need "why," e.g., tracing a stockout back to a specific delayed PO or a supplier's raw-material issue. This turns the dashboard from descriptive to diagnostic. |
| **Automated alerting with severity tiers (push/email/Slack/Teams)** | Dashboards are pull-based; disruptions need push-based alerts so decision-makers act before customer impact, not after login. \[already planned this as a mocked toast notification — just add color-coded severity (critical/high/medium) to it. Trivial addition.\] |
| **Scenario simulation / "what-if" engine** | Lets planners test "what if Supplier X fails" or "what if demand spikes 30%" before it happens — shifts the tool from reactive/predictive to prescriptive planning. |
| **Automated workflow triggers (not just recommendations)** | E.g., auto-drafting a PO to an alternate supplier or auto-triggering a stock transfer request for human approval — reduces time-to-action, which is often the real bottleneck, not the insight itself. |
|  |  |
|  |  |
| **Confidence scores on every prediction** | Forecasts and risk scores without confidence intervals get either blindly trusted or ignored; showing model confidence builds calibrated trust in a decision-support tool. |
|  |  |
| **Role-based views (procurement vs. logistics vs. C-suite)** | A warehouse manager and a CFO need very different slices of the same data; single dashboard for all roles usually gets ignored by someone. |
|  |  |
| **Audit trail / explainability log** | For regulated industries (pharma, food) and for building trust in AI recommendations — "why did the agent suggest Warehouse B?" needs a traceable answer. |

**Differentiating Factors**  
**1\. Disruption Cascade Simulator**

**What it is:** Instead of showing a delay as an isolated event, the system traces what it actually touches downstream — which products, which warehouses, which pending orders. **How it works:**  
Shipment delayed (Supplier A → Warehouse 2\)  
        ↓  
System checks: which products does this shipment carry?  
        ↓  
Checks: which of those products are already low in Warehouse 2?  
        ↓  
Checks: which pending orders depend on that stock?  
        ↓  
Output: "This delay puts 3 pending orders at risk of stockout within 4 days."  
**Why it's powerful:** Most tools show "shipment is late." SupplySense shows the actual chain reaction, which is what operations teams are trying to prevent in the first place.

**2\. Cost-of-Delay Translator**

**What it is:** Every risk flag gets converted into an estimated financial impact, not just an operational one. **How it works:** Combine the at-risk order value, the product's margin, and the estimated delay length into a rough ₹ figure — "Estimated impact if unresolved: ₹X in delayed/lost revenue." **Why it's powerful:** Judges and business-minded evaluators respond to numbers that translate straight into money. It reframes the tool from "an ops dashboard" to "a decision-support system a CFO would actually read."

**3\. Recovery Resilience Score**

**What it is:** A second layer on top of the standard reliability score — not just "how often does this supplier deliver on time," but "how fast do they recover after they don't." **How it works:** Track the gap between a missed delivery and the next on-time delivery in the historical data. A supplier that recovers in 2 days scores very differently from one that stays disrupted for 3 weeks, even if their average reliability looks similar on paper. **Why it's powerful:** Two suppliers can have the same reliability score for very different reasons. This surfaces the difference that actually matters when choosing an alternate supplier mid-disruption.

**4\. Silent Stockout Radar**

**What it is:** A feed of products that are heading toward stockout but haven't been flagged as "critical" yet — the ones that would normally be missed until it's too late. **How it works:** Instead of only alerting once a product crosses the critical threshold, the system surfaces anything trending toward that threshold faster than expected, ranked by how soon it will cross it. **Why it's powerful:** This is the difference between a system that reacts and one that actually anticipates, which is the exact goal stated in the problem statement.

**5\. What-If Scenario Engine**

**What it is:** A simple simulation box where the ops team can type a hypothetical — "What if Supplier A's capacity drops 20% next week?" — and see the network-wide effect before it happens. **How it works:** Take the question, adjust the relevant variable in the dataset temporarily, re-run the shortage/risk logic, and summarize the new state in plain language via the LLM. **Why it's powerful:** It moves the tool from "here's what's happening" to "here's what would happen if," which is a genuinely rare feature in a hackathon-scale build and demos very well.

**6\. Decision-Ready Intelligence**  
**What this means in simple language:** Most dashboards hand the operations team a wall of numbers and expect them to figure out what to do next. SupplySense never shows a risk without also showing the recommended action and its estimated cost of inaction next to it. The output isn't "here's your data" — it's "here's the one thing to do next, and here's what it costs you if you don't." Every screen ends in a decision, not just a chart.

**7\. The 7-Day Lookahead**  
**What this means in simple language:** Every supply chain dashboard on the market defaults to showing today's state — what's low right now, what's late right now. SupplySense's default view is the forecasted state a week out, with today's snapshot as the secondary layer underneath it. The entire product is built around the idea in the problem statement itself: anticipate disruptions, don't just react to them. The dashboard's first screen literally answers "what breaks next week if nothing changes," before it answers "what's broken today."

**8.From Insight to Action in One Click — Autonomous Mitigation, Not Just Alerts.**  
Most competing "supply chain intelligence" tools stop at prediction and dashboards — they tell you something is wrong and leave execution to humans, who are often the actual bottleneck during a live disruption.  
The differentiator: position this as a closed-loop agent, not just an analytics layer. When a disruption is predicted, the agent doesn't just recommend — it pre-stages the action (drafts the alternate-supplier PO, reserves capacity at a backup warehouse, drafts the customer-facing delay communication) and routes it for one-click human approval.

# Swastik

### **What is SupplySense, in one line?**

An AI system that watches a company's entire supply chain 24/7, predicts problems before they happen, tells decision-makers what to do about it, and lets them just *ask questions in plain English* instead of digging through dashboards.

### **The Simple Analogy**

Think of it like a **smart doctor for your supply chain**:

* It constantly checks your "vitals" (stock levels, shipments, suppliers)  
* It predicts problems before symptoms show ("you'll run out of X in 5 days")  
* It suggests treatment ("switch to supplier Y" / "reorder Z units now")  
* You can just ask it questions instead of reading test reports yourself

### **The 4 Layers (How It Actually Works)**

**1\. Data Ingestion — "Gathering all the vitals"**  
 Pulls data from suppliers, warehouses, POs, inventory, logistics carriers, and external sources (weather, news). Normalizes it all into one clean format.

**2\. Analysis & Prediction — "Reading the vitals"**  
 Runs continuously (not on-demand) to:

* Monitor inventory levels  
* Predict shortages/overstock  
* Detect abnormal demand spikes \+ explain why  
* Detect shipment delays \+ estimate who gets hurt

**3\. Risk & Recommendation — "The diagnosis \+ prescription"**

* Scores every supplier's reliability  
* Recommends alternate suppliers/warehouses during disruption  
* Prioritizes who gets limited stock  
* Suggests what to procure and when

**4\. Interface — "Talking to the doctor"**

* Real-time dashboard  
* Auto-written executive summaries  
* Natural language chat ("Which suppliers will miss delivery next week?")

### **All the Screens (Mandatory)**

| Screen | Purpose |
| ----- | ----- |
| **Main Dashboard** | Overview: shortages, supplier risk, delays, warehouse utilization, forecasts, service-level impact |
| **Inventory Screen** | Stock levels per warehouse/SKU, shortage/overstock flags |
| **Supplier Risk Screen** | Ranked scorecard of all suppliers (color-coded: green/yellow/red) |
| **Shipment Delay Screen** | List of delayed shipments \+ downstream impact (which orders/customers affected) |
| **Recommendations/Alerts Feed** | Proactive cards: "Supplier X delayed → switch to Supplier Y" |
| **Procurement Suggestions Screen** | What to reorder, how much, from whom |
| **Executive Summary View** | Auto-generated plain-English report of today's risks |
| **Chat/NLQ Screen** | Ask questions, get answers, conversational interface |
| **Data Integrations Screen** (admin) | Shows connected sources, sync status, data freshness |

---

### **Mandatory Features Checklist**

* Multi-source data ingestion (real APIs for weather/news, simulated for ERP/WMS/carrier)  
* Real-time inventory monitoring across warehouses  
* Demand forecasting model (shortage/overstock prediction)  
* Anomaly/demand-spike detection with cause attribution  
* Shipment delay detection \+ business impact estimation  
* Supplier reliability scoring (delivery, lead time, quality, fulfillment rate)  
* Alternate supplier/warehouse recommendation engine  
* Inventory allocation prioritization logic  
* Procurement recommendation generator  
* Live dashboard with all key metrics  
* Auto-generated executive summary  
* Natural language query interface  
  


### What Could Make You WIN — USP & Differentiator Ideas

Most teams building this will stop at "dashboard \+ forecasting model." Here's what separates a winning build from a generic one:

**1\. Explainable recommendations, not black-box answers**  
 Every "switch to Supplier Y" suggestion should show *why* — "Supplier Y has 96% on-time rate vs. 71% for current supplier, and 2-day shorter lead time." Judges trust systems that show reasoning, not just conclusions.

**2\. Live external signal correlation (real demo wow-factor)**  
 Actually pull real weather/news data and show the system connecting "storm near Warehouse 3" → "predicted delay" → "recommended reroute." This is the single easiest way to make the demo feel alive instead of staged on fake CSVs.

**3\. One killer end-to-end scenario, demoed live**  
 Instead of showing 20 features shallowly, script ONE full disruption story (e.g., "supplier delay → predicted stockout → recommended alternate supplier → auto-generated exec summary → you ask the chatbot and it confirms") and walk judges through it live. This proves the loop actually works, not just individual pieces.

**4\. The chat interface should feel genuinely agentic**  
 Don't just do simple Q\&A — let it chain reasoning: ask "what's causing today's biggest disruption?" and have it pull from multiple layers (shipment delay \+ supplier score \+ inventory impact) into one synthesized answer. This is what makes it feel like an "agent," not a search bar.

**5\. A confidence/trust indicator on every prediction**  
 Show a confidence score or "based on X weeks of data" next to forecasts. This signals product maturity — most hackathon teams present predictions as if they're certain, which judges know is unrealistic.

**6\. Business-impact framing everywhere, not just technical metrics**  
 Instead of "stockout predicted," say "$14,000 revenue at risk, 3 customer orders affected." Translating technical output into dollars/customers is what makes non-technical judges (and real buyers) care.

**7\. A "what-if" simulator (stretch goal, high wow-factor)**  
 Let the user simulate a scenario — "what if this supplier goes down for a week?" — and instantly see projected impact. This is rare in hackathon builds and demonstrates real product thinking beyond just monitoring.

**8\. Tight scope, deep execution**  
 Don't try to build all 6 data sources and all 4 layers equally deep. Pick ONE disruption type (e.g., supplier delay) and go deep — forecasting, scoring, recommendation, and chat all working well for that one scenario — rather than shallow coverage everywhere. Judges reward depth over breadth almost every time.

## **SupplySense — Layer-by-Layer Deep Dive (Features \+ Extras \+ Screens)**

### **Layer 1: Data Ingestion — "Gathering all the vitals"**

**Core Features (mandatory):**

* Connectors for: suppliers, warehouses, POs, inventory, logistics/carriers, external sources (weather, news)  
* Data normalization into a common schema  
* Scheduled polling (e.g., every 15 min) \+ event-based updates (webhooks for shipment status)  
* Storage layer (raw \+ cleaned tables)

**Extras that add value:**

* **Data quality checks** — flag missing/duplicate/stale records before they reach the prediction layer  
* **Source health monitoring** — auto-detect when a source stops sending data (e.g., "carrier API silent for 2 hrs")  
* **Synthetic data generator** — realistic simulated ERP/WMS/carrier data with seasonality and noise (since you won't have real enterprise access)  
* **Live external APIs** — real weather \+ news feeds, even in a prototype, for demo credibility

**Screens:**

| Screen | What it shows |
| ----- | ----- |
| **Integrations Screen** | List of all data sources, connection status (live/error), last sync time |
| **Data Freshness Indicator** | Small strip showing how recent each source's data is |
| **Raw Event Log** (optional) | Live feed of incoming records — proves the pipeline is actually running, not static |

---

### **Layer 2: Analysis & Prediction — "Reading the vitals"**

**Core Features (mandatory):**

* Real-time inventory monitoring across warehouses  
* Shortage/overstock prediction (time-series forecasting)  
* Demand spike/anomaly detection \+ cause attribution (seasonality/promo/external event)  
* Shipment delay detection \+ downstream business impact estimation

**Extras that add value:**

* **Hierarchical forecasting** — SKU-level \+ warehouse/category-level forecasts, reconciled  
* **Confidence intervals** — "70% chance of stockout in 3–7 days," not a fake-precise single number  
* **Exogenous variables** — feed weather, promotions, holidays into the forecast model  
* **Root-cause correlation engine** — automatically links an anomaly to a likely external signal (e.g., matches spike timing to a promo calendar or news event)  
* **Trend vs. one-off distinction** — flag whether a spike is a lasting shift or a blip

**Screens:**

| Screen | What it shows |
| ----- | ----- |
| **Inventory Monitor Screen** | Live stock levels per SKU/warehouse, color-coded by risk (red/yellow/green) |
| **Demand Forecast Screen** | Forecast charts per SKU with confidence bands |
| **Anomaly Detection Screen** | List of detected spikes/drops with likely cause tagged |
| **Shipment Delay Screen** | Delayed shipments \+ which orders/customers are impacted downstream |

---

### **Layer 3: Risk & Recommendation — "The diagnosis \+ prescription"**

**Core Features (mandatory):**

* Supplier reliability scoring (delivery performance, lead time, quality, fulfillment rate)  
* Alternate supplier/warehouse recommendation during disruption  
* Inventory allocation prioritization when stock is limited  
* Procurement recommendations based on forecasted demand

**Extras that add value:**

* **Explainable scoring** — show *why* a supplier's score changed (e.g., feature importance: "late deliveries \+15%, quality steady")  
* **Substitutability graph** — a clear mapping of which suppliers/warehouses can cover which SKUs, so recommendations aren't random guesses  
* **Optimization-based allocation** — treat allocation as a constrained problem (SLA priority vs. margin vs. fairness), not just "first come first served"  
* **Estimated dollar impact on every recommendation** — "$12K stockout risk avoided by switching"  
* **Feedback loop** — planner accepts/rejects a recommendation, and the system adjusts future scoring/weighting

**Screens:**

| Screen | What it shows |
| ----- | ----- |
| **Supplier Risk Scorecard** | Ranked list of suppliers, color-coded scores, drill-down into "why" |
| **Recommendation/Alert Feed** | Cards like "Supplier X delayed → switch to Supplier Y," with reasoning shown |
| **Allocation Priority Screen** | Who/what gets limited stock first, with rationale |
| **Procurement Suggestions Screen** | What to reorder, how much, from whom, by when |

---

### **Layer 4: Interface — "Talking to the doctor"**

**Core Features (mandatory):**

* Real-time dashboard (shortages, supplier risk, delays, warehouse utilization, forecasts, service-level impact)  
* Auto-generated executive summaries  
* Natural language chat/query interface

**Extras that add value:**

* **Agentic chat (tool-calling)** — the chatbot pulls from inventory, supplier scores, shipment data, and forecasts dynamically to answer multi-part questions, instead of canned responses  
* **Reasoning trace shown in chat** — when it answers "which supplier is riskiest," it shows the data it pulled and why, not just a final line  
* **"What-if" simulator** — user asks "what if Supplier A goes down for a week?" and sees a projected impact instantly  
* **Voice or push notifications** — proactive alert delivery (Slack/email/SMS style) instead of waiting for someone to open the dashboard  
* **Role-based views** — planner sees operational detail, executive sees summary-only view

**Screens:**

| Screen | What it shows |
| ----- | ----- |
| **Main Dashboard** | Single-pane overview of all key metrics across the system |
| **Executive Summary View** | Auto-written plain-English report of today's risks \+ mitigation suggestions |
| **Chat/NLQ Screen** | Conversational interface, ask anything, see reasoning trace |
| **What-If Simulator Screen** (stretch) | Scenario testing — simulate a disruption, see projected impact |

---

# PRD

# **PRD — SupplySense (Hackathon MVP)**

## **1\. Product One-Liner**

An AI system that watches a company's supply chain, predicts disruptions before they hit, tells decision-makers what to do about it, and lets them ask questions in plain English.

## **2\. Scope Decision (read this first)**

The full spec has 4 layers and 12+ features. **We are not building all of it.** Given the deadline, we are building **one complete, working disruption story end-to-end**, fully wired from data → prediction → recommendation → interface. Everything else is cut unless time remains.

## **3\. In-Scope MVP (now TWO stories we're building — see note below)**

**Story A — Disruption Response (original scenario):** A key supplier's shipment gets delayed → system predicts a stockout for a specific product/warehouse → system recommends an alternate supplier with reasoning \+ cost impact → system auto-writes an executive summary → user can ask the chatbot about it and get a synthesized answer.

**Story B — Proactive Inventory Management (newly mandatory):** the system also detects overstock situations, flags demand anomalies with a likely cause, prioritizes which pending orders get stock when availability is limited, and generates procurement suggestions from forecasted demand — independent of any single disruption event.

**Features required (19 total — all mandatory, none optional):**

1. Simulated/synthetic data for: suppliers, warehouses, inventory, purchase orders, shipments (seeded, not live-integrated)  
2. Real live weather API integration (for one external signal, to show it's not all fake data)  
3. Inventory monitoring (current stock per SKU/warehouse)  
4. Shortage prediction (simple forecast: burn rate \+ days-to-stockout)  
5. Shipment delay detection (from seeded/simulated shipment events)  
6. Downstream impact tracing (which orders/products affected by a delay) — **Disruption Cascade Simulator**  
7. Supplier reliability scoring (basic formula from historical delivery/quality data)  
8. Recovery Resilience Score (time-to-recover after a missed delivery)  
9. Alternate supplier recommendation with reasoning shown  
10. Cost-of-Delay Translator (₹ impact estimate)  
11. Confidence score shown on every prediction  
12. Auto-generated executive summary (LLM call)  
13. Chat/NLQ interface with tool-calling (agentic, pulls from multiple data sources)  
14. Dashboard with 7-Day Lookahead as default view  
15. Auto-drafted dealer/supplier communication (templated, filled from real data)  
16. **Overstock detection** — same forecasting engine as shortage, flagging the opposite direction (stock far exceeding demand-justified levels)  
17. **Anomaly/demand-spike detection with cause attribution** — formalized here as its own mandatory feature (previously only implicit in the schema/code, now explicit)  
18. **Inventory allocation prioritization logic** — when available stock can't cover all pending customer orders for a SKU, rank which orders get fulfilled first (by order value, SLA priority, or a simple weighted rule)  
19. **Procurement recommendation generator** — from forecasted demand, suggest what to reorder, how much, and roughly when, independent of any specific disruption

    ## **4\. Explicitly Out of Scope (cut if time is short — this list is now shorter)**

* Real ERP/WMS/carrier integrations (simulated data only)  
* Silent Stockout Radar (nice-to-have, build only if ahead of schedule)  
* What-If Simulator (stretch goal, build only if ahead of schedule)  
* Multi-agent debate/negotiation systems  
* Real payment/insurance/action-taking automation  
* User authentication / multi-tenant support / role-based views  
* Mobile responsiveness beyond basic usability

  ## **5\. Target User (for the demo narrative)**

An operations/supply chain planner at a mid-size manufacturing or distribution company who currently checks 3-4 disconnected systems to answer "am I at risk this week?"

## **6\. Success Criteria (for THIS hackathon, not production)**

* \[ \] The one disruption story (Story A) runs live, end-to-end, without manual intervention once triggered  
* \[ \] Every recommendation shown has visible reasoning \+ confidence \+ ₹ impact  
* \[ \] Chatbot can answer at least 3 of the 4 sample questions from the original spec, correctly, using real backend data  
* \[ \] Dashboard defaults to the 7-day lookahead view  
* \[ \] A dealer communication is auto-generated and shown on screen, filled with real data from the scenario  
* \[ \] At least one seeded SKU shows an overstock flag, with the same explainability treatment as shortage predictions  
* \[ \] At least one seeded anomaly is detected and shown with a likely cause (promo/weather/unknown)  
* \[ \] At least one seeded SKU with limited stock shows an allocation priority ranking across 2+ pending orders  
* \[ \] The procurement recommendation screen/section shows at least 2-3 real suggestions generated from forecasted demand

  ## **7\. Core User Stories**

1. As a planner, I open the dashboard and immediately see what's predicted to break in the next 7 days, not just today.  
2. As a planner, when a shipment is delayed, I want to see exactly which orders/products it threatens, not just "shipment late."  
3. As a planner, when the system recommends an alternate supplier, I want to see why — not just a name.  
4. As a planner, I want to know the rupee cost of ignoring a risk, so I can prioritize.  
5. As a planner, I want to ask a question in plain English and get an answer that's actually reasoned across multiple data points, not a canned response.  
6. As a planner, I want the system to draft the outreach message to the supplier/dealer for me, not just tell me to do it.  
7. As a planner, I want to know when I'm sitting on too much stock, not just too little, so I don't tie up working capital.  
8. As a planner, when demand suddenly spikes or drops, I want the system to tell me why, not just that it happened.  
9. As a planner, when I don't have enough stock to cover every pending order, I want the system to tell me who should get it first, and why.  
10. As a planner, I want procurement suggestions generated from actual forecasted demand, not something I have to work out myself.

    ## **8\. Demo Script (what we present at 12 PM)**

**Story A — Disruption Response:**

1. Show dashboard — 7-day lookahead, everything looks fine-ish  
2. Trigger/show a shipment delay event  
3. Cascade simulator shows affected orders  
4. Cost-of-Delay shows ₹ impact  
5. System recommends alternate supplier with reasoning \+ confidence \+ Recovery Resilience Score  
6. Dealer message auto-drafted, shown on screen  
7. Executive summary auto-generated  
8. Ask chatbot "what's causing today's biggest disruption?" — it independently reconstructs the story

**Story B — Proactive Inventory Management:** 9\. Show the overstock flag on a seeded SKU, alongside a shortage flag on another — same explainability treatment on both 10\. Show the anomaly feed — a seeded demand spike tagged as "likely cause: promotion" 11\. Show the allocation priority screen — a SKU with more pending orders than available stock, ranked with reasoning 12\. Show 2-3 procurement suggestions generated from forecasted demand

1. 

# TRD

# **TRD — SupplySense (Hackathon MVP)**

## **1\. Tech Stack**

| Layer | Choice | Why |
| ----- | ----- | ----- |
| Backend | **FastAPI** (Python) | Fast to build, easy async, good with SSE/streaming, good for ML/data work |
| Database | **PostgreSQL** | Relational data fits supply chain entities well; easy to query for both of you in parallel |
| Test Frontend (during backend build) | Simple **Streamlit** app OR raw HTML \+ fetch calls OR Postman/curl | Fastest way to poke endpoints without wasting time on UI before backend is proven |
| Real Frontend (after backend works) | **Next.js 14** | Matches your usual stack, fast to build dashboards with |
| LLM calls | **Anthropic API (Claude)** or OpenAI — pick whichever either of you has a key for already | Used for: exec summary generation, chat/NLQ agent, recommendation reasoning text |
| External live data | **OpenWeatherMap API** (free tier) | Real live external signal — for demo credibility |
| Hosting (if needed) | Localhost for dev; Render/Railway for backend if you want a live demo URL, Vercel for frontend later | Keep it simple — local demo is fine if internet/deploy is risky this close to deadline |

## **2\. System Architecture (high level)**

\[Synthetic Data Seeder\] \---\> \[PostgreSQL\]  
                                  |  
\[Weather API\] \--------------------|  
                                  v  
                        \[FastAPI Backend\]  
                          |     |      |  
                    Ingestion  Analysis  Risk/Reco  
                     Layer      Layer     Layer  
                          \\      |       /  
                           v     v      v  
                        \[Unified API Layer\]  
                          |             |  
                   \[Test Frontend\]  \[Chat/NLQ Agent\]  
                          |  
                   \[Next.js Frontend\] (built later)

## **3\. Backend Modules (map directly to team split doc)**

1. **Data Layer** — DB models, seed script for synthetic data (suppliers, warehouses, SKUs, POs, shipments, demand history)  
2. **Ingestion Layer** — weather API fetcher, normalization functions, scheduled/one-shot sync endpoint  
3. **Prediction Engine** — stockout forecasting (simple: days-to-stockout \= current\_stock / avg\_daily\_demand), shipment delay detection, cascade impact tracer  
4. **Risk & Recommendation Engine** — supplier scoring formula, recovery resilience calculation, alternate-supplier matcher, cost-of-delay calculator  
5. **LLM/Agent Layer** — exec summary generator, chat/NLQ agent with tool-calling, dealer message template filler  
6. **API Layer** — REST endpoints exposing all of the above to the frontend

## **4\. Core API Endpoints (minimum needed for MVP)**

GET  /api/dashboard/overview          \-\> 7-day lookahead summary \+ today's snapshot  
GET  /api/inventory                   \-\> stock levels per SKU/warehouse  
GET  /api/inventory/{sku\_id}/forecast \-\> shortage prediction \+ confidence  
GET  /api/shipments/delays            \-\> list of delayed shipments  
GET  /api/shipments/{id}/impact       \-\> cascade impact for a specific delay  
GET  /api/suppliers/scores            \-\> ranked supplier reliability \+ recovery scores  
GET  /api/recommendations             \-\> active recommendations w/ reasoning \+ cost impact  
POST /api/recommendations/{id}/message \-\> generate dealer message from template  
GET  /api/summary/executive           \-\> auto-generated exec summary text  
POST /api/chat                        \-\> { question: string } \-\> agentic answer  
POST /api/simulate/trigger-delay      \-\> manually trigger the demo scenario (for live demo control)

## **5\. Forecasting / ML Approach (kept simple given time constraint)**

* **Shortage prediction:** `days_to_stockout = current_stock / rolling_avg_daily_demand`. Add basic confidence based on how much historical variance there is (more variance \= lower confidence). No need for ARIMA/Prophet given the timeline — a clean, explainable formula beats an overbuilt model you can't finish.  
* **Anomaly/demand spike:** simple z-score against rolling average; if it correlates with a seeded "promo" or weather flag, tag the cause.  
* **Supplier reliability score:** weighted formula — `score = w1*on_time_rate + w2*(1/avg_lead_time_deviation) + w3*quality_rate`. Pick simple weights (e.g. 0.5/0.25/0.25), document them.  
* **Recovery Resilience Score:** average number of days between a missed delivery and the next on-time delivery, from seeded historical data.  
* **Cost of Delay:** `impact = at_risk_order_value * (delay_days_factor)` — keep the formula simple and explainable, show your work in the UI.

## **6\. LLM Integration Points**

1. **Executive Summary** — feed structured JSON (today's risks, predictions, recommendations) to the LLM with a prompt asking for a short plain-English summary. Use a clear system prompt to keep tone consistent.  
2. **Chat/NLQ Agent** — tool-calling setup: define tools like `get_inventory_status(sku)`, `get_supplier_score(supplier_id)`, `get_shipment_delays()`, `get_recommendation(scenario_id)`. Let the LLM decide which tools to call based on the question, then synthesize an answer.  
3. **Dealer Message Generator** — feed a template \+ situation data (supplier name, SKU, quantity, dates, reason) to the LLM to fill in a natural, professional message.

## **7\. Data Seeding Requirements**

Write one Python script that seeds:

* 5-8 suppliers (with varied historical reliability — some good, some bad, some "bad but fast recovery")  
* 2-3 warehouses  
* 15-20 SKUs/products  
* 3-6 months of synthetic demand history per SKU (with at least one seasonal pattern and one promo spike baked in)  
* 10-15 purchase orders (mix of on-time and late)  
* A handful of shipment events, including one clearly "delayed" event to trigger the demo scenario

## **8\. Testing Approach**

* Test every backend endpoint with curl/Postman or a minimal Streamlit page **before** touching the real frontend  
* Do not start the Next.js frontend until all endpoints in Section 4 return correct, realistic data  
* Keep a shared Postman collection or a markdown file of example requests/responses so both of you can test independently without waiting on each other

## **9\. Deployment (optional, only if time allows)**

* Backend: Render or Railway (fastest free options for FastAPI \+ Postgres)  
* Frontend: Vercel  
* If deployment eats more than 30 minutes near the deadline, **skip it and demo from localhost** — a working local demo beats a broken deployed one.

# Backend Schema

**Backend Schema — SupplySense (Hackathon MVP)**

All tables below are the minimum needed to make the one demo scenario work end-to-end. Add fields only if you have spare time.

## **1\. `suppliers`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | UUID / serial PK |  |
| name | text |  |
| product\_categories | text\[\] | which SKUs they can supply |
| avg\_lead\_time\_days | float | baseline |
| on\_time\_rate | float | 0-1, computed or seeded |
| quality\_rate | float | 0-1, computed or seeded |
| reliability\_score | float | computed (see TRD formula) |
| recovery\_resilience\_score | float | computed — avg days to bounce back after a miss |

## **2\. `warehouses`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | UUID / serial PK |  |
| name | text |  |
| location | text | for weather API lookup |
| capacity\_units | int | optional, for utilization display |

## **3\. `products` (SKUs)**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | UUID / serial PK |  |
| name | text |  |
| category | text |  |
| unit\_margin | float | used in Cost-of-Delay calc |
| unit\_price | float |  |

## **4\. `inventory_snapshots`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| product\_id | FK \-\> products |  |
| warehouse\_id | FK \-\> warehouses |  |
| stock\_on\_hand | int |  |
| reorder\_point | int |  |
| safety\_stock | int |  |
| recorded\_at | timestamp |  |

## **5\. `demand_history`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| product\_id | FK \-\> products |  |
| warehouse\_id | FK \-\> warehouses |  |
| date | date |  |
| units\_sold | int |  |
| is\_promo\_flag | boolean | for anomaly cause attribution |

## **6\. `purchase_orders`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | UUID / serial PK |  |
| supplier\_id | FK \-\> suppliers |  |
| product\_id | FK \-\> products |  |
| warehouse\_id | FK \-\> warehouses | destination |
| quantity | int |  |
| expected\_delivery\_date | date |  |
| actual\_delivery\_date | date, nullable | null if not yet delivered |
| status | enum | pending / delivered / delayed / cancelled |

## **7\. `shipments`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | UUID / serial PK |  |
| purchase\_order\_id | FK \-\> purchase\_orders |  |
| carrier\_name | text |  |
| current\_status | enum | in\_transit / delayed / delivered |
| original\_eta | date |  |
| current\_eta | date |  |
| delay\_days | int | computed: current\_eta \- original\_eta |

## **8\. `shipment_events`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| shipment\_id | FK \-\> shipments |  |
| event\_type | text | e.g. "delay\_reported", "in\_transit\_update" |
| event\_timestamp | timestamp |  |
| notes | text |  |

## **9\. `external_signals`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| signal\_type | enum | weather / news |
| location | text |  |
| description | text | e.g. "Heavy rain warning" |
| severity | enum | low / medium / high |
| fetched\_at | timestamp |  |

## **10\. `forecasts`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| product\_id | FK \-\> products |  |
| warehouse\_id | FK \-\> warehouses |  |
| predicted\_days\_to\_stockout | float |  |
| confidence\_score | float | 0-1 |
| generated\_at | timestamp |  |

## **11\. `anomalies`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| product\_id | FK \-\> products |  |
| detected\_at | timestamp |  |
| anomaly\_type | text | spike / drop |
| likely\_cause | text | promo / weather / unknown |
| severity | enum | low / medium / high |

## **12\. `recommendations`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | UUID / serial PK |  |
| trigger\_type | text | e.g. "shipment\_delay", "shortage\_predicted" |
| trigger\_ref\_id | text | id of the shipment/forecast that triggered it |
| recommended\_action | text | e.g. "switch to Supplier B" |
| reasoning\_text | text | human-readable explanation |
| estimated\_cost\_impact\_inr | float | from Cost-of-Delay Translator |
| confidence\_score | float |  |
| status | enum | active / accepted / rejected |
| created\_at | timestamp |  |

## **13\. `dealer_messages`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| recommendation\_id | FK \-\> recommendations |  |
| template\_type | text | e.g. "delay\_notice", "expedite\_request" |
| generated\_text | text | LLM-filled message |
| recipient | text | supplier/dealer name |
| created\_at | timestamp |  |

## **14\. `chat_logs`**

| Field | Type | Notes |
| ----- | ----- | ----- |
| id | serial PK |  |
| question | text |  |
| answer | text |  |
| tools\_used | text\[\] | which backend calls the agent made |
| created\_at | timestamp |  |

---

## **Relationships Summary**

suppliers  \---\< purchase\_orders \>---  products  
                     |  
                     v  
                 shipments \---\< shipment\_events

products \---\< inventory\_snapshots \>--- warehouses  
products \---\< demand\_history \>--- warehouses  
products \---\< forecasts \>--- warehouses  
products \---\< anomalies

shipments/forecasts  \---\>  recommendations  \---\>  dealer\_messages

## **Build Order (matches task split doc)**

1. `suppliers`, `warehouses`, `products` (base tables — build first, together, so both of you agree on IDs/shape)  
2. `inventory_snapshots`, `demand_history`, `purchase_orders`, `shipments`, `shipment_events`, `external_signals` (raw/ingested data)  
3. `forecasts`, `anomalies` (analysis layer output)  
4. `recommendations`, `dealer_messages` (risk/recommendation layer output)  
5. `chat_logs` (interface layer, built last since it depends on everything above existing)

# App Flow

# **App Flow — SupplySense (Hackathon MVP)**

## **1\. Data Flow Through the System (backend, invisible to user)**

1. 1\. Seed script populates suppliers, warehouses, products, demand history, POs, shipments  
2. 2\. Weather API fetched live \-\> stored in external\_signals  
3. 3\. Prediction engine runs (on-demand for hackathon, not truly continuous):  
4.      \- reads inventory\_snapshots \+ demand\_history \-\> writes forecasts  
5.      \- reads demand\_history \+ external\_signals \-\> writes anomalies  
6.      \- reads shipments \-\> detects delays \-\> triggers cascade impact trace  
7. 4\. Risk/Recommendation engine runs:  
8.      \- reads forecasts \+ shipments/delays \-\> computes supplier scores \+ recovery scores  
9.      \- generates recommendations (with reasoning \+ cost impact \+ confidence)  
10. 5\. LLM layer runs on top of steps 3-4 output:  
11.      \- generates executive summary  
12.      \- generates dealer message (on demand, per recommendation)  
13. 6\. All of the above exposed via API layer (see TRD Section 4\)  
14. 7\. Frontend (test, then real) calls API layer to render screens  
15. 8\. Chat agent calls the SAME API layer as tools, at question time  
    

    ## **2\. User Flow (what a person actually does, screen by screen)**

    ### **Step 1 — Lands on Dashboard**

* Sees **7-Day Lookahead** view by default (what breaks next week)  
* Secondary section below shows today's snapshot  
* Sees a highlighted card: "1 active disruption detected"

  ### **Step 2 — Clicks into the disruption**

* Goes to **Shipment Delay Screen**  
* Sees the delayed shipment, original ETA vs current ETA  
* Sees the **Cascade Simulator** output: which products/orders are threatened

  ### **Step 3 — Sees the financial stakes**

* **Cost-of-Delay Translator** shows ₹ impact if unresolved, right next to the cascade output

  ### **Step 4 — Sees the recommendation**

* Goes to **Recommendations/Alerts Feed**  
* Sees: "Switch to Supplier B" card with reasoning text, confidence score, and Recovery Resilience Score comparison between current and recommended supplier

  ### **Step 5 — Takes action (simulated)**

* Clicks "Generate Dealer Message" on the recommendation  
* Sees an auto-filled message ready to send to the recommended supplier/dealer

  ### **Step 6 — Reads the summary**

* Goes to **Executive Summary View**  
* Sees the whole situation written in plain English, generated by the LLM from the structured data above

  ### **Step 7 — Asks the chatbot**

* Goes to **Chat/NLQ Screen**  
* Asks: "What's causing today's biggest disruption?"  
* Agent calls tools (get\_shipment\_delays, get\_recommendation, get\_supplier\_score) and synthesizes an answer matching what the user already saw — proving the reasoning is real, not scripted

  ## **3\. Demo-Trigger Flow (important for live presentation)**

Since real-time monitoring isn't practical to fake convincingly in a live demo, build a **manual trigger endpoint** (`POST /api/simulate/trigger-delay`) that:

1. Marks a specific seeded shipment as "delayed" with a chosen delay length  
2. Immediately re-runs the prediction \+ recommendation pipeline for just that scenario  
3. Returns updated data instantly, so during the demo you can press one button and watch the dashboard/cascade/recommendation/summary update live

This is the single most important piece of plumbing for a convincing live demo — build it early, not last.

## **4\. Screen-to-Endpoint Map**

| Screen | Endpoint(s) used |
| ----- | ----- |
| Dashboard | `/api/dashboard/overview` |
| Inventory Screen | `/api/inventory`, `/api/inventory/{sku_id}/forecast`, `/api/inventory/overstock` |
| Anomaly Feed | `/api/anomalies` |
| Shipment Delay Screen | `/api/shipments/delays`, `/api/shipments/{id}/impact` |
| Supplier Risk Screen | `/api/suppliers/scores` |
| Recommendations Feed | `/api/recommendations` |
| Dealer Message | `/api/recommendations/{id}/message` |
| Allocation Priority Screen | `/api/allocation/{product_id}` |
| Procurement Suggestions Screen | `/api/procurement/suggestions` |
| Executive Summary | `/api/summary/executive` |
| Chat/NLQ | `/api/chat` |
| Demo trigger button | `/api/simulate/trigger-delay` |

## **5\. Build-vs-Demo Order**

Build the backend and test it in this exact sequence, since each step depends on the last:

1. Seed data → confirm via direct DB query or a `/api/inventory` test call  
2. Forecast endpoint → confirm shortage prediction shows sensible days-to-stockout  
3. Shipment delay \+ cascade endpoint → confirm impact tracing works  
4. Supplier scoring \+ recommendation endpoint → confirm reasoning text \+ cost impact populate correctly  
5. Executive summary \+ chat endpoints → confirm LLM calls work and pull real data, not hallucinated numbers  
6. Demo trigger endpoint → confirm one button re-runs 2-4 correctly  
7. Only now start the real Next.js frontend, screen by screen, in the same order as the table above  
16. 

# Backend Division

# **Backend Task Distribution — Full Detail**

This replaces the earlier short version. It maps **every single feature from the PRD, every table from the Backend Schema, and every endpoint from the TRD** to one of you by name, so there is nothing left ambiguous or unassigned.

## **Coverage Check (so you know nothing is missing)**

| Source doc | Item count | All assigned below? |
| ----- | ----- | ----- |
| PRD — in-scope MVP features | 19 | Yes — see Section 3 |
| Backend Schema — tables | 17 | Yes — see Section 1 |
| TRD — API endpoints | 15 | Yes — see Section 2, incl. the one shared/joint endpoint |

---

## **1\. Table Ownership (who builds/seeds/writes to which table)**

| Table | Owner | Notes |
| ----- | ----- | ----- |
| suppliers | **Swastik** | includes seeding varied reliability histories |
| warehouses | **Swastik** |  |
| products | **Swastik** |  |
| inventory\_snapshots | **Swastik** |  |
| demand\_history | **Swastik** | needs seasonal pattern \+ 1 promo spike baked in |
| purchase\_orders | **Swastik** | mix of on-time/late records |
| shipments | **Swastik** | includes the one shipment reserved for the live demo trigger |
| shipment\_events | **Swastik** |  |
| external\_signals | **Swastik** | weather API writes here |
| forecasts | **Swastik** | output of prediction engine |
| anomalies | **Swastik** | output of anomaly detector |
| recommendations | **Tanishka** | output of risk/recommendation engine |
| dealer\_messages | **Tanishka** | LLM-generated |
| chat\_logs | **Swastik** | agent conversation history — moved here since the chat/NLQ agent itself is now Swastik's |
| customer\_orders | **Swastik** | **new** — raw/ingested data (like purchase\_orders), feeds the allocation logic Tanishka builds on top |
| allocation\_decisions | **Tanishka** | **new** — output of allocation prioritization logic |
| procurement\_suggestions | **Tanishka** | **new** — output of procurement recommendation generator |

**13 tables to Swastik, 4 to Tanishka** — table count isn't the real measure of effort here; see Section 4 for the actual balance.

---

## **2\. Endpoint Ownership (all 11 \+ the 1 shared aggregation)**

| Endpoint | Owner | Depends on |
| ----- | ----- | ----- |
| `GET /api/inventory` | **Swastik** | inventory\_snapshots |
| `GET /api/inventory/{sku_id}/forecast` | **Swastik** | forecasts |
| `GET /api/shipments/delays` | **Swastik** | shipments |
| `GET /api/shipments/{id}/impact` | **Swastik** | shipments, purchase\_orders, inventory\_snapshots (cascade logic) |
| `POST /api/simulate/trigger-delay` | **Swastik** | shipments, re-triggers forecast \+ recommendation pipeline |
| `GET /api/inventory/overstock` | **Swastik** | forecasts (overstock fields) — same engine as shortage prediction, inverted |
| `GET /api/anomalies` | **Swastik** | anomalies — formalizing what was already built in the forecasting service |
| `GET /api/suppliers/scores` | **Tanishka** | suppliers |
| `GET /api/recommendations` | **Tanishka** | recommendations |
| `POST /api/recommendations/{id}/message` | **Tanishka** | recommendations, dealer\_messages, LLM call |
| `GET /api/allocation/{product_id}` | **Tanishka** | customer\_orders, inventory\_snapshots, allocation\_decisions |
| `GET /api/procurement/suggestions` | **Tanishka** | forecasts, suppliers, procurement\_suggestions |
| `GET /api/summary/executive` | **Tanishka** | forecasts, recommendations, anomalies, LLM call |
| `POST /api/chat` | **Swastik** | the hardest/most LLM-heavy piece — tool-calling agent that calls both Swastik's and Tanishka's endpoints as tools, then synthesizes an answer |
| `GET /api/dashboard/overview` | **Joint — build together at Midpoint Sync** | pulls from both tracks (today's snapshot \+ 7-day lookahead \+ active disruption count); build this only once both tracks' underlying endpoints already work, since it's just an aggregation layer |

---

## **3\. Every PRD Feature, Mapped to Owner**

| \# | Feature (from PRD Section 3\) | Owner |
| ----- | ----- | ----- |
| 1 | Simulated/synthetic data (suppliers, warehouses, inventory, POs, shipments) | **Swastik** |
| 2 | Real live weather API integration | **Swastik** |
| 3 | Inventory monitoring | **Swastik** |
| 4 | Shortage prediction (days-to-stockout formula) | **Swastik** |
| 5 | Shipment delay detection | **Swastik** |
| 6 | Downstream impact tracing (Cascade Simulator) | **Swastik** |
| 7 | Supplier reliability scoring | **Tanishka** |
| 8 | Recovery Resilience Score | **Tanishka** |
| 9 | Alternate supplier recommendation \+ reasoning | **Tanishka** |
| 10 | Cost-of-Delay Translator | **Tanishka** |
| 11 | Confidence score on predictions | **Split** — Swastik adds it to forecasts, Tanishka adds it to recommendations (same concept, applied in each person's own layer) |
| 12 | Auto-generated executive summary (LLM) | **Tanishka** |
| 13 | Chat/NLQ agentic interface | **Swastik** — the hardest/most LLM-heavy piece, deliberately placed here |
| 14 | Dashboard 7-day lookahead data | **Joint** — see `/api/dashboard/overview` above |
| 15 | Auto-drafted dealer/supplier communication | **Tanishka** |
| 16 | Overstock detection | **Swastik** |
| 17 | Anomaly/demand-spike detection with cause attribution | **Swastik** |
| 18 | Inventory allocation prioritization logic | **Tanishka** |
| 19 | Procurement recommendation generator | **Tanishka** |

**Result: 9 features to Swastik, 8 to Tanishka, 2 joint/split.** This is the real, effort-adjusted balance — every item from the PRD is accounted for above.

---

## **5\. Full Step-by-Step Build Order**

### **Swastik — Track A**

1. FastAPI \+ Postgres skeleton (shared step, do together first)  
2. Create all 13 owned tables (schema/migrations, incl. chat\_logs, customer\_orders)  
3. Write seed script: suppliers (varied reliability), warehouses, products, demand\_history (with seasonal \+ promo pattern), purchase\_orders, shipments (incl. one reserved for the demo trigger), shipment\_events, customer\_orders (incl. one SKU deliberately oversubscribed for the allocation demo)  
4. Weather API integration → `external_signals`  
5. Build `GET /api/inventory`  
6. Build shortage prediction formula \+ confidence → `GET /api/inventory/{sku_id}/forecast`  
7. Build overstock detection (same engine, inverted) → `GET /api/inventory/overstock`  
8. Build anomaly detector (z-score \+ cause tagging) → `GET /api/anomalies`  
9. Build shipment delay detection → `GET /api/shipments/delays`  
10. Build Cascade Simulator logic → `GET /api/shipments/{id}/impact`  
11. Build `POST /api/simulate/trigger-delay`  
12. Build the Chat/NLQ agent with tool-calling → `POST /api/chat` (the hardest piece — start as soon as steps 5-10 are done, since it needs those endpoints as callable tools; stub Tanishka's endpoints with fake data if you reach this first, then swap to real calls)  
13. Join Tanishka for Midpoint Sync (Section 6\)  
14. Help build `GET /api/dashboard/overview` jointly

    ### **Tanishka — Track B**

1. FastAPI \+ Postgres skeleton (shared step, do together first)  
2. Create 4 owned tables (recommendations, dealer\_messages, allocation\_decisions, procurement\_suggestions)  
3. Design and test supplier reliability scoring formula \+ Recovery Resilience Score (can prototype against dummy numbers before Swastik's seed data exists)  
4. Once seed data exists: build `GET /api/suppliers/scores`  
5. Build alternate-supplier matcher logic (substitutability \+ scores) \+ Cost-of-Delay calculator → `GET /api/recommendations`  
6. Build allocation prioritization logic (weighted score on order value \+ SLA priority) → `GET /api/allocation/{product_id}`  
7. Build procurement suggestion generator (from Swastik's forecasts \+ your supplier scores) → `GET /api/procurement/suggestions`  
8. Build LLM prompt \+ integration for Executive Summary → `GET /api/summary/executive`  
9. Build LLM prompt \+ integration for Dealer Message generation → `POST /api/recommendations/{id}/message`  
10. Once both LLM integrations work, help stress-test Swastik's Chat/NLQ agent with tricky questions across all feature areas (disruption, overstock, allocation, procurement) — the highest-risk piece in the build, benefits from a second pair of eyes  
11. Join Swastik for Midpoint Sync (Section 6\)  
12. Build `GET /api/dashboard/overview` jointly

    ## **6\. Midpoint Sync — Checklist (do this together, don't skip)**

* \[ \] Trigger a delay via `/api/simulate/trigger-delay`  
* \[ \] Confirm `forecasts` updates correctly  
* \[ \] Confirm `/api/shipments/{id}/impact` shows the right cascade  
* \[ \] Confirm `/api/recommendations` produces a sensible alternate supplier with reasoning \+ cost impact  
* \[ \] Confirm `/api/summary/executive` reflects the same numbers, not hallucinated ones  
* \[ \] Confirm `/api/chat` can answer a question about this exact scenario correctly  
* \[ \] Confirm `/api/inventory/overstock` correctly flags the seeded overstocked SKU  
* \[ \] Confirm `/api/anomalies` correctly flags the seeded promo/weather-linked spike with a cause  
* \[ \] Confirm `/api/allocation/{product_id}` correctly ranks pending orders for the deliberately oversubscribed SKU  
* \[ \] Confirm `/api/procurement/suggestions` returns sensible suggestions tied to real forecasts  
* \[ \] Only after all of the above pass: build `/api/dashboard/overview` together, then move to frontend  
* 

# Frontend Division

# **Frontend Task Distribution — Full Detail**

Same logic as the backend split: **each person builds the frontend for the features they already own on the backend.** You already know your own data shapes best, so this avoids wasted time re-explaining API responses to each other mid-build.

## **Coverage Check**

| Source doc | Item count | All assigned below? |
| ----- | ----- | ----- |
| App Flow — MVP screens | 12 | Yes — see Section 1 |
| App Flow — screen-to-endpoint map | 12 | Yes — matches Section 1 |
| PRD — USP/feature items needing UI treatment | 12 | Yes — see Section 2 |

---

## **1\. Screen Ownership**

| Screen | Owner | Backend endpoint(s) it calls | Notes |
| ----- | ----- | ----- | ----- |
| Dashboard (7-Day Lookahead) | **Swastik** (lead) \+ Tanishka contributes 1 widget | `/api/dashboard/overview` | Entry point — build last of Swastik's screens once the others exist, since it aggregates pieces from both. Tanishka adds the "active disruption" card sourced from `/api/recommendations`. |
| Inventory Screen | **Swastik** | `/api/inventory`, `/api/inventory/{sku_id}/forecast` |  |
| Overstock View | **Swastik** | `/api/inventory/overstock` | Can be a toggle/tab on the Inventory Screen rather than a fully separate page — same layout, opposite direction |
| Anomaly Feed | **Swastik** | `/api/anomalies` | Small feed/list, similar layout to the Recommendations Feed but Swastik-owned since it's his backend endpoint |
| Shipment Delay Screen | **Swastik** | `/api/shipments/delays`, `/api/shipments/{id}/impact` | Includes the Cascade Simulator visual |
| Chat/NLQ Screen | **Swastik** | `/api/chat` | Hardest frontend piece — needs to render multi-step/tool-call reasoning in a readable way, not just a plain text bubble |
| Supplier Risk Screen | **Tanishka** | `/api/suppliers/scores` | Includes Recovery Resilience Score display alongside standard reliability |
| Recommendations/Alerts Feed | **Tanishka** | `/api/recommendations`, `/api/recommendations/{id}/message` | Includes the Dealer Message generator UI (button → generated message shown) |
| Allocation Priority Screen | **Tanishka** | `/api/allocation/{product_id}` | Ranked list of pending orders for a limited-stock SKU, with reasoning shown per rank |
| Procurement Suggestions Screen | **Tanishka** | `/api/procurement/suggestions` | Simple list — product, suggested quantity, supplier, by-date, reasoning |
| Executive Summary View | **Tanishka** | `/api/summary/executive` |  |
| Demo Trigger Control | **Swastik** | `/api/simulate/trigger-delay` | Small button/control embedded in the Dashboard — build alongside Dashboard, not as a separate screen |

**Result: 6 screens to Swastik, 6 to Tanishka**, split by which backend track each of you already owns.

---

## **2\. USP/Feature Visual Treatments (mapped to owner)**

These are the specific UI details that make the demo land — assigned to whoever owns the screen they live on.

| Feature | Lives on screen | Owner |
| ----- | ----- | ----- |
| Cascade Simulator visual (delay → product → orders chain) | Shipment Delay Screen | **Swastik** |
| Confidence score display on forecasts | Inventory Screen | **Swastik** |
| Overstock flag \+ excess units display | Overstock View | **Swastik** |
| Anomaly cause tag (promo/weather/unknown) | Anomaly Feed | **Swastik** |
| 7-Day Lookahead toggle/default view | Dashboard | **Swastik** |
| Reasoning trace in chat responses | Chat/NLQ Screen | **Swastik** |
| Recovery Resilience Score comparison (current vs. recommended supplier) | Supplier Risk Screen / Recommendations Feed | **Tanishka** |
| Cost-of-Delay ₹ figure on every recommendation | Recommendations Feed | **Tanishka** |
| Explainable reasoning text on recommendations | Recommendations Feed | **Tanishka** |
| Dealer message generator (button → filled template shown) | Recommendations Feed | **Tanishka** |
| Ranked order list with priority reasoning | Allocation Priority Screen | **Tanishka** |
| Procurement suggestion cards with reasoning | Procurement Suggestions Screen | **Tanishka** |

---

## **4\. Build Order**

### **Swastik**

1. Inventory Screen, incl. Overstock View as a toggle/tab (simplest — stock levels \+ forecast \+ confidence \+ overstock flag)  
2. Anomaly Feed (small list, quick to build once the endpoint returns data)  
3. Shipment Delay Screen (Cascade Simulator visual)  
4. Chat/NLQ Screen (hardest — reasoning trace display)  
5. Dashboard \+ Demo Trigger Control (built last, pulls pieces from 1-4 plus Tanishka's disruption card)

   ### **Tanishka**

1. Supplier Risk Screen (scorecard \+ Recovery Resilience Score)  
2. Recommendations/Alerts Feed (reasoning \+ cost \+ dealer message generator — build in that order, each is additive to the same card)  
3. Allocation Priority Screen (ranked list \+ reasoning)  
4. Procurement Suggestions Screen (simplest of the new ones — list of cards)  
5. Executive Summary View (simplest overall — mostly just rendering LLM text cleanly)  
6. Build the Dashboard's "active disruption" widget, hand off to Swastik to slot into the main Dashboard

   ## **5\. Shared Setup (do together first, \~15-20 min)**

* Agree on the Next.js project structure (pages/routes, shared components folder)  
* Agree on the **shared design tokens**: color scheme for risk levels (red/yellow/green), font, spacing — do this once, don't let each person invent their own halfway through  
* Agree on a shared API client/fetch wrapper so both of you call the backend the same way

  ## **6\. Integration Checkpoint (before demo rehearsal)**

* \[ \] Every screen renders real backend data, not placeholder/mock data  
* \[ \] Dashboard correctly reflects the same numbers shown on the deeper screens (no mismatch between summary and detail views)  
* \[ \] Trigger the demo scenario from the Dashboard button and confirm every screen updates correctly when navigated to afterward  
* \[ \] Chat/NLQ answers match what's shown on the other screens for the same scenario  
* \[ \] Move to demo rehearsal (Team Workflow doc, Phase 6\) only after this checklist passes  
* 

