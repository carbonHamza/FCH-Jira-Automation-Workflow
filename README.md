# JIRA Ticket Automation System - VDB Project

> **Automated JIRA ticket creation following VDB project standards**
> 
> Based on analysis of 75 historical tickets across 6 epics

---

## 📁 Directory Structure

```
jira-automation/
├── scripts/
│   ├── create_tickets.py      # Interactive CLI for ticket creation
│   └── push_to_jira.py         # Push tickets to JIRA via API
├── utils/
│   └── ticket_generator.py    # Core ticket generation logic
├── templates/
│   └── (Future: ticket templates)
└── README.md                   # This file
```

---

## 🚀 Quick Start

### 1. Interactive Ticket Creation

Create tickets using the interactive wizard:

```bash
cd /home/claude/jira-automation
python3 scripts/create_tickets.py
```

This will launch an interactive menu where you can:
- Create individual tickets
- Generate full epic ticket sets
- Review your batch
- Export to JSON

### 2. Create from JSON Batch File

If you have a pre-made batch file:

```bash
# Dry run (preview only)
python3 scripts/push_to_jira.py tickets_batch.json --dry-run

# Actually create in JIRA
python3 scripts/push_to_jira.py tickets_batch.json --epic-key VDB-1234
```

---

## 📋 Ticket Types Supported

The automation system supports all VDB standard ticket types:

| Type | Description | Priority Suggestion |
|------|-------------|---------------------|
| **view_table_data** | View data in table format | High |
| **add_entity** | Add/create new records | High |
| **perform_actions** | Perform actions on records | High |
| **search_filter** | Search and filter functionality | High |
| **download** | Download data | Medium |
| **upload_csv** | Bulk upload via CSV | Medium |
| **backend_architecture** | Backend scaffolding | High |
| **rbac_permissions** | RBAC configuration | High |
| **nav_menu** | Navigation menu items | High |
| **edge_cases** | Edge case handling | Medium |

---

## 🎯 Usage Examples

### Example 1: Create a Full Epic

```python
from ticket_generator import TicketGenerator

generator = TicketGenerator()

# Generate standard epic ticket set
tickets = generator.generate_epic_tickets(
    epic_name="Patient Management",
    include_backend=True,
    include_rbac=True,
    include_nav=True,
    tabs=["Active Patients", "Discharged", "Admitted"]
)

# This generates:
# - 1 Backend Architecture ticket
# - 1 RBAC Permissions ticket
# - 1 Navigation Menu ticket
# - 2 tickets per tab (View + Search/Filter)
# Total: 9 tickets
```

### Example 2: Create Single Ticket Programmatically

```python
from ticket_generator import TicketGenerator

generator = TicketGenerator()

# Generate summary
summary = generator.generate_summary(
    ticket_type="add_entity",
    feature_name="Patient Management",
    entity_name="patient"
)

# Generate description
description = generator.generate_description(
    ticket_type="add_entity",
    entity_name="patient",
    fields=[
        {"name": "First Name", "type": "Text field", "mandatory": True},
        {"name": "Last Name", "type": "Text field", "mandatory": True},
        {"name": "DOB", "type": "Date picker", "mandatory": True},
        {"name": "Notes", "type": "Large text", "mandatory": False}
    ]
)

# Suggest priority
priority = generator.suggest_priority("add_entity")

print(f"Summary: {summary}")
print(f"Priority: {priority}")
print(f"\nDescription:\n{description}")
```

### Example 3: Batch Create from Meeting Notes

```python
# Suppose you have meeting notes with action items
action_items = [
    "User should be able to view patient data in table",
    "User should be able to add new patients",
    "User should be able to search and filter patients"
]

generator = TicketGenerator()
tickets = []

for item in action_items:
    # Detect ticket type
    ticket_type = generator.detect_ticket_type(item)
    
    # Generate ticket
    summary = generator.generate_summary(ticket_type, "Patient Management")
    description = generator.generate_description(ticket_type)
    priority = generator.suggest_priority(ticket_type)
    
    tickets.append({
        "type": "Story",
        "summary": summary,
        "description": description,
        "priority": priority
    })

# Export to JSON
import json
with open('/mnt/user-data/outputs/batch.json', 'w') as f:
    json.dump({"tickets": tickets}, f, indent=2)
```

---

## 📖 Standards Reference

All generated tickets follow the **VDB JIRA Ticket Standards** documented in:
- `/mnt/project/VDB-JIRA-Ticket-Standards.md`

Key standards applied:
- ✅ Consistent summary patterns
- ✅ Standardized description formatting
- ✅ Proper priority assignment
- ✅ FE/BE scope prefixes
- ✅ Facility scope specification
- ✅ Mobile responsiveness notes
- ✅ Standard field specifications

---

## 🔧 Configuration

### Cloud ID
Default: `b62faa91-9d69-4d74-b5d3-a6ca7ee49309`

To use a different Atlassian instance:
```bash
python3 scripts/push_to_jira.py batch.json --cloud-id YOUR_CLOUD_ID
```

### Historical Data
The system uses historical ticket data from:
- `/mnt/user-data/outputs/historical-tickets-data.json`

This contains 75 analyzed tickets across 6 epics used for pattern detection.

---

## 📝 Ticket Generation Workflow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Define Requirements                                       │
│    - Feature name                                            │
│    - Ticket type                                             │
│    - Scope (FE/BE/Full-stack)                               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Generate Ticket Content                                   │
│    - Summary following VDB patterns                          │
│    - Description with proper formatting                      │
│    - Priority suggestion                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Review & Edit                                             │
│    - Preview generated content                               │
│    - Make adjustments if needed                              │
│    - Add to batch                                            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Export Batch                                              │
│    - Save as JSON file                                       │
│    - Ready for JIRA creation                                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. Create in JIRA                                            │
│    - Push via Atlassian API                                  │
│    - Link to epic (optional)                                 │
│    - Verify creation                                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎨 Customization

### Adding New Templates

To add a new ticket template:

1. Edit `utils/ticket_generator.py`
2. Add template method (e.g., `_template_my_new_type`)
3. Update `generate_description()` to call it
4. Add to `detect_ticket_type()` pattern matching

Example:
```python
def _template_my_new_type(self, **kwargs) -> str:
    """Generate my new type ticket description"""
    return """**Acceptance criteria:**
    
<Your template here>

---

### Important Notes

* <Standard notes>
"""
```

### Modifying Standards

To update ticket standards:
1. Update `/mnt/project/VDB-JIRA-Ticket-Standards.md`
2. Modify template methods in `ticket_generator.py`
3. Update detection patterns if needed

---

## 🐛 Troubleshooting

### Tickets not following standards?
- Check historical data is loaded correctly
- Verify template methods match standards document
- Review generated output before pushing to JIRA

### Import errors?
```bash
# Ensure you're in the right directory
cd /home/claude/jira-automation

# Check Python path
python3 -c "import sys; print(sys.path)"
```

### API connection issues?
- Verify Cloud ID is correct
- Check Atlassian connector is configured
- Test with dry-run first

---

## 📊 Analytics

### Historical Data Coverage

Based on analysis of **75 tickets** across **6 epics**:

| Epic | Issues | Completion |
|------|--------|------------|
| VDB-2298 (Pre-Intake) | 15 | 80% |
| VDB-1739 (Mortality Log) | 11 | 100% ✅ |
| VDB-1710 (53A Log) | 12 | 100% ✅ |
| VDB-1689 (Infirmary Log) | 15 | 100% ✅ |
| VDB-1413 (Rate Code) | 14 | 14% |
| VDB-1441 (Claim History) | 8 | 0% |

**Total description coverage: 69.3%**

This provides strong pattern recognition for:
- Summary conventions
- Description formatting
- Priority assignment
- Field specifications
- Standard workflows

---

## 🔮 Future Enhancements

Planned features:
- [ ] AI-powered ticket generation from meeting transcripts
- [ ] Figma design integration
- [ ] Automatic epic decomposition
- [ ] Dependency detection and linking
- [ ] Batch editing capabilities
- [ ] Template customization UI
- [ ] Integration with project management tools

---

## 📞 Support

For issues or questions:
1. Check the standards document: `/mnt/project/VDB-JIRA-Ticket-Standards.md`
2. Review historical examples: `/mnt/user-data/outputs/historical-tickets-data.json`
3. Test with dry-run mode before production use

---

## 📜 License

Internal tool for VDB project. Based on patterns extracted from 75 historical JIRA tickets.

**Last Updated:** 2026-02-12
