#!/usr/bin/env python3
"""
JIRA Ticket Creator - Atlassian API Integration
Creates tickets in JIRA using the Atlassian connector
"""

import json
import sys
from pathlib import Path


class JiraTicketCreator:
    """Create tickets in JIRA via Atlassian API"""
    
    def __init__(self, cloud_id: str = "b62faa91-9d69-4d74-b5d3-a6ca7ee49309"):
        self.cloud_id = cloud_id
        self.project_key = "VDB"
    
    def create_issue(self, summary: str, description: str, 
                    issue_type: str = "Story", priority: str = "Medium",
                    epic_key: str = None) -> dict:
        """
        Create a single JIRA issue
        
        This is a placeholder for the actual API call.
        In Claude's automation environment, you would call:
        
        Atlassian:createJiraIssue with parameters:
        - cloudId: self.cloud_id
        - projectKey: self.project_key
        - issueTypeName: issue_type
        - summary: summary
        - description: description
        - additional_fields: {
            "priority": {"name": priority},
            "parent": {"key": epic_key} if epic_key else None
          }
        
        Returns:
            dict: Created issue details
        """
        
        issue_data = {
            "cloudId": self.cloud_id,
            "projectKey": self.project_key,
            "issueTypeName": issue_type,
            "summary": summary,
            "description": description,
            "additional_fields": {
                "priority": {"name": priority}
            }
        }
        
        if epic_key:
            issue_data["parent"] = epic_key
        
        # This would be the actual API call in production
        # result = Atlassian:createJiraIssue(**issue_data)
        
        return {
            "message": "Would create ticket (API call placeholder)",
            "data": issue_data
        }
    
    def create_epic(self, summary: str, description: str = None) -> dict:
        """
        Create an Epic in JIRA
        
        Returns:
            dict: Created epic details with epic_key
        """
        
        epic_data = {
            "cloudId": self.cloud_id,
            "projectKey": self.project_key,
            "issueTypeName": "Epic",
            "summary": summary,
            "description": description or f"Epic for {summary}",
        }
        
        # This would be the actual API call in production
        # result = Atlassian:createJiraIssue(**epic_data)
        
        return {
            "message": "Would create epic (API call placeholder)",
            "epic_key": "VDB-XXXX",  # Would be returned by API
            "data": epic_data
        }
    
    def create_batch(self, tickets: list, epic_key: str = None) -> dict:
        """
        Create multiple tickets in batch
        
        Args:
            tickets: List of ticket dictionaries
            epic_key: Optional epic to link tickets to
            
        Returns:
            dict: Results summary
        """
        
        results = {
            "created": [],
            "failed": [],
            "total": len(tickets)
        }
        
        for i, ticket in enumerate(tickets, 1):
            print(f"\nCreating ticket {i}/{len(tickets)}: {ticket['summary'][:60]}...")
            
            try:
                result = self.create_issue(
                    summary=ticket['summary'],
                    description=ticket['description'],
                    issue_type=ticket.get('type', 'Story'),
                    priority=ticket.get('priority', 'Medium'),
                    epic_key=epic_key
                )
                results["created"].append({
                    "summary": ticket['summary'],
                    "result": result
                })
                print(f"  ✅ Created (placeholder)")
            except Exception as e:
                results["failed"].append({
                    "summary": ticket['summary'],
                    "error": str(e)
                })
                print(f"  ❌ Failed: {e}")
        
        return results
    
    def preview_tickets(self, tickets: list):
        """Preview tickets before creation"""
        print("\n" + "=" * 70)
        print(f"TICKET PREVIEW ({len(tickets)} tickets)")
        print("=" * 70)
        
        for i, ticket in enumerate(tickets, 1):
            print(f"\n{i}. [{ticket.get('priority', 'Medium')}] {ticket.get('type', 'Story')}")
            print(f"   {ticket['summary']}")
            print(f"   Description length: {len(ticket.get('description', ''))} chars")
    
    def load_batch_file(self, filepath: str) -> dict:
        """Load tickets from JSON file"""
        with open(filepath, 'r') as f:
            return json.load(f)
    
    def create_from_file(self, filepath: str, epic_key: str = None, 
                        dry_run: bool = False):
        """Create tickets from a JSON batch file"""
        
        print(f"\n📂 Loading tickets from: {filepath}")
        data = self.load_batch_file(filepath)
        tickets = data.get('tickets', [])
        
        print(f"📋 Found {len(tickets)} tickets")
        
        # Preview
        self.preview_tickets(tickets)
        
        if dry_run:
            print("\n🔍 DRY RUN MODE - No tickets will be created")
            return
        
        # Confirm
        response = input(f"\n❓ Create {len(tickets)} tickets in JIRA? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("❌ Cancelled")
            return
        
        # Create tickets
        print("\n🚀 Creating tickets...")
        results = self.create_batch(tickets, epic_key=epic_key)
        
        # Summary
        print("\n" + "=" * 70)
        print("CREATION SUMMARY")
        print("=" * 70)
        print(f"✅ Created: {len(results['created'])}")
        print(f"❌ Failed: {len(results['failed'])}")
        print(f"📊 Total: {results['total']}")
        
        if results['failed']:
            print("\nFailed tickets:")
            for failed in results['failed']:
                print(f"  - {failed['summary']}")
                print(f"    Error: {failed['error']}")


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Create JIRA tickets from JSON batch file")
    parser.add_argument('batch_file', help="Path to JSON batch file")
    parser.add_argument('--epic-key', help="Epic key to link tickets to (e.g., VDB-1234)")
    parser.add_argument('--dry-run', action='store_true', help="Preview without creating")
    parser.add_argument('--cloud-id', default="b62faa91-9d69-4d74-b5d3-a6ca7ee49309", 
                       help="Atlassian Cloud ID")
    
    args = parser.parse_args()
    
    creator = JiraTicketCreator(cloud_id=args.cloud_id)
    creator.create_from_file(
        filepath=args.batch_file,
        epic_key=args.epic_key,
        dry_run=args.dry_run
    )


if __name__ == "__main__":
    main()
