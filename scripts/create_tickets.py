#!/usr/bin/env python3
"""
Interactive JIRA Ticket Creator
Command-line interface for creating VDB project tickets
"""

import sys
import os
import json
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))

from ticket_generator import TicketGenerator


class TicketCreatorCLI:
    """Interactive CLI for creating JIRA tickets"""
    
    def __init__(self):
        self.generator = TicketGenerator(
            historical_data_path="/mnt/user-data/outputs/historical-tickets-data.json"
        )
        self.tickets_to_create = []
    
    def print_header(self, text: str):
        """Print formatted header"""
        print("\n" + "=" * 70)
        print(text.center(70))
        print("=" * 70)
    
    def print_section(self, text: str):
        """Print formatted section"""
        print("\n" + "-" * 70)
        print(text)
        print("-" * 70)
    
    def get_input(self, prompt: str, default: str = None, options: list = None) -> str:
        """Get user input with optional default and validation"""
        if options:
            print(f"\n{prompt}")
            for i, option in enumerate(options, 1):
                print(f"  {i}. {option}")
            while True:
                choice = input(f"\nEnter choice (1-{len(options)}): ").strip()
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(options):
                        return options[idx]
                except ValueError:
                    pass
                print("Invalid choice. Please try again.")
        else:
            prompt_text = f"\n{prompt}"
            if default:
                prompt_text += f" [{default}]"
            prompt_text += ": "
            
            value = input(prompt_text).strip()
            return value if value else default
    
    def get_yes_no(self, prompt: str, default: bool = True) -> bool:
        """Get yes/no input"""
        default_text = "Y/n" if default else "y/N"
        response = input(f"\n{prompt} ({default_text}): ").strip().lower()
        
        if not response:
            return default
        return response in ['y', 'yes', 'true', '1']
    
    def create_single_ticket(self):
        """Interactive wizard for creating a single ticket"""
        self.print_header("CREATE SINGLE TICKET")
        
        # Select ticket type
        ticket_types = [
            ("view_table_data", "View Table Data"),
            ("add_entity", "Add Entity/Record"),
            ("perform_actions", "Perform Actions"),
            ("search_filter", "Search & Filter"),
            ("download", "Download Data"),
            ("upload_csv", "Upload CSV"),
            ("backend_architecture", "Backend Architecture"),
            ("rbac_permissions", "RBAC Permissions"),
            ("nav_menu", "Navigation Menu"),
            ("edge_cases", "Edge Cases"),
            ("generic_story", "Generic Story")
        ]
        
        print("\nSelect ticket type:")
        for i, (key, label) in enumerate(ticket_types, 1):
            print(f"  {i}. {label}")
        
        choice = int(input(f"\nEnter choice (1-{len(ticket_types)}): ").strip()) - 1
        ticket_type_key, ticket_type_label = ticket_types[choice]
        
        # Get common fields
        feature_name = self.get_input("Feature/Epic name", "My Feature")
        
        # Type-specific fields
        kwargs = {"feature_name": feature_name}
        
        if ticket_type_key in ["view_table_data", "search_filter", "perform_actions"]:
            tab_name = self.get_input("Tab name (if applicable)", feature_name)
            kwargs["tab_name"] = tab_name
        
        if ticket_type_key == "add_entity":
            entity_name = self.get_input("Entity name (e.g., 'patient', 'claim')", "record")
            kwargs["entity_name"] = entity_name
        
        if ticket_type_key in ["backend_architecture", "nav_menu", "rbac_permissions"]:
            scope = self.get_input("Scope (FE/BE/Full-stack)", "Full-stack", ["FE", "BE", "Full-stack"])
            if scope != "Full-stack":
                kwargs["scope"] = scope
        
        # Generate ticket
        summary = self.generator.generate_summary(ticket_type_key, **kwargs)
        description = self.generator.generate_description(ticket_type_key, **kwargs)
        priority = self.generator.suggest_priority(ticket_type_key)
        
        # Allow user to override
        priority = self.get_input("Priority", priority, ["Highest", "High", "Medium", "Low"])
        
        # Preview
        self.print_section("TICKET PREVIEW")
        print(f"\nType: Story")
        print(f"Priority: {priority}")
        print(f"Summary: {summary}")
        print(f"\nDescription:\n{description}")
        
        # Confirm
        if self.get_yes_no("Add this ticket to batch?", True):
            self.tickets_to_create.append({
                "type": "Story",
                "summary": summary,
                "description": description,
                "priority": priority
            })
            print(f"\n✅ Ticket added to batch ({len(self.tickets_to_create)} total)")
        else:
            print("\n❌ Ticket discarded")
    
    def create_epic_tickets(self):
        """Interactive wizard for creating a full epic ticket set"""
        self.print_header("CREATE EPIC TICKET SET")
        
        epic_name = self.get_input("Epic name", "New Feature")
        
        # Configuration
        include_backend = self.get_yes_no("Include Backend Architecture ticket?", True)
        include_rbac = self.get_yes_no("Include RBAC Permissions ticket?", True)
        include_nav = self.get_yes_no("Include Navigation Menu ticket?", True)
        
        # Tabs
        tabs = []
        if self.get_yes_no("Does this feature have tabs/sections?", False):
            print("\nEnter tab names (one per line, empty line to finish):")
            while True:
                tab = input("  Tab name: ").strip()
                if not tab:
                    break
                tabs.append(tab)
        
        # Generate tickets
        tickets = self.generator.generate_epic_tickets(
            epic_name=epic_name,
            include_backend=include_backend,
            include_rbac=include_rbac,
            include_nav=include_nav,
            tabs=tabs
        )
        
        # Preview
        self.print_section(f"GENERATED {len(tickets)} TICKETS")
        for i, ticket in enumerate(tickets, 1):
            print(f"\n{i}. [{ticket['priority']}] {ticket['summary']}")
        
        # Confirm
        if self.get_yes_no(f"\nAdd all {len(tickets)} tickets to batch?", True):
            self.tickets_to_create.extend(tickets)
            print(f"\n✅ {len(tickets)} tickets added to batch ({len(self.tickets_to_create)} total)")
        else:
            print("\n❌ Tickets discarded")
    
    def review_batch(self):
        """Review all tickets in the batch"""
        if not self.tickets_to_create:
            print("\n⚠️  No tickets in batch")
            return
        
        self.print_header(f"BATCH REVIEW ({len(self.tickets_to_create)} tickets)")
        
        for i, ticket in enumerate(self.tickets_to_create, 1):
            print(f"\n{i}. [{ticket['priority']}] {ticket['summary']}")
    
    def export_batch(self):
        """Export batch to JSON file"""
        if not self.tickets_to_create:
            print("\n⚠️  No tickets to export")
            return
        
        filename = self.get_input("Output filename", "tickets_batch.json")
        filepath = f"/mnt/user-data/outputs/{filename}"
        
        with open(filepath, 'w') as f:
            json.dump({
                "tickets": self.tickets_to_create,
                "count": len(self.tickets_to_create),
                "project": "VDB"
            }, f, indent=2)
        
        print(f"\n✅ Exported {len(self.tickets_to_create)} tickets to {filepath}")
    
    def clear_batch(self):
        """Clear the ticket batch"""
        if self.get_yes_no(f"Clear all {len(self.tickets_to_create)} tickets from batch?", False):
            self.tickets_to_create = []
            print("\n✅ Batch cleared")
    
    def main_menu(self):
        """Main menu loop"""
        self.print_header("JIRA TICKET CREATOR - VDB PROJECT")
        
        while True:
            print("\n" + "=" * 70)
            print("MAIN MENU")
            print("=" * 70)
            print(f"\nCurrent batch: {len(self.tickets_to_create)} tickets")
            print("\n1. Create single ticket")
            print("2. Create epic ticket set")
            print("3. Review batch")
            print("4. Export batch to JSON")
            print("5. Clear batch")
            print("6. Exit")
            
            choice = input("\nEnter choice (1-6): ").strip()
            
            if choice == "1":
                self.create_single_ticket()
            elif choice == "2":
                self.create_epic_tickets()
            elif choice == "3":
                self.review_batch()
            elif choice == "4":
                self.export_batch()
            elif choice == "5":
                self.clear_batch()
            elif choice == "6":
                if not self.tickets_to_create or self.get_yes_no(f"Exit without exporting {len(self.tickets_to_create)} tickets?", False):
                    print("\n👋 Goodbye!")
                    break
            else:
                print("\n❌ Invalid choice")


def main():
    """Entry point"""
    cli = TicketCreatorCLI()
    try:
        cli.main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
