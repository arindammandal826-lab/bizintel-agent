# 🤖 BizIntel Agent: Autonomous Self-Correcting Business Intelligence

### AI-Powered Strategic Intelligence Dossiers via Multi-Agent Consensus & Self-Correction Loops

> **Submission Track:** Reasoning Agents Track | Microsoft Agents League Hackathon 2026

[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Model](https://img.shields.io/badge/Model-GPT--4o--mini-green.svg)](https://github.com/marketplace/models)
[![Architecture](https://img.shields.io/badge/Architecture-Analyst%20%7C%20Critic%20%7C%20Revision-orange.svg)](https://github.com/arindammandal826-lab/bizintel-agent)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🎯 Executive Summary & Core Innovation

Traditional AI reporting tools suffer from information staleness, hallucinated financials, and unstructured formatting. BizIntel Agent addresses these flaws with a multi-agent **Analyst-Critic-Revision** framework running on live-harvested data streams. 

Rather than deploying a single linear prompt generation, this agent treats research as a rigorous, iterative peer-review system modeled after elite management consulting firms.

### Key Engineering Pillars
* **Multi-Source Signal Harvesting:** Assembles multi-modal data in real-time across 6 distinct web protocols, bypassing training data cut-offs.
* **Autonomous Quality-Gated Guardrails:** Features a hard-coded review cycle where a Critic Agent computes mathematical consistency and structural verification before allowing outputs to pass.
* **Separation of Concerns:** Distinct execution layers for data retrieval, inference/criticism, and presentation formatting.

---

## 🧠 System Architecture & Multi-Agent Reasoning Loop

The engine relies on a stateful reasoning and correction cycle structured into 5 discrete stages:

```text
  ┌───────────────────────────────────────────────────────────────────┐
  │ 1. DATA HARVESTING ENGINE                                         │
  │    → Wikipedia Summary API (Historical Context)                   │
  │    → Google News RSS & Bing News API (Current Affairs)            |
  │    → Yahoo Finance RSS (Market Signals & Stock Performance)       │
  │    → Reddit JSON API (Granular Public & Consumer Sentiment)       │
  │    → DuckDuckGo Instant API (Web Summary Rollups)                 │
  └─────────────────────────────────┬─────────────────────────────────┘
                                    ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ 2. ANALYST AGENT (Strategy Layer)                                 │
  │    → Evaluates raw context streams.                               │
  │    → Generates structured analysis and applies exact formulaic    │
  │      Intelligence Scoring.                                        │
  └─────────────────────────────────┬─────────────────────────────────┘
                                    ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ 3. CRITIC AGENT (Autonomous Quality Gatekeeper)                   │
  │   → Inspects report against rigid temporal and mathematical rules.│
  │   → Evaluates math strings, flags temporal anomalies, scores text.│
  └─────────────────────────────────┬─────────────────────────────────┘
                                    ▼
                    Is Report Approved by Critic?
                     /                         \
               [NO] /                           \ [YES]
                   ▼                             ▼
  ┌──────────────────────────────┐        ┌──────────────────────────────┐
  │ 4. REVISION AGENT            │        │ 5. EMISSION LAYER            │
  │    → Ingests Analyst Report  │        │    → Skips revision.         │
  │      and Critic's Issues List│        │    → Locks production state. │
  │    → Executes targeted fixes.│        │                              │
  └────────────────┬─────────────┘        └──────────────┬───────────────┘
                   │                                     │
                   └──────────────────┬──────────────────┘
                                      ▼
  ┌───────────────────────────────────────────────────────────────────┐
  │ OUTPUT REGISTRY                                                   │
  │    → /reports/report_[company].md  (Report file)                  │
  │    → /reports/audits/audit_[company].json (Full Trace Audit Log)  │
  └───────────────────────────────────────────────────────────────────
```

---

## 🛠 Technical Implementation & Source File Matrix

The core repository splits operations elegantly into decoupled operational files:

| Module | Core Responsibility | Technical Highlights |
| :--- | :--- | :--- |
| `main.py` | Application Entrypoint & Runtime Orchestrator | Error containment boundaries, user terminal I/O, and file persistence pipelines. |
| `src/agent.py` | Multi-Agent Loop Management | Hosts prompts for Analyst, Critic, and Revision models. Governs JSON parsing and conditional execution flow based on Critic flags. |
| `src/tools.py` | Multi-Protocol Data Scrapers | Implements safe URL quoting, timeout limits, XML parsing via `xml.etree.ElementTree`, and native REST requests. |
| `src/report.py` | Presentation & File Serialization Engine | Transforms nested unstructured python JSON dictionaries into highly readable, executive-ready Markdown files. |

---

## The Self-Correction System

The key difference between the other agents and this agent is its **proven ability to recover from internal errors** before emission. Here is a real-world trace compiled directly from the system's generated logs:

### 1. The Analyst Overlooks a Math Error
The Analyst generates an Intelligence Score formula but hallucinates a math summary total:
> `"Baseline 5.0 + 2.5/2.5 financial + 2.5/2.5 innovation - 1.0/2.5 risk = 8.0/10"` *(Error: 5.0 + 2.5 + 2.5 - 1.0 = 9.0, not 8.0)*

### 2. The Critic Identifies the Flaw
The autonomous Critic Agent traps the response, intercepts the error, blocks the output path, and outputs structured issues:
```json
{
  "critic_score": 5,
  "critic_verdict": "Needs Improvement",
  "approved": false,
  "issues_found": [
    "Issue 1: The opening overview statement is structurally generic.",
    "Issue 2: The math in the Intelligence Score formula does not compute correctly; it should equal 9.0, not 8.0."
  ]
}
```

### 3. The Revision Agent Fixes It Perfectly
The Revision Agent processes the error array, refines the opening statement to be analytical, performs the arithmetic correction, and locks down a perfect `9.0/10` output in the final Markdown file.

---

## 🚀 Installation & Local Execution

### Prerequisites
* Python 3.11 or higher
* Valid GitHub Personal Access Token (for access to Azure AI Inference Models API marketplace)

### 1. Environment Setup
```bash
# Clone the repository
git clone https://github.com/arindammandal826-lab/bizintel-agent.git
cd bizintel-agent

# Build and activate localized virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install deterministic production dependencies
pip install -r requirements.txt
```

### 2. Configuration Matrix
Create a `.env` file in the root project directory:
```env
GITHUB_TOKEN=ghp_YourActualGitHubPersonalAccessTokenHere
```
> *Note: Your GitHub Token requires zero special permissions (standard `read:user` access works flawlessly).*

### 3. Execution
```bash
python main.py
```

---

## 📊 Verified Output Formats

Every runtime execution guarantees two atomic exports under the `reports/` tree:

### Production Intelligence Dossier (`reports/report_[company].md`)
A production-ready markdown file containing structured headings:
* **Executive Overview:** High-impact openings populated with specific company data, dates, and product metrics.
* **Intelligence Score:** Math-verified strategic index.
* **Competitive Landscape:** Quantitative breakdowns of market alternatives.
* **Market Sentiment & Moats:** Context-derived indicators of enterprise stability.

### Technical Audit Trail Log (`reports/audits/audit_[company].json`)
For transparent evaluation, the system outputs an immutable audit log detailing exactly what went wrong during the reasoning steps and how the agent corrected itself. This file documents the `model_used`, detailed `issues_found`, `critic_score`, and verified `data_sources` used during that execution.

---

## 👨‍💻 Built By

**Arindam Mandal**
Microsoft Agents League Hackathon 2026 — Reasoning Agents Track