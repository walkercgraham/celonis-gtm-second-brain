---
name: stakeholder-research
description: Conduct deep stakeholder research to build a profile of the target contact. Gathers career background, likely priorities, role-typical pain points, and engagement approach from LinkedIn snippets, executive bios, interviews, and public statements. Use after external research (or in parallel), when stakeholder section is empty/incomplete, or when preparing for a new meeting with a different stakeholder.
---

# Stakeholder Research Skill

This skill performs deep stakeholder research and populates the `stakeholder` section of the Account Brief. It bridges company-level research with individual motivations to personalize engagement. **All findings must include source URLs** so AEs can verify and explore further.

## Reference Materials

| File | Purpose | When to Read |
|------|---------|--------------|
| `references/role_research_guide.yaml` | Role-specific priorities, pain points, and engagement approaches | After identifying stakeholder's role/title |
| `references/stakeholder_search_templates.yaml` | Search query patterns for stakeholder research | When starting research |
| `references/example_outputs/aramco_stakeholder_example.yaml` | Gold standard showing expected depth | To understand expected output format |

## Prerequisites

- An existing Account Brief file for the target company
- The Account Brief must have `inputs.stakeholder_name` populated
- `inputs.stakeholder_title` is optional — this skill will discover and populate the title during research

## Phase 0: Vault-First Check (Before Web Research)

Before starting any web research, check if this person already exists in the vault:

1. Search for existing stakeholder page at `02-areas/celonis/[client]/stakeholders/[name].md`
2. If found: read the existing page. **Merge** new findings with existing vault knowledge — do NOT overwrite interaction history, relationship notes, or "What They Care About" sections that were populated from direct experience.
3. Check `02-areas/celonis/[client]/meetings/` for any meeting notes mentioning this person — extract existing relationship context.

### Slack Internal Intel

Search Slack for internal discussions about this stakeholder:

```
slack_search_public_and_private(
  query: "[Stakeholder Name] [Company]",
  sort: "timestamp",
  sort_dir: "desc",
  limit: 5
)
```

Extract:
- What colleagues have said about this person's priorities or style
- Any relationship context (who knows them, how they respond)
- Deal context mentioning their role in decisions

### Knowledge Lake Check

Query for prior Celonis engagement with this company:

```
search_knowledge(
  query: "[Company Name] [Stakeholder Name OR Title] engagement",
  topics: ["cortex_internal"],
  top_n: 3
)
```

If results found: note any prior VE/AE interactions with this stakeholder or their team.

### Add "Internal Intel" Section to Output

```yaml
internal_intel:
  vault_context: "[Summary of existing vault knowledge — interaction history, known preferences]"
  slack_signal:
    - "[Name] mentioned in #[channel] by [colleague] — [context]"
  prior_celonis_engagement: "[Any KL results about this person/team]"
  source: "Vault + Slack + Knowledge Lake"
```

This section appears BEFORE the web research output, as internal context is higher confidence than public sources.

## Research Depth Requirements

| Source Type | Priority | Examples |
|-------------|----------|----------|
| LinkedIn Profile Snippet | **Highest** | Title, location, experience from search |
| Company Executive Bio | High | Official biography, responsibilities |
| Direct Interviews/Quotes | High | Podcasts, industry publications, keynotes |
| Conference Presentations | Medium | Speaking engagements, panel discussions |
| Press Releases | Medium | Appointment announcements, project quotes |
| News Articles | Medium | Executive mentions, company news |

**Minimum requirement:** 6-10 sources per stakeholder

## Web Research Approach

### CRITICAL: LinkedIn Handling

**LinkedIn URLs ALWAYS return 999/403 errors.** Never attempt to fetch LinkedIn directly.

**Instead, extract from search snippets:**

```
WebFetch:
  url: "https://html.duckduckgo.com/html/?q=%22[First+Last]%22+[Company]+site%3Alinkedin.com"
  prompt: "Extract ALL information visible in the search results about this person.
           This includes: job title, company, location, follower count, 
           any text from their headline or summary that appears in snippets.
           DO NOT try to visit LinkedIn URLs - just extract what's visible here."
```

**Example snippet extraction:**
```
Search result shows:
"Alexander Park - Chief Information Officer - McLaren Automotive Ltd
London Area, United Kingdom · 7,100+ followers
Technology executive with 20 years of experience working across software, automotive..."

Extract:
- Name: Alexander Park
- Title: Chief Information Officer  
- Company: McLaren Automotive Ltd
- Location: London Area, United Kingdom
- Experience: 20 years in technology/software
- Industries: software, automotive
```

**Record as:**
```yaml
source:
  type: "Search snippet (LinkedIn)"
  url: "https://html.duckduckgo.com/html/?q=%22Alex+Park%22+McLaren+CIO"
  status: "Accessible (snippet only - LinkedIn blocks direct access)"
  extracted: "Title, location, experience level, industry background"
```

### Step 1: Initial Profile Search (3-4 searches)

Run these searches and extract from snippets:

```
1. "[Name]" [Company] site:linkedin.com
   → Extract: Title, location, experience summary

2. "[Name]" [Company] biography OR about
   → Look for company bio pages, board pages

3. "[Name]" appointed [Company]
   → Find appointment announcements with background

4. "[Name]" [Company] interview OR keynote OR podcast
   → Find public statements and priorities
```

### Step 2: Follow Accessible Links

From search results, fetch the top 3-5 non-LinkedIn URLs:

**Prioritize:**
1. Company executive/leadership pages
2. Appointment press releases
3. Conference speaker bios
4. Industry news articles
5. Wikipedia (if notable)

```
WebFetch:
  url: "[non-linkedin-url]"
  prompt: "Extract all information about [Name]: biography, career history,
           previous roles, education, achievements, quotes, stated priorities."
```

### Step 3: Deep Dive Searches

Based on initial findings, search for:

```
1. "[Name]" [previous company from LinkedIn] 
   → Verify career history

2. "[Name]" [Industry] conference OR summit [recent year]
   → Find speaking engagements

3. "[Name]" [specific initiative found] 
   → Find statements about their work

4. [Company] [Title] priorities OR strategy
   → Role-level context even if not person-specific
```

### Step 4: Track All Sources

For each search/fetch, record:
- URL attempted
- Status (Accessible, Blocked, Snippet only)
- What was extracted
- Date accessed

## Research Workflow

### Phase 1: Establish Basic Profile (Including Title Discovery)

**Search queries:**
```
https://html.duckduckgo.com/html/?q=%22[Name]%22+[Company]+site%3Alinkedin.com
https://html.duckduckgo.com/html/?q=%22[Name]%22+[Company]+biography
https://html.duckduckgo.com/html/?q=%22[Name]%22+appointed+[Company]
```

**Extract:**
- Full name and current title (**discover title here if not provided by AE**)
- Tenure in current role (appointment date if found)
- Location
- Career stage indicator (years of experience)
- LinkedIn URL (for reference, not fetching)

**Title Discovery:** If `inputs.stakeholder_title` is null/empty, the title MUST be discovered in this phase. The LinkedIn snippet search (`"[Name]" [Company] site:linkedin.com`) typically reveals the title in the search result snippet (e.g., "Alex Park - Chief Information Officer - McLaren Automotive"). This discovered title should be populated in `stakeholder.title`.

### Phase 2: Career Background

**Search for career history:**
```
https://html.duckduckgo.com/html/?q=%22[Name]%22+[Company]+career+history
https://html.duckduckgo.com/html/?q=%22[Name]%22+previously+OR+former
https://html.duckduckgo.com/html/?q=%22[Name]%22+education+OR+university+OR+MBA
```

**Extract:**
- Previous companies and roles
- Career progression pattern
- Education background
- Notable achievements

**Determine Career Stage:**
- **Rising:** <10 years experience, Director/VP level
- **Established:** 10-20 years, SVP/EVP level
- **C-Suite:** 20+ years, CxO title

### Phase 3: Public Statements & Priorities

**Search for their own words:**
```
https://html.duckduckgo.com/html/?q=%22[Name]%22+[Company]+interview
https://html.duckduckgo.com/html/?q=%22[Name]%22+[Company]+keynote+OR+conference
https://html.duckduckgo.com/html/?q=%22[Name]%22+says+OR+stated+OR+announced
```

**Extract:**
- Stated priorities and focus areas
- Pain points they've mentioned
- Vision or strategy statements
- Topics they're passionate about

### Phase 4: Role-Based Priority Mapping

1. Load role from `role_research_guide.yaml`
2. Review role-typical priorities
3. Cross-reference with `company.strategic_priorities`
4. Generate `likely_priorities` combining:
   - Role-typical concerns
   - Company-specific context
   - Research-specific signals (quotes, statements)

## Output Schema

```yaml
stakeholder:
  name: "Alex Park"
  title: "Chief Information Officer"
  tenure_in_role: "Recent appointment"
  tenure_at_company: "<1 year"
  career_stage: "C-suite"
  
  background:
    summary: |
      Technology executive with 20 years of experience in software and 
      automotive sectors. Previously held technology leadership roles at 
      FORSEVEN, Arrival, and Walgreens Boots Alliance.
    previous_companies:
      - company: "FORSEVEN"
        role: "Technology leadership"
        source: "LinkedIn snippet [1]"
      - company: "Arrival"
        role: "Technology leadership"
        source: "LinkedIn snippet [1]"
      - company: "Walgreens Boots Alliance"
        role: "Technology leadership"
        source: "LinkedIn snippet [1]"
    education: "Mathematics and Data Protection, Lomonosov Moscow State University"
    notable_achievements:
      - achievement: "Led Rescale/NVIDIA AI physics partnership at McLaren"
        source: "News/LinkedIn [2]"
        
  likely_priorities:
    - priority: "Unify fragmented data systems across McLaren"
      rationale: "Publicly stated focus on 'breaking down fragmented workflows'"
      source: "LinkedIn announcement [1]"
      
    - priority: "Implement AI and agentic engineering capabilities"
      rationale: "Leading Rescale/NVIDIA partnership for AI physics"
      source: "Industry news [3]"
      
    - priority: "Demonstrate quick wins in new CIO role"
      rationale: "Recent appointment - typical priority for new executives"
      source: "Role-typical (inferred)"
      
  pain_points_by_role:
    - pain_point: "Fragmented workflows and siloed data across business units"
      source: "Direct statement [1]"
      
    - pain_point: "Legacy system constraints limiting agility"
      source: "Role-typical for CIO"
      
    - pain_point: "Proving ROI on digital transformation investments"
      source: "Role-typical for new CIO"
      
  engagement_approach:
    recommended_tone: "Strategic, technical peer-to-peer. Deep technical background - avoid oversimplification."
    topics_to_emphasize:
      - "Process intelligence as foundation for AI initiatives"
      - "SAP integration and visibility"
      - "Quick time-to-value for new CIO mandate"
    topics_to_avoid:
      - "Generic digital transformation pitches"
      - "Overly simplistic ROI claims"
      - "Comparisons to mass-market automotive"
      
  linkedin_url: "https://www.linkedin.com/in/alexander-park-mclaren/"
  
  # Sources for this stakeholder
  stakeholder_sources:
    - id: 1
      type: "Search snippet (LinkedIn)"
      url: "https://html.duckduckgo.com/html/?q=%22Alex+Park%22+McLaren+CIO"
      status: "Accessible (snippet)"
      extracted: "Title, company, location, 20 years experience, previous companies"
      accessed: "2026-04-08"
      
    - id: 2
      type: "News article"
      url: "https://www.example.com/mclaren-ai-partnership"
      status: "Accessible"
      extracted: "Rescale/NVIDIA partnership details"
      accessed: "2026-04-08"
      
    - id: 3
      type: "Industry publication"
      url: "https://www.example.com/mclaren-digital-transformation"
      status: "Blocked (paywall)"
      extracted: "Snippet only - AI initiative headline"
      accessed: "2026-04-08"
```

## Source Documentation Requirements

**Every finding must have:**
1. The data point
2. Source reference (footnote number)
3. Quality rating (Direct or Inferred)

**The `stakeholder_sources` section must track:**
- All URLs/searches attempted
- Status (Accessible, Blocked, Snippet only)
- What was extracted
- Date accessed

## Validation Before Completion

Before marking research complete, verify:

- [ ] `stakeholder.name` populated
- [ ] `stakeholder.title` populated (discovered during research if not provided by AE)
- [ ] `stakeholder.career_stage` determined
- [ ] `stakeholder.background.summary` provides career narrative
- [ ] At least 2-3 `likely_priorities` with rationale and source
- [ ] At least 2 `pain_points_by_role` identified
- [ ] `engagement_approach.recommended_tone` set
- [ ] `engagement_approach.topics_to_emphasize` has 3+ items
- [ ] `stakeholder_sources` section has 6-10 entries
- [ ] Sources include both snippets and followed links

**If title cannot be discovered:** Flag in outputs_log and ask AE to provide the title. Do not proceed to domain inference without a title, as it is critical for accurate domain scoring.

## Handling Common Challenges

### Limited Public Presence

For stakeholders with minimal public information:
1. Rely more heavily on role-typical patterns
2. Mark priorities as "Inferred" quality
3. Note limitations in outputs_log
4. Flag for AE to supplement with direct knowledge

### Name Verification

Always verify the stakeholder is who the AE thinks:
- Search `[Company] [Title] appointed` to find actual role holder
- If name differs, note correction in outputs_log
- Cross-reference multiple sources

### Non-US/Non-English

- Search in English first (most executives have English LinkedIn)
- Check for English press releases
- Note if sources are translated

## Integration with Other Skills

This skill provides data for:
- **Hypothesis Generator:** Uses `likely_priorities` and `pain_points_by_role` to personalize hypotheses
- **Storyline Creator:** Uses `engagement_approach` to shape narrative tone
- **Enablement Pack:** Stakeholder profile becomes key section with hyperlinked sources
- **One-Pagers:** Stakeholder summary for quick reference

## Example Research Flow

```
User: Research Alex Park at McLaren

Claude: Researching Alex Park at McLaren...
(Note: No title provided - will discover during research)

Search 1: "Alex Park" McLaren site:linkedin.com
→ Snippet shows: CIO, McLaren Automotive, London, 20 years experience, 
  previous: FORSEVEN, Arrival, Walgreens Boots Alliance
→ **Title discovered: Chief Information Officer**
→ Source recorded: Snippet [1]

Search 2: "Alex Park" McLaren appointed
→ Found news article about appointment
→ Fetching article... Accessible
→ Source recorded: News [2]

Search 3: McLaren CIO digital transformation
→ Found article about Rescale/NVIDIA partnership
→ Fetching... Blocked (paywall)
→ Snippet extracted, source recorded: Snippet [3]

Search 4: "Alex Park" McLaren interview OR keynote
→ Found conference presentation reference
→ Fetching speaker bio... Accessible
→ Source recorded: Conference [4]

[Continue until 6-10 sources collected]

Profile complete with 8 sources (5 accessible, 3 snippet-only).
```
