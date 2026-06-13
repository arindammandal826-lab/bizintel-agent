import os
import json
from datetime import datetime

def generate_report(data: dict) -> str:
    company = data.get("company", "Unknown")
    analysis = data.get("analysis", {})
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = []
    
    # Enterprise Markdown Header
    report.append(f"# 🏢 BIZINTEL DOSSIER: {company.upper()}")
    report.append(f"> **Generated via Autonomous Reasoning Agent** | {timestamp}\n")
    report.append("---\n")

    if "raw_analysis" in analysis:
        report.append("## ⚠️ RAW ANALYSIS LOG\n")
        report.append(analysis["raw_analysis"])
    else:
        # 1. Executive Summary & Confidence
        report.append("## 📌 1. EXECUTIVE OVERVIEW")
        report.append(f"{analysis.get('company_overview', 'No overview available.')}")
        report.append(f"\n**Data Confidence Score:** `{analysis.get('data_confidence', 'N/A')}`\n")
        
        # 2. Intelligence Score Blockquote
        score_data = analysis.get('intelligence_score', '')
        report.append("## 🏆 2. INTELLIGENCE SCORE")
        report.append(f"> **{score_data}**\n")

        # 3. Market Landscape
        report.append("## 🌍 3. COMPETITIVE LANDSCAPE")
        report.append(f"{analysis.get('competitive_landscape', 'No landscape data.')}\n")

        # Market Sentiment Section
        sentiment = analysis.get("market_sentiment", {})
        if sentiment:
            report.append("## 📣 4. MARKET SENTIMENT")
            report.append(f"* **Reddit Signal:** {sentiment.get('reddit_signal', 'N/A')}")
            report.append(f"* **News Tone:** {sentiment.get('news_tone', 'N/A')}")
            report.append(f"* **Overall:** {sentiment.get('overall', 'N/A')}")
            report.append("\n")

        sections = [
            ("💪 5. KEY STRENGTHS & MOATS", "key_strengths"),
            ("⚠️ 6. RISK SIGNALS & VULNERABILITIES", "risk_signals"),
            ("📈 7. 12-MONTH GROWTH INDICATORS", "growth_indicators"),
            ("🎯 8. STRATEGIC RECOMMENDATIONS", "strategic_recommendations"),
        ]
        
        for header, key in sections:
            value = analysis.get(key)
            if value:
                report.append(f"## {header}")
                if isinstance(value, list):
                    for item in value:
                        if " — " in item:
                            parts = item.split(" — ", 1)
                            report.append(f"* **{parts[0]}**: {parts[1]}")
                        else:
                            report.append(f"* {item}")
                else:
                    report.append(f"{value}")
                report.append("\n")

    report.append("---\n*End of Automated Intelligence Report — BizIntel Agent*")
    return "\n".join(report)

def save_report(report_text: str, company_name: str, analysis_data: dict = None) -> str:
    # 1. Save the clean Markdown report
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    clean_company = company_name.replace(' ', '_').lower()
    report_filename = f"{reports_dir}/report_{clean_company}.md"
    
    with open(report_filename, "w", encoding="utf-8") as f:
        f.write(report_text)
        
    # 2. Save the Agent Audit Log separately
    if analysis_data and "agent_meta" in analysis_data:
        audits_dir = os.path.join(reports_dir, "audits")
        os.makedirs(audits_dir, exist_ok=True)
        
        audit_filename = f"{audits_dir}/audit_{clean_company}.json"
        with open(audit_filename, "w", encoding="utf-8") as f:
            json.dump(analysis_data["agent_meta"], f, indent=4)
            
    return report_filename