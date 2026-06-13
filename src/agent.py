import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from src.tools import (
    search_company_info,
    search_company_news,
    search_financial_info,
    search_bing_news,
    search_reddit_sentiment,
    search_duckduckgo_summary
)

load_dotenv()

def create_client():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not found in .env file")
    return OpenAI(
        base_url="https://models.inference.ai.azure.com",
        api_key=token
    )

# ─────────────────────────────────────────
# AGENT 1: ANALYST — Generates initial report
# ─────────────────────────────────────────
def analyst_agent(client, model, company_name,
                  company_info, news_info, financial_info,
                  bing_info, reddit_info, ddg_info) -> dict:
    print("  → 🤖 Analyst Agent: Generating initial intelligence...")

    today = datetime.now().strftime("%B %d, %Y")

    prompt = f"""You are a world-class senior strategy consultant at McKinsey & Company.
Your report will be read by a Fortune 500 CEO to make multi-billion dollar strategic decisions.

CRITICAL DATE CONTEXT: Today is {today}.
- Future projections MUST reference dates AFTER {today}
- NEVER cite 2024 or 2025 as future years — they are in the past
- NEVER invent specific percentages, dollar figures, or financial metrics
- If exact numbers are unavailable in the data, use specific qualitative facts
- EXECUTIVE PHRASING: Use natural corporate timelines (e.g., "Expected in late 2026" or "12-18 month horizon"). NEVER use robotic formatting like "post-{today}".

=== INTELLIGENCE SOURCES (6 DATA FEEDS) ===

[SOURCE 1 — WIKIPEDIA BACKGROUND]
{company_info}

[SOURCE 2 — GOOGLE NEWS HEADLINES]
{news_info}

[SOURCE 3 — FINANCIAL MARKET SIGNALS]
{financial_info}

[SOURCE 4 — BING NEWS ADDITIONAL COVERAGE]
{bing_info}

[SOURCE 5 — REDDIT PUBLIC SENTIMENT]
{reddit_info}

[SOURCE 6 — DUCKDUCKGO WEB SUMMARY]
{ddg_info}

===========================================

MCKINSEY REPORTING STANDARDS — NON-NEGOTIABLE:
1. ZERO FLUFF: company_overview must open with the single most critical strategic insight from the data. No generic definitions like "X is a company that makes Y."
2. CROSS-SOURCE SYNTHESIS: Combine signals across all 6 sources. If Reddit sentiment conflicts with financial headlines, flag it as a risk signal.
3. DATA INTEGRITY: Every bullet must cite a specific named product, verified date, direct quote, or named event from the sources. NEVER invent figures.
4. CEO-GRADE RECOMMENDATIONS: Each recommendation must be a specific, executable corporate directive — not generic advice.
5. MATH ACCURACY: intelligence_score math must be exactly correct: 5.0 + X + Y - Z = stated total.
6. REDDIT SIGNAL: If Reddit shows strong negative sentiment, add it as a risk signal with subreddit and upvote count.

Return ONLY this valid JSON object, no markdown, no extra text:
{{
  "company_overview": "Single most critical strategic insight about {company_name} right now, based on cross-source synthesis. No generic definitions. Max 3 sentences.",
  "data_confidence": "High/Medium/Low — justified in one sentence based on source quality.",
  "competitive_landscape": "Named competitors from the data with specific context of how they compete with {company_name}.",
  "key_strengths": [
    "[Named Product/Initiative — Source] — [specific strategic advantage with evidence]",
    "[Named Product/Initiative — Source] — [specific strategic advantage with evidence]",
    "[Named Product/Initiative — Source] — [specific strategic advantage with evidence]"
  ],
  "risk_signals": [
    "[Named Threat — Source] — [specific evidence and potential consequence]",
    "[Named Threat — Source] — [specific evidence and potential consequence]",
    "[Named Threat — Source] — [specific evidence and potential consequence]"
  ],
  "growth_indicators": [
    "[Strategic Initiative / Growth Driver — Time Horizon & Source] — [specific market opportunity]",
    "[Strategic Initiative / Growth Driver — Time Horizon & Source] — [specific market opportunity]",
    "[Strategic Initiative / Growth Driver — Time Horizon & Source] — [specific market opportunity]"
  ],
  "strategic_recommendations": [
    "[Specific Executive Action] — addresses [named risk/opportunity] identified in [source]",
    "[Specific Executive Action] — addresses [named risk/opportunity] identified in [source]",
    "[Specific Executive Action] — addresses [named risk/opportunity] identified in [source]"
  ],
  "market_sentiment": {{
    "reddit_signal": "Positive/Negative/Mixed — based on Reddit data with specific evidence",
    "news_tone": "Bullish/Bearish/Neutral — based on headline analysis across Google and Bing",
    "overall": "one sentence synthesis of public and market sentiment"
  }},
  "intelligence_score": "Baseline 5.0 + [X]/2.5 financial ([specific data-backed reason]) + [Y]/2.5 innovation ([specific data-backed reason]) - [Z]/2.5 risk ([specific data-backed reason]) = [exact total]/10. [One sentence CEO-level verdict on {company_name}.]"
}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a world-class McKinsey business intelligence expert writing for Fortune 500 CEOs. Today is {today}. Never hallucinate figures. Cross-synthesize all 6 data sources. Return only valid JSON, no markdown."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=4000
    )

    text = response.choices[0].message.content
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    return json.loads(text)


# ─────────────────────────────────────────
# AGENT 2: CRITIC — Reviews and scores quality
# ─────────────────────────────────────────
def critic_agent(client, model, company_name, analysis: dict) -> dict:
    print("  → 🔍 Critic Agent: Reviewing analysis quality...")

    today = datetime.now().strftime("%B %d, %Y")

    critique_prompt = f"""You are a ruthless Senior Managing Partner at McKinsey.
Audit this CEO-grade business intelligence report for "{company_name}".
Today is {today}.

REPORT TO AUDIT:
{json.dumps(analysis, indent=2)}

RUTHLESS AUDIT CHECKLIST — FAIL ANY OF THESE:
1. FLUFF: Does company_overview open with a generic definition instead of a critical strategic insight? FAIL.
2. HALLUCINATION: Did the analyst invent dollar figures, percentages, or metrics not in source data? FAIL.
3. STALE DATES: Are 2024 or 2025 cited as future dates? FAIL.
4. MATH: Manually compute 5.0 + X + Y - Z. Does it equal the stated total exactly? FAIL if wrong.
5. VAGUENESS: Are there bullets without specific named products, events, or sources? FAIL.
6. MARKET SENTIMENT: Is the market_sentiment section present and populated with real data? FAIL if missing.
7. CEO QUALITY: Would a Fortune 500 CEO find every recommendation specific and executable? FAIL if generic.

IMPORTANT CALIBRATION: If the report contains at least 3 specific named products or events with dates, and the math is correct, score it 7 or above and set approved to true. Only fail reports with clear hallucinations or wrong math.

Return ONLY this valid JSON:
{{
  "overall_quality": "Acceptable/Needs Improvement",
  "quality_score": <integer 1-10>,
  "issues_found": [
    "Issue 1: [exact quote from report that failed and precise reason why]",
    "Issue 2: [exact quote from report that failed and precise reason why]"
  ],
  "improvement_instructions": [
    "Fix [section]: [precise surgical instruction]",
    "Fix [section]: [precise surgical instruction]"
  ],
  "approved": <true or false>
}}"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a ruthless quality control partner. Return only valid JSON, no markdown."
            },
            {"role": "user", "content": critique_prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    text = response.choices[0].message.content
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    return json.loads(text)


# ─────────────────────────────────────────
# AGENT 3: REVISION — Fixes based on critique
# ─────────────────────────────────────────
def revision_agent(client, model, company_name, original_analysis: dict, critique: dict) -> dict:
    print("  → ✏️  Revision Agent: Applying surgical fixes...")

    today = datetime.now().strftime("%B %d, %Y")

    revision_prompt = f"""You are a senior McKinsey analyst fixing a CEO-grade report about "{company_name}".
Today is {today}. Apply every fix below with surgical precision.

ORIGINAL REPORT:
{json.dumps(original_analysis, indent=2)}

ISSUES TO FIX:
{json.dumps(critique.get('issues_found', []), indent=2)}

PRECISE INSTRUCTIONS:
{json.dumps(critique.get('improvement_instructions', []), indent=2)}

MANDATORY FIX RULES:
1. Remove ALL invented percentages or dollar figures — replace with qualitative facts from data
2. Remove ALL 2024/2025 future date references — use 2026 or later
3. Replace ALL generic phrases with specific named products, events, or quoted headlines
4. Recalculate intelligence_score so math is exactly correct
5. Ensure market_sentiment section is present with real evidence
6. Every recommendation must be a specific executable corporate action
7. Return the COMPLETE report with ALL sections — same JSON schema

Return ONLY valid JSON. No markdown. No extra text."""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"You are a world-class McKinsey analyst. Today is {today}. Fix all issues precisely. Return only valid JSON."
            },
            {"role": "user", "content": revision_prompt}
        ],
        temperature=0.2,
        max_tokens=4000
    )

    text = response.choices[0].message.content
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    return json.loads(text)


# ─────────────────────────────────────────
# ORCHESTRATOR — Runs the full multi-agent loop
# ─────────────────────────────────────────
def run_agent(company_name: str) -> dict:
    client = create_client()
    model = os.getenv("MODEL_NAME", "gpt-4o-mini")

    print(f"\n🔍 Analyzing: {company_name}")
    print("=" * 50)

    # STEP 1 — Gather Data from 6 sources
    print("\n📡 Step 1: Gathering intelligence from 6 sources...")
    print("  → [1/6] Wikipedia background...")
    company_info = search_company_info(company_name)
    print("  → [2/6] Google News headlines...")
    news_info = search_company_news(company_name)
    print("  → [3/6] Yahoo Finance signals...")
    financial_info = search_financial_info(company_name)
    print("  → [4/6] Bing News coverage...")
    bing_info = search_bing_news(company_name)
    print("  → [5/6] Reddit public sentiment...")
    reddit_info = search_reddit_sentiment(company_name)
    print("  → [6/6] DuckDuckGo web summary...")
    ddg_info = search_duckduckgo_summary(company_name)

    # STEP 2 — Analyst Agent generates initial report
    print("\n🧠 Step 2: Multi-Agent Reasoning Loop...")
    try:
        initial_analysis = analyst_agent(
            client, model, company_name,
            company_info, news_info, financial_info,
            bing_info, reddit_info, ddg_info
        )
    except json.JSONDecodeError:
        print("  → ⚠️ Analyst returned invalid JSON. Retrying...")
        initial_analysis = analyst_agent(
            client, model, company_name,
            company_info, news_info, financial_info,
            bing_info, reddit_info, ddg_info
        )

    # STEP 3 — Critic Agent reviews quality
    try:
        critique = critic_agent(client, model, company_name, initial_analysis)
        print(f"  → 📋 Critic Score: {critique.get('quality_score', '?')}/10 — {critique.get('overall_quality', '?')}")
    except json.JSONDecodeError:
        print("  → ⚠️ Critic returned invalid JSON. Skipping revision.")
        critique = {"approved": True, "quality_score": "N/A", "overall_quality": "Skipped"}

    # STEP 4 — Revise if needed
    if not critique.get("approved", True):
        print("  → 🔄 Issues detected. Running revision loop...")
        try:
            final_analysis = revision_agent(
                client, model, company_name,
                initial_analysis, critique
            )
            print("  → ✅ Revision complete.")
        except json.JSONDecodeError:
            print("  → ⚠️ Revision returned invalid JSON. Using original.")
            final_analysis = initial_analysis
    else:
        print("  → ✅ Report approved by Critic. No revision needed.")
        final_analysis = initial_analysis

    # STEP 5 — Attach agent metadata
    print("\n📊 Step 3: Structuring final report...")
    final_analysis["agent_meta"] = {
        "generated_on": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "critic_score": critique.get("quality_score", "N/A"),
        "critic_verdict": critique.get("overall_quality", "N/A"),
        "revised": not critique.get("approved", True),
        "issues_found": critique.get("issues_found", []),
        "model_used": model,
        "agents_used": ["Analyst", "Critic", "Revision"],
        "data_sources": [
            "Wikipedia REST API",
            "Google News RSS",
            "Yahoo Finance RSS",
            "Bing News RSS",
            "Reddit JSON API",
            "DuckDuckGo Instant API"
        ]
    }

    return {
        "company": company_name,
        "analysis": final_analysis
    }