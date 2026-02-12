# 🚀 Quick Start Guide - JIRA Ticket Automation

## ⚡ 5-Minute Setup

### Step 1: Verify Installation
```bash
cd /mnt/user-data/outputs/jira-automation
ls -la
```

You should see:
- ✅ `scripts/` - Automation scripts
- ✅ `utils/` - Core libraries
- ✅ `README.md` - Full documentation
- ✅ `demo.py` - Example usage

---

## 🎯 Common Use Cases

### Use Case 1: Generate Tickets for a New Feature

**Scenario:** You need to create tickets for a new "Patient Portal" feature with 2 tabs.

**Solution:**
```bash
python3 << 'EOF'
from utils.ticket_generator import TicketGenerator

generator = TicketGenerator()

tickets = generator.generate_epic_tickets(
    epic_name="Patient Portal",
    include_backend=True,
    include_rbac=True,
    include_nav=True,
    tabs=["Dashboard", "Messages"]
)

import json
with open('/mnt/user-data/outputs/patient-portal-tickets.json', 'w') as f:
    json.dump({"tickets": tickets}, f, indent=2)

print(f"✅ Generated {len(tickets)} tickets!")
EOF
```

**Result:** 7 tickets created in JSON file, ready to push to JIRA.

---

### Use Case 2: Interactive Ticket Creation

**Scenario:** You want to create tickets interactively with a wizard.

**Solution:**
```bash
python3 scripts/create_tickets.py
```

Follow the prompts to:
1. Select ticket type
2. Fill in details
3. Add to batch
4. Export when done

---

### Use Case 3: Create Single Specific Ticket

**Scenario:** You need just one "Search & Filter" ticket.

**Solution:**
```bash
python3 << 'EOF'
from utils.ticket_generator import TicketGenerator

generator = TicketGenerator()

summary = generator.generate_summary(
    ticket_type="search_filter",
    feature_name="Lab Results",
    tab_name="Pending Results"
)

description = generator.generate_description(
    ticket_type="search_filter",
    tab_name="Pending Results",
    search_fields=["Patient Name", "Test Name"],
    filters=[
        {"name": "Test Date (From/To)", "type": "Date range", "default": "Empty"},
        {"name": "Test Type", "type": "Dropdown", "default": "All"},
        {"name": "Status", "type": "Dropdown", "default": "All"}
    ]
)

print("Summary:", summary)
print("\nDescription:", description)
EOF
```

---

## 📝 Ticket Type Cheat Sheet

| I need to... | Use this type | Example |
|--------------|---------------|---------|
| Show data in a table | `view_table_data` | Lab results table |
| Add new records | `add_entity` | Add new patient |
| Edit/delete/actions | `perform_actions` | Edit patient info |
| Search and filter | `search_filter` | Filter by date |
| Download CSV/PDF | `download` | Download reports |
| Upload bulk data | `upload_csv` | Import claims |
| Backend setup | `backend_architecture` | Database models |
| User permissions | `rbac_permissions` | Role access |
| Navigation item | `nav_menu` | Add menu item |
| Handle edge cases | `edge_cases` | Deleted user handling |

---

## 🎨 Customization Examples

### Custom Field Specifications

```python
from utils.ticket_generator import TicketGenerator

generator = TicketGenerator()

description = generator.generate_description(
    ticket_type="add_entity",
    entity_name="appointment",
    fields=[
        {
            "name": "Patient",
            "type": "Searchable dropdown",
            "mandatory": True
        },
        {
            "name": "Appointment Date",
            "type": "Date picker",
            "mandatory": True,
            "default": "Tomorrow"
        },
        {
            "name": "Duration",
            "type": "Dropdown",
            "mandatory": True,
            "default": "30 minutes"
        },
        {
            "name": "Notes",
            "type": "Large text",
            "mandatory": False
        }
    ],
    facility_scope="facility-specific"
)
```

### Custom Table Columns

```python
description = generator.generate_description(
    ticket_type="view_table_data",
    tab_name="Appointments",
    columns=[
        "Patient Name (Last, First)",
        "Date & Time (MM/DD/YYYY HH:MM)",
        "Provider",
        "Type (Office Visit, Telehealth, Follow-up)",
        "Status (Scheduled, Checked-In, Completed, Cancelled)",
        "Actions (Edit, Cancel, Reschedule, View Notes)"
    ]
)
```

---

## 🔄 Complete Workflow Example

### Scenario: New "Appointment Scheduler" Feature

```bash
# 1. Run the demo to see examples
python3 demo.py

# 2. Create your tickets
python3 << 'EOF'
import sys
sys.path.insert(0, 'utils')
from ticket_generator import TicketGenerator
import json

generator = TicketGenerator()

tickets = generator.generate_epic_tickets(
    epic_name="Appointment Scheduler",
    include_backend=True,
    include_rbac=True,
    include_nav=True,
    tabs=["Upcoming", "Today", "History"]
)

# Add custom "Add Appointment" ticket
tickets.append({
    "type": "Story",
    "summary": generator.generate_summary("add_entity", "Appointment Scheduler", entity_name="appointment"),
    "description": generator.generate_description(
        "add_entity",
        entity_name="appointment",
        facility_scope="facility-specific"
    ),
    "priority": "High"
})

with open('/mnt/user-data/outputs/appointment-scheduler.json', 'w') as f:
    json.dump({"tickets": tickets, "total": len(tickets)}, f, indent=2)

print(f"✅ Created {len(tickets)} tickets")
EOF

# 3. Review the output
cat /mnt/user-data/outputs/appointment-scheduler.json | head -50

# 4. Test with dry-run
python3 scripts/push_to_jira.py /mnt/user-data/outputs/appointment-scheduler.json --dry-run

# 5. Push to JIRA (when ready)
# python3 scripts/push_to_jira.py /mnt/user-data/outputs/appointment-scheduler.json --epic-key VDB-XXXX
```

---

## 🐛 Troubleshooting

### Problem: "Module not found"
**Solution:**
```bash
cd /mnt/user-data/outputs/jira-automation
python3 -c "import sys; sys.path.insert(0, 'utils'); from ticket_generator import TicketGenerator; print('✅ OK')"
```

### Problem: Tickets don't follow VDB standards
**Solution:** Check that you're using the correct ticket types and field specifications. Review:
```bash
cat README.md | grep "Ticket Types"
```

### Problem: Want to modify templates
**Solution:** Edit `utils/ticket_generator.py` and update the `_template_*` methods.

---

## 📚 Resources

- **Full Documentation:** `README.md`
- **Standards Reference:** `/mnt/project/VDB-JIRA-Ticket-Standards.md`
- **Historical Examples:** `/mnt/user-data/outputs/historical-tickets-data.json`
- **Demo Script:** `demo.py`

---

## 💡 Pro Tips

1. **Start with demo.py** - See working examples before creating your own
2. **Use dry-run** - Always test with `--dry-run` before pushing to JIRA
3. **Review generated tickets** - Check the JSON output before submission
4. **Batch similar tickets** - Create all tickets for a feature in one batch
5. **Follow naming conventions** - Use the exact patterns from standards

---

## 🎉 Success Indicators

You're successfully using the automation if:
- ✅ Tickets follow VDB naming patterns
- ✅ Descriptions include "Acceptance criteria" sections
- ✅ Priority is automatically suggested correctly
- ✅ Field specifications use standard formats
- ✅ Facility scope is always specified
- ✅ Mobile behavior notes are included for tables

---

**Need Help?** Check the full `README.md` or review historical ticket examples!
