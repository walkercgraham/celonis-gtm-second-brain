---
type: concept
tags: [celonis, ai-agent, moc]
created: 2026-01-01
modified: 2026-01-01
status: active
related:
  - "[[_moc-celonis-client-work]]"
---

# AI Use Cases Across Accounts

Cross-cutting view of AI use case patterns across your account portfolio. Use this to answer "who else has done this?" and to spot reusable patterns when positioning AI at new accounts.

Populate this as you work across clients. Each section tracks a common use case pattern with reference implementations.

---

## Spare Parts / Inventory Lookup
Finding, identifying, and sourcing spare parts — often with fuzzy matching, image recognition, or inventory checks across plants.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Every manufacturing/mining account has this pain. Image recognition → material code → inventory check → PR/stock transfer is the typical architecture.

---

## Vendor / Supplier Inbox Automation
AI agent responding to vendor emails (invoice status, payment timing, block reasons) or automating supplier communication.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** High-volume, repetitive, low-risk — ideal first AI use case for AP/procurement teams.

---

## Dunning / Collections Optimisation
AI-driven personalisation of dunning notices, prediction of late payers, or collections prioritisation.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Working capital improvement with clear financial metric (DSO, overdue %). Low governance risk compared to other AI use cases.

---

## Cash / Credit Forecasting
Predicting cash flow, credit limit breaches, or payment timing using ML/Prediction Builder.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Finance teams love this — clear ROI, predictive, ties to working capital targets.

---

## Duplicate Detection
Finding duplicate invoices, claims, materials, or records using ML/fuzzy matching.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Annotation Builder is the natural fit for many of these. Look for accounts with live implementations as reference customers.

---

## Process Copilot (Knowledge Retrieval)
Chatbot/copilot answering operational questions from process data ("What's the STP rate?", "Where is this invoice?").

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Broad applicability, low risk, good adoption driver. But "not the strongest expression of Celonis value" — better as wedge than flagship.

---

## PR / Purchasing Agent
Agentic AI that creates purchase requisitions, selects vendors, and/or optimises terms.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** High-value, CFO-aligned, but complex to build.

---

## Case Triage / Complaint Routing
AI categorisation, routing, sentiment analysis, or summarisation of cases/complaints/tickets.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Annotation Builder is the natural fit. Strong for ITSM and customer service use cases.

---

## Controls Automation
Automating manual control tests, compliance checks, or audit processes.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** "Celonis AI is made for this." High FTE savings, clear compliance value.

---

## Order Block Resolution
AI to identify which order blocks can safely be removed to unblock billing/delivery.

| Account | Status | Specifics |
|---------|--------|-----------|

---

## Touchless AP / Invoice Processing
End-to-end automation of invoice processing with minimal human intervention.

| Account | Status | Specifics |
|---------|--------|-----------|

---

## SLA Breach / Outcome Prediction
Predicting which cases/tickets will breach SLA or which customers will churn.

| Account | Status | Specifics |
|---------|--------|-----------|

---

## Inventory Optimisation (Agentic)
AI-driven decisions on safety stock, reorder points, material allocation, or excess stock reduction.

| Account | Status | Specifics |
|---------|--------|-----------|

**Pattern:** Monte Carlo + safety stock formulas (King's, etc.) is the typical approach. Look for $100M+ excess inventory targets.

---

## How to Use This Note

- **Before positioning AI at a new account:** Check which use cases match their process landscape and find reference accounts
- **During `/prep`:** Link to specific sections to surface "we've done this before at X"
- **For internal enablement:** Share patterns with VEs working similar accounts
- **Tag search:** Use `#usecase/[name]` in Obsidian to find all related notes
