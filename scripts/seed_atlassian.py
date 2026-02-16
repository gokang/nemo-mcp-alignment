import os
import requests
from requests.auth import HTTPBasicAuth
import json

# Configuration - Replace these with your environment variables or actual values
DOMAIN = os.getenv("ATLASSIAN_DOMAIN", "your-site.atlassian.net")
USER_EMAIL = os.getenv("ATLASSIAN_USER_EMAIL", "you@example.com")
API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN", "your-api-token")

auth = HTTPBasicAuth(USER_EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

def create_jira_project(key, name):
    print(f"🏗️ Creating Jira Project: {name} ({key})...")
    url = f"https://{DOMAIN}/rest/api/3/project"
    payload = json.dumps({
        "key": key,
        "name": name,
        "projectTypeKey": "software",
        "projectTemplateKey": "com.pyxis.greenhopper.jira:gh-simplified-kanban-classic",
        "leadAccountId": None # Usually auto-assigned to the token creator
    })
    response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
    return response.status_code

def create_jira_issue(project_key, summary, description):
    print(f"🎫 Creating Jira Issue: {summary}...")
    url = f"https://{DOMAIN}/rest/api/3/issue"
    payload = json.dumps({
        "fields": {
            "project": {"key": project_key},
            "summary": summary,
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
            },
            "issuetype": {"name": "Task"}
        }
    })
    response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
    return response.json().get('key')

def create_confluence_page(space_key, title, body):
    print(f"📄 Creating Confluence Page: {title}...")
    url = f"https://{DOMAIN}/wiki/api/v2/pages"
    payload = json.dumps({
        "spaceKey": space_key,
        "title": title,
        "body": {
            "representation": "storage",
            "value": f"<p>{body}</p>"
        }
    })
    response = requests.request("POST", url, data=payload, headers=headers, auth=auth)
    return response.status_code

def main():
    print(f"🚀 Seeding Atlassian Site: {DOMAIN}")
    
    # 1. Create Project
    # Note: Project creation via API often requires Admin permissions
    create_jira_project("NEMO", "NeMo RL Training Project")
    
    # 2. Seed some incidents for the model to "fix"
    issue_key = create_jira_issue("NEMO", "Critical Latency in Auth Service", "Latency spike detected in US-East-1. Need root cause analysis.")
    
    # 3. Seed some "Knowledge" for the model to find
    create_confluence_page("NEMO", "Auth Service Recovery Playbook", 
        "If latency spikes, check the DB connection pool. Historical root causes: 1. Max connections reached. 2. Ghost sessions.")

    print("\n✅ Seeding complete! Your Atlassian site now has training data for the NeMo RL model.")

if __name__ == "__main__":
    if "your-site" in DOMAIN:
        print("❌ Error: Please set your ATLASSIAN_DOMAIN, ATLASSIAN_USER_EMAIL, and ATLASSIAN_API_TOKEN environment variables first.")
    else:
        main()
