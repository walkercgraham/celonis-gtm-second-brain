# Staleness Thresholds

Configurable scoring rubric for the refresh skill. Adjust these values based on portfolio cadence.

## Rating Thresholds

| Parameter | Fresh (Green) | Aging (Amber) | Stale (Red) |
|-----------|---------------|---------------|-------------|
| Days since last meeting | ≤7 | 8-14 | 15+ |
| Days since hub modified | ≤7 | 14-21 | 22+ |
| Overdue action items | 0-1 | 2-5 | 6+ |
| Status narrative age | ≤14d | 15-21d | 22+d |
| Hypothesis silence | ≤21d | 22-30d | 31+d |

## Rating Logic

- **Fresh** requires ALL conditions met (AND logic)
- **Amber** triggers on ANY single condition (OR logic)
- **Red** triggers on ANY single condition at Red level (OR logic)
- If multiple Red conditions hit simultaneously, note as "deeply stale"

## Stage-Adjusted Thresholds

Some stages naturally have longer cadences:

| Stage | Meeting Cadence Adjustment | Rationale |
|-------|---------------------------|-----------|
| Discovery | Standard (above) | Active engagement, frequent touchpoints |
| PoV | Standard (above) | Execution phase, regular check-ins |
| Delivery | +7 days grace | Delivery may have longer execution sprints |
| Expansion | +14 days grace | Expansion discussions have longer cycles |
| Demo Prep | -3 days (stricter) | Time-sensitive, needs daily attention |

Apply grace period by adding days to the threshold before classifying.

## Signal Noise Filters

### Slack Messages to IGNORE
- "can you join?" / "running late" / "on my way"
- Calendar notifications
- Bot messages (unless from a workflow tool)
- Messages from yourself (you already know)
- Generic channel announcements not specific to the client

### Slack Messages to KEEP
- Deal updates ("contract signed", "budget approved", "on hold")
- Deliverable progress ("demo ready", "POV results in")
- Stakeholder changes ("new CIO", "reorg announced")
- Escalations ("competitor in", "timeline moved up")
- Meeting outcomes ("call went well", "they want to expand")
- Questions about the client from other team members

### Knowledge Lake Results to IGNORE
- Generic industry reports not mentioning the client
- Celonis marketing materials
- Results about different companies with similar names

### Knowledge Lake Results to KEEP
- New reference customers in same industry
- New assets (demos, decks) matching active hypotheses
- Prior engagement data not in hub
- Competitive intelligence mentioning client's tech stack
