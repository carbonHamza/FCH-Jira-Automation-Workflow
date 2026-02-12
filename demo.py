#!/usr/bin/env python3
"""
DEMO: Generate Tickets for a New Feature
Shows end-to-end workflow for creating a full epic ticket set
"""

import sys
import json
from pathlib import Path

# Add utils to path
sys.path.insert(0, str(Path(__file__).parent / 'utils'))

from ticket_generator import TicketGenerator


def demo_single_ticket():
    """Demo: Create a single ticket"""
    print("\n" + "=" * 70)
    print("DEMO 1: Create a Single Ticket")
    print("=" * 70)
    
    generator = TicketGenerator()
    
    # Generate a "View Table Data" ticket
    summary = generator.generate_summary(
        ticket_type="view_table_data",
        feature_name="Medication Log",
        tab_name="Active Medications"
    )
    
    description = generator.generate_description(
        ticket_type="view_table_data",
        feature_name="Medication Log",
        tab_name="Active Medications",
        columns=[
            "Patient Name (Last Name, First Name)",
            "Medication Name",
            "Dosage",
            "Frequency",
            "Prescribed Date",
            "Status",
            "Actions (Edit, Discontinue, View History)"
        ],
        facility_scope="facility-specific"
    )
    
    priority = generator.suggest_priority("view_table_data")
    
    print(f"\n📋 Ticket Type: Story")
    print(f"🎯 Priority: {priority}")
    print(f"📝 Summary: {summary}")
    print(f"\n📄 Description:\n{description}")
    
    return {
        "type": "Story",
        "summary": summary,
        "description": description,
        "priority": priority
    }


def demo_epic_generation():
    """Demo: Generate a full epic ticket set"""
    print("\n" + "=" * 70)
    print("DEMO 2: Generate Full Epic Ticket Set")
    print("=" * 70)
    
    generator = TicketGenerator()
    
    # Generate tickets for "Medication Log" feature
    tickets = generator.generate_epic_tickets(
        epic_name="Medication Log",
        include_backend=True,
        include_rbac=True,
        include_nav=True,
        tabs=["Active Medications", "Discontinued", "History"]
    )
    
    print(f"\n✅ Generated {len(tickets)} tickets:")
    print("\n" + "-" * 70)
    
    for i, ticket in enumerate(tickets, 1):
        print(f"\n{i}. [{ticket['priority']}] {ticket['type']}")
        print(f"   {ticket['summary']}")
    
    print("\n" + "-" * 70)
    
    return tickets


def demo_custom_fields():
    """Demo: Create ticket with custom fields"""
    print("\n" + "=" * 70)
    print("DEMO 3: Create Ticket with Custom Fields")
    print("=" * 70)
    
    generator = TicketGenerator()
    
    # Generate "Add Entity" ticket with specific fields
    summary = generator.generate_summary(
        ticket_type="add_entity",
        feature_name="Medication Log",
        entity_name="medication"
    )
    
    description = generator.generate_description(
        ticket_type="add_entity",
        entity_name="medication",
        fields=[
            {
                "name": "Patient Name",
                "type": "Searchable dropdown",
                "mandatory": True
            },
            {
                "name": "Medication Name",
                "type": "Text field with autocomplete",
                "mandatory": True
            },
            {
                "name": "Dosage",
                "type": "Text field",
                "mandatory": True
            },
            {
                "name": "Frequency",
                "type": "Dropdown",
                "mandatory": True,
                "default": "Once daily"
            },
            {
                "name": "Route",
                "type": "Dropdown",
                "mandatory": True
            },
            {
                "name": "Prescribed Date",
                "type": "Date picker",
                "mandatory": True,
                "default": "Today"
            },
            {
                "name": "Prescribing Physician",
                "type": "Searchable dropdown",
                "mandatory": True
            },
            {
                "name": "Special Instructions",
                "type": "Large text field",
                "mandatory": False
            }
        ],
        facility_scope="facility-specific"
    )
    
    priority = generator.suggest_priority("add_entity")
    
    print(f"\n📋 Ticket Type: Story")
    print(f"🎯 Priority: {priority}")
    print(f"📝 Summary: {summary}")
    print(f"\n📄 Description:\n{description}")
    
    return {
        "type": "Story",
        "summary": summary,
        "description": description,
        "priority": priority
    }


def demo_search_filter():
    """Demo: Create search and filter ticket"""
    print("\n" + "=" * 70)
    print("DEMO 4: Create Search & Filter Ticket")
    print("=" * 70)
    
    generator = TicketGenerator()
    
    summary = generator.generate_summary(
        ticket_type="search_filter",
        feature_name="Medication Log",
        tab_name="Active Medications"
    )
    
    description = generator.generate_description(
        ticket_type="search_filter",
        feature_name="Medication Log",
        tab_name="Active Medications",
        search_fields=["Patient Name", "Medication Name"],
        filters=[
            {
                "name": "Prescribed Date (From/To)",
                "type": "Date range picker",
                "default": "Empty"
            },
            {
                "name": "Route",
                "type": "Dropdown",
                "default": "All"
            },
            {
                "name": "Frequency",
                "type": "Dropdown",
                "default": "All"
            },
            {
                "name": "Prescribing Physician",
                "type": "Searchable dropdown",
                "default": "All"
            }
        ]
    )
    
    priority = generator.suggest_priority("search_filter")
    
    print(f"\n📋 Ticket Type: Story")
    print(f"🎯 Priority: {priority}")
    print(f"📝 Summary: {summary}")
    print(f"\n📄 Description:\n{description}")
    
    return {
        "type": "Story",
        "summary": summary,
        "description": description,
        "priority": priority
    }


def export_all_demos():
    """Export all demo tickets to JSON file"""
    print("\n" + "=" * 70)
    print("EXPORTING ALL DEMO TICKETS")
    print("=" * 70)
    
    all_tickets = []
    
    # Run all demos and collect tickets
    all_tickets.append(demo_single_ticket())
    all_tickets.extend(demo_epic_generation())
    all_tickets.append(demo_custom_fields())
    all_tickets.append(demo_search_filter())
    
    # Export to file
    output_file = "/mnt/user-data/outputs/medication-log-tickets.json"
    
    export_data = {
        "project": "VDB",
        "epic_name": "Medication Log",
        "total_tickets": len(all_tickets),
        "tickets": all_tickets,
        "metadata": {
            "generated_by": "JIRA Ticket Automation System",
            "date": "2026-02-12",
            "based_on_standards": "VDB-JIRA-Ticket-Standards.md"
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(export_data, f, indent=2)
    
    print(f"\n✅ Exported {len(all_tickets)} tickets to:")
    print(f"   {output_file}")
    print("\n📊 Summary:")
    print(f"   - Backend Architecture: 1 ticket")
    print(f"   - RBAC Permissions: 1 ticket")
    print(f"   - Navigation Menu: 1 ticket")
    print(f"   - Tab View/Filter tickets: 6 tickets (3 tabs × 2)")
    print(f"   - Custom tickets: 3 tickets")
    print(f"   Total: {len(all_tickets)} tickets")
    
    return output_file


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("JIRA TICKET AUTOMATION - DEMO SUITE")
    print("=" * 70)
    print("\nThis demo shows how to generate tickets for a new 'Medication Log' feature")
    
    # Run individual demos
    demo_single_ticket()
    demo_epic_generation()
    demo_custom_fields()
    demo_search_filter()
    
    # Export everything
    output_file = export_all_demos()
    
    print("\n" + "=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("\n1. Review the generated tickets:")
    print(f"   cat {output_file}")
    print("\n2. Test with dry-run:")
    print(f"   python3 scripts/push_to_jira.py {output_file} --dry-run")
    print("\n3. Create in JIRA (when ready):")
    print(f"   python3 scripts/push_to_jira.py {output_file} --epic-key VDB-XXXX")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
