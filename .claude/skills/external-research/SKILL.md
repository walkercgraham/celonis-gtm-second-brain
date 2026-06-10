---
name: external-research
description: Conduct deep company research from public sources to populate the Account Brief. Gathers firmographics, strategic priorities, financial context, technology signals, and competitive landscape from earnings calls, SEC filings, annual reports, press releases, and analyst coverage. Use after Account Brief initialized, when company section is empty/incomplete, or to refresh data before a new engagement.
---

# External Research Skill

This skill performs deep company research from public sources and populates the `company` section of the Account Brief. **All findings must include source URLs** so AEs can verify and explore further.

## Reference Materials

| File | Purpose | When to Read |
|------|---------|--------------|
| `references/industry_research_guide.yaml` | Industry-specific queries, signals, and Celonis relevance | Before starting - to identify industry-specific search patterns |
| `references/non_us_company_guide.yaml` | EMEA, APAC, and private company research strategies | For non-US headquartered or private companies |
| `references/source_quality_guide.yaml` | Source tier definitions and quality ratings | When documenting findings |
| `references/search_query_templates.yaml` | Generic search query patterns | When needing query ideas |
| `references/example_outputs/aramco_research_example.yaml` | Gold standard showing expected depth | To understand expected output format |
| `references/example_outputs/research_finding_templates.yaml` | Templates with good/bad examples | When formatting findings |

## Prerequisites

- An existing Account Brief file for the target company
- The Account Brief must have `inputs.company_name` populated

## Research Depth Requirements

This is NOT surface-level research. The skill must gather intel from:

| Source Type | Priority | Examples |
|-------------|----------|----------|
| Earnings Calls & Transcripts | **Highest** | Quarterly earnings, investor days |
| SEC Filings (US Public) | High | 10-K (annual), 10-Q (quarterly), 8-K (events) |
| Annual Reports (Non-US/Private) | High | Integrated reports, sustainability reports |
| Industry Analyst Reports | High | Gartner, Forrester, IDC, sector-specific |
| Press Releases | Medium | Corporate newsroom, PR Newswire |
| News & Trade Publications | Medium | Reuters, industry journals |
| Job Postings | Medium | Signals for technology and initiatives |
| Company Website | Medium | Investor relations, about us, leadership |

**Minimum requirement:** 10-15 distinct sources per company

## Web Research Approach

Use the **search engine → extract snippets → follow links** approach:

### Step 1: DuckDuckGo HTML Search (Primary Method)

**Why DuckDuckGo:** Google often redirects to consent pages. DuckDuckGo's HTML endpoint returns results directly with rich snippets.

```
WebFetch:
  url: "https://html.duckduckgo.com/html/?q=[URL-encoded-query]"
  prompt: "Extract ALL search result titles, snippets, and URLs. 
           Include any information visible in the snippets (titles, descriptions, 
           dates, key facts). List each result with its URL."
```

**IMPORTANT: Extract information from snippets first.** Search engine snippets often contain key facts (job titles, company descriptions, dates, quotes) without needing to visit the page. This is especially valuable for LinkedIn profiles which block direct access.

**Example searches:**
```
https://html.duckduckgo.com/html/?q=McLaren+Automotive+CEO+strategy+2025
https://html.duckduckgo.com/html/?q=McLaren+Automotive+SAP+ERP+implementation
https://html.duckduckgo.com/html/?q="Alex+Park"+McLaren+CIO
https://html.duckduckgo.com/html/?q=McLaren+digital+transformation+technology
```

### Step 2: Follow Top 3-5 Links Per Search

After extracting snippets, fetch the most relevant URLs:

```
WebFetch:
  url: "[result-url]"
  prompt: "Extract strategic priorities, financial metrics, technology initiatives,
           leadership information, and any executive quotes. Include specific 
           numbers and dates. Note any relevant facts for a B2B sales pitch."
```

**Prioritize:**
1. Company investor relations pages
2. Press releases and news
3. Wikipedia (good for quick facts)
4. Industry publications
5. Technology case studies

### Step 3: Track Source Accessibility

For each URL attempted, track:
- **Accessible:** Successfully fetched content
- **Blocked (403/404):** Note as "attempted but blocked"
- **Paywall:** Note as "paywalled - snippet only"
- **Redirect:** Follow the redirect or note as inaccessible

**Record all attempted sources in the Account Brief `sources` section.**

### Recommended Search Sequence

Run these searches in parallel where possible:

1. **Company Overview:**
   - `[Company] Wikipedia`
   - `[Company] investor relations`
   - `[Company] about company overview`

2. **Stakeholder (if known):**
   - `"[Stakeholder Name]" [Company]`
   - `"[Stakeholder Name]" LinkedIn` (extract from snippet only)

3. **Strategy & Financials:**
   - `[Company] earnings call transcript [year]`
   - `[Company] annual report [year]`
   - `[Company] investor day presentation`
   - `[Company] CEO strategy priorities`

4. **Technology & Strategic Partnerships:**
   - `[Company] SAP OR Oracle ERP implementation`
   - `[Company] digital transformation technology`
   - `[Company] cloud AWS OR Azure OR Google partnership`
   - `[Company] AI artificial intelligence strategy`
   - `[Company] Microsoft Copilot OR "Copilot Studio"`
   - `[Company] Databricks OR Snowflake data platform`
   - `[Company] AI partner OR "AI center of excellence"`

5. **Recent News:**
   - `[Company] news [current year]`
   - `[Company] acquisition merger partnership`
   - `[Company] new CEO leadership change`

6. **Competitive Landscape (BROAD — not just process mining):**
   - `[Company] process mining OR Celonis OR Signavio OR Minit`
   - `[Company] ServiceNow OR UiPath OR "Blue Prism" OR "Power Automate"`
   - `[Company] Palantir OR C3.ai OR Dataiku OR "decision intelligence"`
   - `[Company] "Blue Yonder" OR Kinaxis OR o9 OR Coupa supply chain`
   - `[Company] automation platform strategy`

## Mandatory Investor Source Searches

These searches MUST be attempted for every public company. They yield the highest-quality strategic insights.

### 1. Annual Reports & Integrated Reports
```
[Company] annual report 2025 PDF
[Company] integrated report 2025
site:[company-domain]/investors annual report
[Company] investor relations annual
```

**Why:** Annual reports contain CEO letters, strategic priorities, risk factors, and financial context that press releases omit.

### 2. Earnings Call Transcripts / Results Presentations
```
[Company] Q4 2025 earnings call transcript
[Company] earnings transcript Seeking Alpha
site:seekingalpha.com [Company] earnings call
[Company] quarterly results conference call
[Company] results presentation [year]
```

**Platforms to check:**
- Seeking Alpha (seekingalpha.com/symbol/[ticker]/earnings)
- Yahoo Finance (finance.yahoo.com/quote/[ticker]/earnings)
- Company IR page (usually under "Events & Presentations")

**Note:** UK/European companies often call these "results presentations" rather than "earnings calls"

**Why:** Earnings calls reveal what executives actually prioritize, analyst concerns, and forward guidance.

### 3. Capital Markets Day / Investor Day Presentations
```
[Company] capital markets day 2025
[Company] investor day presentation
[Company] strategic update investor
[Company] CMD [year]
[Company] analyst day
```

**Why:** CMD presentations outline 3-5 year strategy, investment priorities, and transformation programs. Search even if >12 months old - strategy doesn't change quarterly.

### 4. Regulatory Filings (Region-Specific)

**Search based on company's listing location:**

| Region | Filing Type | Search Query |
|--------|-------------|--------------|
| **US** | 10-K (annual), 10-Q (quarterly), 8-K (events) | `site:sec.gov [Company] 10-K` |
| **UK** | Annual Report, RNS announcements | `[Company] Companies House` or `site:londonstockexchange.com [Company]` |
| **Germany** | Geschäftsbericht, Bundesanzeiger | `[Company] annual report english` (DAX companies publish English) |
| **France** | Document d'enregistrement universel | `[Company] universal registration document` |
| **Saudi Arabia** | Tadawul filings | `site:tadawul.com.sa [Company]` |
| **UAE** | ADX/DFM announcements | `[Company] ADX investor relations` |
| **Australia** | ASX announcements | `site:asx.com.au [Company]` |
| **Japan** | EDINET filings | `[Company] investor relations english` (summaries available) |
| **Hong Kong** | HKEx announcements | `site:hkexnews.hk [Company]` |
| **India** | BSE/NSE filings | `[Company] BSE annual report` |

**Why:** Regulatory filings contain risk factors, segment breakdowns, and legal disclosures not found in press releases.

### 5. Analyst Coverage & Credit Ratings
```
[Company] Gartner Magic Quadrant
[Company] Forrester Wave
[Company] Moody's credit rating
[Company] S&P rating outlook
[Industry] analyst report [Company]
```

**Why:** Analyst reports provide competitive positioning and industry context.

## Output Schema

The skill populates these fields in the Account Brief:

```yaml
company:
  # Basic firmographics
  industry: "Automotive"
  sub_industry: "Luxury Automotive / Motorsport"
  headquarters: "Woking, Surrey, England"
  region: "EMEA"
  revenue: "~£1.2-1.4B (estimated 2024)"
  employees: "~2,000+"
  public_or_private: "Private (CYVN Holdings)"
  stock_ticker: null
  
  # Celonis classification
  customer_segment: "Enterprise"
  deal_type: "New Logo"
  
  # Strategic context (with source references)
  strategic_priorities:
    - priority: "Digital transformation and unified data architecture"
      evidence: "CIO Alex Park announced partnership with Rescale/NVIDIA for AI physics"
      source: "LinkedIn announcement" # [1]
      source_url: "https://html.duckduckgo.com/html/?q=Alex+Park+McLaren+CIO"
      quality: "Direct"
      
  trigger_events:
    - event: "CYVN Holdings acquisition"
      date: "December 2024"
      source: "Wikipedia / News" # [2]
      source_url: "https://en.wikipedia.org/wiki/McLaren_Automotive"
      relevance: "$2B cash injection, expansion mandate"
      confidence: "High"
      
  financial_context:
    summary: "Privately held, recently acquired by CYVN Holdings..."
    growth_trajectory: "Expansion"
    key_metrics:
      - "~4,000 vehicles produced annually"
      - "SAP downtime costs ~£250K/day"
    sources:
      - "[3] Microsoft case study"
      
  technology_signals:
    erp_systems:
      - system: "SAP ECC / SAP HANA Enterprise Cloud"
        source: "Microsoft Azure case study" # [4]
        source_url: "https://customers.microsoft.com/..."
    cloud_platforms:
      - "Microsoft Azure"
      - "Google Cloud (Racing)"
    digital_transformation: "Active - new CIO mandate"

    strategic_partnerships:
      - partner: "Microsoft"
        relationship_type: "Cloud Provider"
        depth: "Enterprise Agreement"
        evidence: "Azure case study published; SAP on Azure HEC deployment"
        source: "Microsoft Customers site [4]"
        implications_for_celonis: "Strong Microsoft alignment — lead with Copilot integration story"
      - partner: "NVIDIA"
        relationship_type: "Technology Alliance"
        depth: "Project-Level"
        evidence: "Rescale/NVIDIA AI physics partnership for vehicle engineering"
        source: "LinkedIn / News [5]"
        implications_for_celonis: "Engineering-focused AI; Celonis operational AI is complementary"

    ai_strategy:
      platform_partner: "Microsoft"
      platform_evidence: "Azure is primary cloud; AI physics work via Rescale on Azure infra"
      maturity: "Piloting"
      ai_initiatives:
        - initiative: "Rescale/NVIDIA AI physics for vehicle engineering"
          domain_relevance: "Idea to Offer"
          source: "LinkedIn / News [5]"
      ai_governance: "CIO (Alex Park) owns digital and data strategy"
      celonis_positioning: "Complement their engineering AI with operational AI — Celonis connects SAP process data to surface execution gaps they can't see from physics models alone"

  competitive_landscape:
    process_intelligence:
      situation: "Greenfield"
      tools_detected: []
      pitch_implications: "No incumbent — land opportunity"
    decision_intelligence:
      tools_detected:
        - tool: "Alteryx"
          scope: "Analytics team"
          domain_overlap: "Data prep and reporting — not real-time operational"
          source: "News / Partnership announcement [6]"
    supply_chain_solutions:
      tools_detected: []
    automation:
      tools_detected: []
    core_platforms:
      tools_detected:
        - tool: "SAP ECC on Azure HEC"
          scope: "Enterprise"
          migration_status: "Live"
          source: "Microsoft case study [4]"
    overall_positioning: "Greenfield for process intelligence. Strong Microsoft alignment creates co-sell opportunity. Alteryx is complementary (analytics) not competitive (operational)."
    key_differentiators:
      - "Real-time operational visibility vs. Alteryx batch analytics"
      - "Cross-system process view connecting SAP to logistics and engineering"
    co_sell_opportunities:
      - "Microsoft co-sell — Azure customer, potential Copilot integration"

# NEW: Sources section for AE verification
sources:
  - id: 1
    type: "Search snippet"
    url: "https://html.duckduckgo.com/html/?q=Alex+Park+McLaren+CIO"
    title: "Alex Park LinkedIn - CIO McLaren Automotive"
    accessed: "2026-04-08"
    status: "Accessible (snippet)"
    notes: "LinkedIn profile not directly accessible but snippet provided key info"
    
  - id: 2
    type: "Wikipedia"
    url: "https://en.wikipedia.org/wiki/McLaren_Automotive"
    title: "McLaren Automotive - Wikipedia"
    accessed: "2026-04-08"
    status: "Accessible"
    
  - id: 3
    type: "Case study"
    url: "https://customers.microsoft.com/en-us/story/mclaren-racing-azure"
    title: "McLaren Racing - Microsoft Customer Story"
    accessed: "2026-04-08"
    status: "Accessible"
    
  - id: 4
    type: "News"
    url: "https://www.autosport.com/f1/news/..."
    title: "McLaren F1 technology partnership"
    accessed: "2026-04-08"
    status: "Blocked (403)"
    notes: "Used alternative source"
```

## Source Documentation Requirements

**Every finding must have:**
1. **What** - The data point
2. **Source reference** - Footnote number linking to sources section
3. **Quality rating** - Direct, Inferred, or Stale (>12 months)

**The `sources` section must track:**
- All URLs attempted (accessible or not)
- Status of each URL (Accessible, Blocked, Paywall, Redirect)
- Date accessed
- Any notes about the source

This allows the AE to:
- Verify any claim by clicking the source
- See which sources were used vs. blocked
- Explore further if needed

## Research Workflow

### Phase 1: Initial Discovery (5-7 searches)

Run these searches to establish baseline understanding:

```
1. [Company] Wikipedia
2. [Company] investor relations overview
3. [Company] news [current year]
4. [Company] CEO OR leadership
5. [Company] SAP OR Oracle OR ERP
6. "[Stakeholder Name]" [Company] (if known)
7. [Company] [Industry] strategy
```

Extract from snippets AND follow top 2-3 accessible links per search.

### Phase 2: Deep Dive (8-12 searches)

Based on Phase 1 findings, go deeper:

```
1. [Company] earnings call transcript [recent quarter]
2. [Company] annual report [year]
3. [Company] digital transformation
4. [Company] acquisition merger partnership [year]
5. [Company] technology investment
6. [Company] [specific initiative found in Phase 1]
7. [Industry]-specific searches from industry_research_guide.yaml
```

**Technology & AI strategy (2-3 searches):**
```
8. [Company] Microsoft OR AWS OR Google cloud partnership agreement
9. [Company] AI strategy OR "Copilot" OR "generative AI" OR Databricks
10. [Company] data platform OR "data lake" OR Snowflake OR Databricks
```

**Competitive landscape (2-3 searches):**
```
11. [Company] process mining OR Celonis OR Signavio OR ServiceNow
12. [Company] supply chain planning OR "Blue Yonder" OR Kinaxis OR o9
13. [Company] automation UiPath OR "Blue Prism" OR "Power Automate" OR Palantir
```

### Phase 3: Validation & Gap-Filling

- Cross-reference key claims across multiple sources
- Fill gaps with targeted searches
- Document confidence levels

---

## Strategic Technology & AI Research

This section is critical for Celonis positioning. Understanding the account's technology partnerships tells you who to co-sell with, how to frame the integration story, and where competitive risk exists.

### What to Research

**1. AI Platform Partner** — The single most important technology question:

| Signal | Means | Search For |
|--------|-------|-----------|
| Microsoft Copilot Studio deployment | Deep Microsoft AI commitment | `[Company] Copilot OR "Copilot Studio" OR "Microsoft AI"` |
| AWS Bedrock / SageMaker usage | AWS-native AI stack | `[Company] AWS Bedrock OR SageMaker OR "Amazon AI"` |
| Databricks investment | Data-first AI approach | `[Company] Databricks OR "data lakehouse" OR "Unity Catalog"` |
| Google Vertex AI | Google Cloud AI | `[Company] "Vertex AI" OR "Google AI" OR Gemini` |
| Palantir Foundry | Decision intelligence focus | `[Company] Palantir OR Foundry` |
| In-house AI org | Build-vs-buy mentality | `[Company] "AI center of excellence" OR "chief AI officer"` |

**2. Strategic Partnerships** — Platform-level bets beyond just cloud:

Look for:
- Enterprise agreements (multi-year, multi-$M commitments)
- Joint press releases ("strategic partnership", "preferred partner")
- Case studies on partner websites (Microsoft Customers, AWS Case Studies)
- Conference keynote appearances (Ignite, re:Invent, Next, Data+AI Summit)
- Job postings mentioning specific platforms

**3. Competitive Solution Landscape** — Who else is solving similar problems:

| Category | Tools to Detect | Why It Matters |
|----------|----------------|----------------|
| Process Intelligence | SAP Signavio, Microsoft Process Advisor, Minit, ABBYY Timeline | Direct competition |
| Decision Intelligence | Palantir Foundry, C3.ai, Dataiku, Alteryx, ThoughtSpot | Overlapping value prop for executive visibility |
| Supply Chain | Blue Yonder, Kinaxis, o9 Solutions, Coupa, E2open, Manhattan | Compete in SC domain |
| Automation/Workflow | UiPath, SS&C Blue Prism, Power Automate, ServiceNow | Compete on action layer |
| Data Platforms | Snowflake, Databricks, SAP BTP, Azure Synapse | Integration context |
| ERP/Core | SAP S/4HANA, Oracle Cloud, Workday | Integration story |

### How to Interpret Findings

**AI Platform Partner → Celonis Positioning:**

| They chose... | Celonis angle |
|---------------|---------------|
| Microsoft / Copilot | "Celonis is the process intelligence layer that feeds Copilot — it can't take action on processes it can't see" |
| AWS / Bedrock | "Celonis runs on AWS, connects to your data lake, and adds process context that ML models alone can't infer" |
| Databricks | "Celonis complements your lakehouse with real-time process intelligence that enriches your data models" |
| Google / Vertex | "Process data from Celonis feeds your AI models with execution context — not just what should happen, but what actually does" |
| Palantir | "Palantir is strategic planning; Celonis is operational execution — different altitude, complementary" |
| In-House | "Your data science team builds models; Celonis gives them process-specific features and an execution layer" |
| None / Early | "Be the AI advisor — position Celonis as the starting point for process-aware AI" |

**Competitive Solutions → Positioning:**

| They have... | Celonis says... |
|--------------|----------------|
| Signavio (modeling only) | "You have the map — now you need the GPS. Celonis shows what actually happens vs. designed process" |
| ServiceNow (workflows) | "ServiceNow is the action layer — Celonis is the intelligence layer that tells it WHAT to act on" |
| Blue Yonder (planning) | "Planning tells you what should happen; Celonis shows the gap between plan and execution" |
| UiPath (bots) | "Bots execute tasks; Celonis identifies which tasks need automation and measures the impact" |
| Palantir (analytics) | "Palantir answers strategic questions; Celonis optimizes the operational processes underneath" |

### Validation for Technology & Competitive Sections

- [ ] AI platform partner identified (or explicitly marked "None Identified")
- [ ] At least 1 strategic partnership documented with evidence
- [ ] `competitive_landscape.process_intelligence.situation` set
- [ ] At least 2 competitive categories assessed (not just process mining)
- [ ] `overall_positioning` written (2-3 sentence summary)
- [ ] `co_sell_opportunities` populated if partnerships identified
- [ ] `ai_strategy.celonis_positioning` written

## Handling Common Issues

### LinkedIn Profiles (Always Blocked)

**Never attempt to fetch LinkedIn URLs directly.** Instead:
1. Search: `"[Name]" [Company] site:linkedin.com` on DuckDuckGo
2. Extract all information visible in the search snippet (title, headline, location, summary preview)
3. Record as "source: Search snippet (LinkedIn)" with the search URL

Example snippet extraction:
```
Search result shows:
"Alexander Park - Chief Information Officer - McLaren Automotive
London Area, United Kingdom · 7,100+ followers
Technology executive with 20 years of experience..."

→ Extract: Name, Title, Company, Location, Experience level
→ Do NOT try to fetch linkedin.com URL
```

### Paywalled Sources (Reuters, Bloomberg, FT)

1. Extract any information visible in the snippet
2. Note as "Paywall - snippet only"
3. Search for the same story on non-paywalled sources

### 404 Errors

1. Note the attempted URL and status
2. Try alternative search terms
3. Look for archived versions or summaries

### Redirect Loops

1. If redirect goes to consent page (Google), skip
2. If redirect goes to valid content, follow it
3. Note both original and final URLs

## Validation Before Completion

Before marking research complete, verify:

### Core Requirements
- [ ] `company.industry` is populated
- [ ] At least 3 strategic priorities with evidence and sources
- [ ] At least 2 trigger events with dates and sources
- [ ] Financial context summary populated
- [ ] `sources` section has 12+ entries (increased from 10)
- [ ] Each source has URL, status, and access date
- [ ] All findings reference a source by footnote number

### Technology & AI Strategy
- [ ] `ai_strategy.platform_partner` set (including "None Identified" if nothing found)
- [ ] At least 1 `strategic_partnerships` entry with evidence
- [ ] `ai_strategy.celonis_positioning` written (how to frame Celonis given their AI choices)
- [ ] ERP systems identified with migration status

### Competitive Landscape
- [ ] `process_intelligence.situation` determined (Greenfield, Competitor Deployed, etc.)
- [ ] At least 2 competitive categories assessed beyond process intelligence
- [ ] `overall_positioning` written (2-3 sentence positioning summary)
- [ ] `co_sell_opportunities` populated if strategic partnerships exist
- [ ] Supply chain solutions checked (critical for SC domain hypotheses)

### Investor Source Validation (Required for Public Companies)
- [ ] Annual report search attempted (note if found or unavailable)
- [ ] Earnings call / results presentation search attempted (at least 2 recent quarters)
- [ ] Capital markets day / investor presentation search attempted
- [ ] Regulatory filing search attempted (SEC for US, Companies House for UK, Tadawul for Saudi, etc.)
- [ ] At least 1 executive quote captured from investor source
- [ ] At least 4 Tier 1 sources included

### For Private Companies
- [ ] Press release search completed
- [ ] Executive interview / podcast search attempted
- [ ] Funding/investment announcement search attempted
- [ ] Note: "Private company - limited disclosure" in sources section
- [ ] At least 2 Tier 1 sources included (adjusted minimum)

## Updating the Account Brief

After completing research:

1. Read the existing Account Brief
2. Populate the `company` section with research findings
3. Add the `sources` section with all URLs attempted
4. Update `meta.last_updated` to current timestamp
5. Update `meta.last_updated_by` to "external-research"
6. Add entry to `outputs_log`
7. **Do NOT** change `workflow_stage` (wait for all research skills to complete)

## Example Output Quality

**Good (with source attribution):**
```yaml
strategic_priorities:
  - priority: "Digital transformation and unified data architecture"
    evidence: "CIO Alex Park: 'breaking down fragmented workflows to create a unified data loop for the future of automotive engineering'"
    source: "LinkedIn/News announcement [1]"
    quality: "Direct"
```

**Bad (no source):**
```yaml
strategic_priorities:
  - priority: "Digital transformation"
    evidence: "The company is focused on digital"
    source: null
    quality: null
```

## Offer Validation After Completion

After populating the `company` section, count the total factual claims with cited sources and offer validation:

```
Research complete. I found [N] factual claims from [M] distinct sources.
Would you like me to validate these before proceeding? (Takes ~2 min)
  • "validate" — Run /research-validation now
  • "skip" or "continue" — Proceed without validation
```

If AE accepts, invoke the research-validation skill inline. If declined, proceed normally.

## Phase 4: Internal Celonis Cross-Reference (Knowledge Lake)

After completing external research, query Celonis internal intelligence to enrich findings:

### 4.1 Prior Engagement Check
```
search_knowledge(
  query: "[Company Name] engagement implementation",
  topics: ["cortex_internal"],
  top_n: 5
)
```
→ Has Celonis engaged with this company before? What was done? What were the outcomes?

### 4.2 Industry Value Benchmarks
```
search_knowledge(
  query: "[Industry] [process areas found in research] value opportunity benchmark",
  topics: ["reasoning_external"],
  top_n: 5
)
```
→ What inefficiencies are typical in their industry? What metrics should we target?

### 4.3 Competitive Positioning
```
search_knowledge(
  query: "[detected competitors from competitive_landscape section]",
  topics: ["competitive"],
  top_n: 5
)
```
→ How does Celonis position against their specific tech stack?

### 4.4 Add to Output

Add a new section to the Account Brief output:

```yaml
celonis_internal_context:
  prior_engagement:
    exists: true/false
    summary: "[What Celonis has done with this company before, if anything]"
    source: "Knowledge Lake - cortex_internal"
  industry_benchmarks:
    - metric: "[e.g. 15-30% maverick spend reduction]"
      process_area: "[procurement]"
      source: "Knowledge Lake - reasoning_external"
  competitive_positioning:
    - competitor: "[detected tool]"
      celonis_angle: "[positioning from KL]"
      source: "Knowledge Lake - competitive"
  relevant_reference_customers:
    - customer: "[name from KL]"
      industry: "[same or adjacent]"
      what_they_did: "[brief]"
      outcome: "[metric]"
      source: "Knowledge Lake - cortex_internal/cortex_external"
```

---

## Trigger Event Freshness

If this research was last run >30 days ago (check `meta.last_updated`), re-run Phase 1 "Recent News" searches before proceeding to ensure trigger events are current. Stale trigger events lead to embarrassing conversations.

---

## Integration with Other Skills

This skill provides foundational data for:

- **Stakeholder Research:** Company context helps interpret stakeholder priorities
- **Domain Inference:** Strategic priorities and triggers inform domain selection
- **Hypothesis Generator:** Strategic priorities map to pain hypotheses
- **Pitch Deck Creator:** Financial context and triggers shape the narrative
- **Enablement Pack:** Sources are hyperlinked for AE reference
- **Research Validation:** Validates claims from this skill's output
- **Pattern Intelligence:** Cross-references with `/pattern` for use case expansion opportunities
