from src.agent import run_agent
from src.report import generate_report, save_report

def main():
    print("\n" + "=" * 60)
    print("  🤖 BIZINTEL AGENT")
    print("  Business Intelligence Powered by Multi-Step Reasoning")
    print("=" * 60)

    company_name = input("\n🏢 Enter company name to analyze: ").strip()

    if not company_name:
        print("❌ Please enter a valid company name.")
        return

    try:
        data = run_agent(company_name)
        report = generate_report(data)
        print("\n")
        print(report)
        
        # We added data["analysis"] here so the function can grab the audit log!
        filename = save_report(report, company_name, data["analysis"])
        
        print(f"\n✅ Report saved to: {filename}")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Check your GITHUB_TOKEN in .env file")

if __name__ == "__main__":
    main()