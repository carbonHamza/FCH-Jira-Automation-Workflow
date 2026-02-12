# 🖥️ JIRA Automation - Complete CLI Guide

> **Command-line interface reference for the JIRA Automation System**
> 
> Version: 2.0 | Date: 2026-02-12

---

## 📚 Table of Contents

1. [Quick Reference](#quick-reference)
2. [Complete Workflow](#complete-workflow)
3. [Individual Tools](#individual-tools)
4. [Common Workflows](#common-workflows)
5. [Advanced Usage](#advanced-usage)
6. [Troubleshooting](#troubleshooting)
7. [Examples](#examples)

---

## 🚀 Quick Reference

### Most Common Commands

```bash
# 1. Complete automated workflow (with user review)
python3 scripts/workflow.py transcripts/meeting.txt

# 2. Process transcript only
python3 scripts/process_transcript.py transcripts/meeting.txt --review

# 3. Interactive ticket creator
python3 scripts/create_tickets.py

# 4. Push tickets to JIRA (dry run first!)
python3 scripts/push_to_jira.py tickets.json --dry-run
python3 scripts/push_to_jira.py tickets.json --epic-key VDB-1234

# 5. See demo examples
python3 demo.py
```

---

## 🔄 Complete Workflow

### workflow.py - End-to-End Orchestrator

**Purpose:** Run complete pipeline from transcript to JIRA-ready tickets with user review checkpoint.

#### Basic Usage

```bash
python3 scripts/workflow.py <transcript-file>
```

#### Options

| Option | Description | Example |
|--------|-------------|---------|
| `transcript` | Path to meeting transcript (required) | `transcripts/meeting.txt` |
| `--non-interactive` | Skip user review checkpoint | `--non-interactive` |
| `--step-by-step` | Pause after each step | `--step-by-step` |

#### Examples

```bash
# Standard usage with user review (RECOMMENDED)
python3 scripts/workflow.py transcripts/medication-log.txt

# Automated mode (no pauses)
python3 scripts/workflow.py transcripts/meeting.txt --non-interactive

# Step-by-step with pause after each phase
python3 scripts/workflow.py transcripts/meeting.txt --step-by-step
```

#### What It Does

```
Step 1: Process transcript → structured JSON
Step 2: Generate review report
Step 3: USER REVIEW CHECKPOINT ⏸️
Step 4: Generate JIRA tickets
Step 5: Save ticket batch
```

#### Output Files

```
transcripts/meeting.txt                    # Your input
transcripts/meeting_structured.json        # Extracted data
transcripts/meeting_review.txt             # Review report
transcripts/meeting_tickets.json           # Final tickets
```

#### Interactive Review

When workflow pauses, you'll see:

```
======================================================================
📋 STEP 2: User Review
======================================================================
[Review report displays here]

❓ Proceed with ticket generation? (yes/no/edit):
```

**Options:**
- `yes` → Continue to ticket generation
- `no` → Cancel workflow
- `edit` → Pause to manually edit structured JSON

---

## 🔧 Individual Tools

### 1. process_transcript.py - Transcript Processor

**Purpose:** Extract structured requirements from meeting transcripts.

#### Basic Usage

```bash
python3 scripts/process_transcript.py <transcript-file>
```

#### Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `transcript_file` | - | Input transcript (required) | - |
| `--output` | `-o` | Output JSON path | `<input>_structured.json` |
| `--review` | `-r` | Generate review report | `false` |

#### Examples

```bash
# Basic extraction
python3 scripts/process_transcript.py transcripts/meeting.txt

# With custom output path
python3 scripts/process_transcript.py transcripts/meeting.txt \
  --output structured-output/meeting.json

# Generate review report
python3 scripts/process_transcript.py transcripts/meeting.txt --review

# Full options
python3 scripts/process_transcript.py transcripts/meeting.txt \
  -o structured-output/custom.json \
  -r
```

#### Output

```
✅ Structured output saved to: transcripts/meeting_structured.json

📄 Review report saved to: transcripts/meeting_review.txt
```

#### What Gets Extracted

- Epic/feature names
- User stories
- Data fields & types
- Table columns
- Tabs/sections
- RBAC requirements
- Priority levels
- Validation rules

---

### 2. create_tickets.py - Interactive Ticket Creator

**Purpose:** Create tickets interactively through a menu-driven wizard.

#### Basic Usage

```bash
python3 scripts/create_tickets.py
```

#### No Options - Fully Interactive

This tool uses an interactive menu system. Just run it and follow the prompts.

#### Main Menu

```
======================================================================
MAIN MENU
======================================================================

Current batch: 0 tickets

1. Create single ticket
2. Create epic ticket set
3. Review batch
4. Export batch to JSON
5. Clear batch
6. Exit

Enter choice (1-6):
```

#### Creating Single Ticket

```
Step 1: Select ticket type
  1. View Table Data
  2. Add Entity/Record
  3. Perform Actions
  4. Search & Filter
  5. Download Data
  6. Upload CSV
  7. Backend Architecture
  8. RBAC Permissions
  9. Navigation Menu
  10. Edge Cases
  11. Generic Story

Step 2: Enter feature details
  Feature/Epic name: Medication Log
  Tab name (if applicable): Active Medications
  
Step 3: Preview ticket
  [Shows generated ticket]
  
Step 4: Confirm
  Add this ticket to batch? (yes/no):
```

#### Creating Epic Set

```
Epic name: Patient Portal
Include Backend Architecture ticket? (Y/n): y
Include RBAC Permissions ticket? (Y/n): y
Include Navigation Menu ticket? (Y/n): y
Does this feature have tabs/sections? (y/N): y

Enter tab names (one per line, empty line to finish):
  Tab name: Dashboard
  Tab name: Messages
  Tab name: 

✅ Generated 7 tickets!
Add all 7 tickets to batch? (yes/no):
```

#### Export Batch

```
Output filename [tickets_batch.json]: patient-portal-tickets.json

✅ Exported 7 tickets to /mnt/user-data/outputs/patient-portal-tickets.json
```

---

### 3. push_to_jira.py - JIRA Integration

**Purpose:** Push generated tickets to JIRA via Atlassian API.

#### Basic Usage

```bash
python3 scripts/push_to_jira.py <batch-file>
```

#### Options

| Option | Description | Example |
|--------|-------------|---------|
| `batch_file` | JSON file with tickets (required) | `tickets.json` |
| `--epic-key` | Link tickets to this epic | `--epic-key VDB-1234` |
| `--dry-run` | Preview without creating | `--dry-run` |
| `--cloud-id` | Atlassian Cloud ID | `--cloud-id <id>` |

#### Examples

```bash
# Dry run first (RECOMMENDED)
python3 scripts/push_to_jira.py transcripts/meeting_tickets.json --dry-run

# Create tickets without epic
python3 scripts/push_to_jira.py transcripts/meeting_tickets.json

# Create and link to epic
python3 scripts/push_to_jira.py transcripts/meeting_tickets.json \
  --epic-key VDB-1234

# Use different Atlassian instance
python3 scripts/push_to_jira.py tickets.json \
  --cloud-id b62faa91-9d69-4d74-b5d3-a6ca7ee49309
```

#### Dry Run Output

```
📂 Loading tickets from: transcripts/meeting_tickets.json
📋 Found 15 tickets

======================================================================
TICKET PREVIEW (15 tickets)
======================================================================

1. [High] Story
   BE: Implement backend architecture of "Medication Log"
   Description length: 245 chars

2. [High] Story
   User should be able to access and view data in table...
   Description length: 512 chars

🔍 DRY RUN MODE - No tickets will be created
```

#### Actual Creation Output

```
🚀 Creating tickets...

Creating ticket 1/15: BE: Implement backend architecture...
  ✅ Created (placeholder)

Creating ticket 2/15: User should be able to access and view...
  ✅ Created (placeholder)

======================================================================
CREATION SUMMARY
======================================================================
✅ Created: 15
❌ Failed: 0
📊 Total: 15
```

---

### 4. demo.py - Example Generator

**Purpose:** See working examples and test the system.

#### Basic Usage

```bash
python3 demo.py
```

#### No Options

Runs all demo scenarios and generates example tickets.

#### What It Does

1. Creates single ticket example
2. Generates full epic set (9 tickets)
3. Shows custom fields example
4. Demonstrates search/filter ticket
5. Exports all to JSON

#### Output

```
======================================================================
JIRA TICKET AUTOMATION - DEMO SUITE
======================================================================

This demo shows how to generate tickets for a new 'Medication Log' feature

[Runs 4 demos]

✅ Exported 12 tickets to:
   /mnt/user-data/outputs/medication-log-tickets.json

📊 Summary:
   - Backend Architecture: 1 ticket
   - RBAC Permissions: 1 ticket
   - Navigation Menu: 1 ticket
   - Tab View/Filter tickets: 6 tickets
   - Custom tickets: 3 tickets
   Total: 12 tickets
```

---

## 📋 Common Workflows

### Workflow 1: Process New Meeting Transcript

```bash
# Complete automation
python3 scripts/workflow.py transcripts/new-meeting.txt

# Review generated files
cat transcripts/new-meeting_review.txt
cat transcripts/new-meeting_tickets.json

# Test before pushing
python3 scripts/push_to_jira.py transcripts/new-meeting_tickets.json --dry-run

# Push to JIRA
python3 scripts/push_to_jira.py transcripts/new-meeting_tickets.json --epic-key VDB-1234
```

### Workflow 2: Manual Ticket Creation

```bash
# Use interactive creator
python3 scripts/create_tickets.py

# Follow prompts to:
# 1. Create tickets
# 2. Add to batch
# 3. Export when done

# Push batch
python3 scripts/push_to_jira.py tickets_batch.json --dry-run
python3 scripts/push_to_jira.py tickets_batch.json
```

### Workflow 3: Extract and Edit Before Generating

```bash
# Step 1: Extract only
python3 scripts/process_transcript.py transcripts/meeting.txt --review

# Step 2: Review
cat transcripts/meeting_review.txt

# Step 3: Edit extracted data
nano transcripts/meeting_structured.json

# Step 4: Generate tickets from edited data
# (Use ticket generator in Python - see advanced section)

# Step 5: Push
python3 scripts/push_to_jira.py final_tickets.json
```

### Workflow 4: Quick Epic Setup

```bash
# Interactive epic creator
python3 scripts/create_tickets.py

# Select option 2: Create epic ticket set
# Enter epic name: Patient Portal
# Enter tabs: Dashboard, Messages, Settings
# Export when done

# Push to JIRA
python3 scripts/push_to_jira.py patient-portal-tickets.json --dry-run
python3 scripts/push_to_jira.py patient-portal-tickets.json
```

### Workflow 5: Test and Iterate

```bash
# Run demo first
python3 demo.py

# Review demo output
cat /mnt/user-data/outputs/medication-log-tickets.json

# Test with your transcript
cp your-notes.txt transcripts/
python3 scripts/workflow.py transcripts/your-notes.txt

# Compare outputs
diff medication-log-tickets.json transcripts/your-notes_tickets.json
```

---

## 🎯 Advanced Usage

### Using Python API Directly

Instead of CLI, you can use the Python API:

#### Example: Custom Ticket Generation

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'utils')
from ticket_generator import TicketGenerator

# Initialize
generator = TicketGenerator()

# Generate specific ticket
summary = generator.generate_summary(
    ticket_type="add_entity",
    feature_name="Patient Portal",
    entity_name="appointment"
)

description = generator.generate_description(
    ticket_type="add_entity",
    entity_name="appointment",
    fields=[
        {"name": "Patient", "type": "Dropdown", "mandatory": True},
        {"name": "Date", "type": "Date picker", "mandatory": True},
        {"name": "Notes", "type": "Large text", "mandatory": False}
    ]
)

print(f"Summary: {summary}")
print(f"\nDescription:\n{description}")
```

#### Example: Custom Extraction

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'scripts')
from process_transcript import TranscriptProcessor

# Initialize
processor = TranscriptProcessor()

# Read transcript
with open('transcripts/meeting.txt', 'r') as f:
    text = f.read()

# Process with custom metadata
metadata = {
    "date": "2026-02-15",
    "attendees": ["Alice", "Bob", "Charlie"],
    "duration": "90 minutes"
}

structure = processor.process_transcript(text, metadata=metadata)

# Access extracted data
for epic in structure['epics']:
    print(f"Epic: {epic['epic_name']}")
    print(f"Tickets: {len(epic['tickets'])}")
```

#### Example: Custom Workflow

```python
#!/usr/bin/env python3
import sys
sys.path.insert(0, 'utils')
sys.path.insert(0, 'scripts')

from ticket_generator import TicketGenerator
from process_transcript import TranscriptProcessor
import json

# Custom pipeline
def my_custom_workflow(transcript_path):
    # Step 1: Extract
    processor = TranscriptProcessor()
    with open(transcript_path, 'r') as f:
        text = f.read()
    
    structure = processor.process_transcript(text)
    
    # Step 2: Custom processing
    for epic in structure['epics']:
        # Add custom logic here
        print(f"Processing: {epic['epic_name']}")
    
    # Step 3: Generate tickets
    generator = TicketGenerator()
    all_tickets = []
    
    for epic in structure['epics']:
        for ticket_spec in epic['tickets']:
            ticket = {
                "summary": ticket_spec['summary'],
                "description": generator.generate_description(
                    ticket_spec['ticket_type'],
                    feature_name=epic['epic_name']
                ),
                "priority": ticket_spec.get('priority', 'Medium')
            }
            all_tickets.append(ticket)
    
    # Step 4: Save
    with open('my_tickets.json', 'w') as f:
        json.dump({"tickets": all_tickets}, f, indent=2)
    
    print(f"Generated {len(all_tickets)} tickets")

# Run it
my_custom_workflow('transcripts/meeting.txt')
```

### Batch Processing Multiple Transcripts

```bash
#!/bin/bash
# process_all_transcripts.sh

for transcript in transcripts/*.txt; do
    echo "Processing: $transcript"
    python3 scripts/workflow.py "$transcript" --non-interactive
done

echo "All transcripts processed!"
```

### Custom Output Directory

```bash
# Process with custom output location
python3 scripts/process_transcript.py transcripts/meeting.txt \
  --output custom-output/meeting.json

# Generate tickets to specific location
python3 << EOF
import sys, json
sys.path.insert(0, 'utils')
from ticket_generator import TicketGenerator

generator = TicketGenerator()
tickets = generator.generate_epic_tickets("My Feature", tabs=["Tab1", "Tab2"])

with open('custom-output/my-tickets.json', 'w') as f:
    json.dump({"tickets": tickets}, f, indent=2)
EOF
```

### Filtering and Modifying Tickets

```bash
# Extract tickets, filter, then push
python3 << EOF
import json

# Load
with open('transcripts/meeting_tickets.json', 'r') as f:
    data = json.load(f)

# Filter - only High priority
filtered = [t for t in data['tickets'] if t['priority'] == 'High']

# Save filtered
with open('high-priority-only.json', 'w') as f:
    json.dump({"tickets": filtered}, f, indent=2)

print(f"Filtered: {len(data['tickets'])} -> {len(filtered)} tickets")
EOF

# Push filtered tickets
python3 scripts/push_to_jira.py high-priority-only.json
```

---

## 🐛 Troubleshooting

### Issue: Command Not Found

```bash
# Error
bash: python3: command not found

# Solution
which python3
# If not found, try:
python --version
# Or install Python 3
```

### Issue: Module Not Found

```bash
# Error
ModuleNotFoundError: No module named 'ticket_generator'

# Solution 1: Check you're in the right directory
cd /mnt/user-data/outputs/jira-automation

# Solution 2: Check file exists
ls -la utils/ticket_generator.py

# Solution 3: Use absolute path
python3 /full/path/to/scripts/workflow.py transcript.txt
```

### Issue: Permission Denied

```bash
# Error
Permission denied: './workflow.py'

# Solution: Make executable
chmod +x scripts/*.py

# Or run with python3
python3 scripts/workflow.py transcript.txt
```

### Issue: Invalid Transcript Format

```bash
# Error: Could not extract requirements

# Solution: Check transcript format
cat transcripts/meeting.txt | head -20

# Ensure it contains:
# - Clear feature names
# - User stories or requirements
# - Some structure (speaker names help)
```

### Issue: No Tickets Generated

```bash
# Check structured output
cat transcripts/meeting_structured.json | jq '.epics[].tickets | length'

# If 0 or null:
# 1. Transcript too vague
# 2. No clear requirements
# 3. Check extraction rules

# Try with example first
python3 scripts/workflow.py transcripts/medication-log-meeting.txt
```

### Issue: Dry Run Fails

```bash
# Error during dry-run

# Check JSON syntax
python3 -m json.tool transcripts/meeting_tickets.json

# If invalid JSON:
# 1. Re-run workflow
# 2. Or manually fix JSON
```

### Issue: Review Checkpoint Hangs

```bash
# Workflow paused at review?

# Type one of:
yes    # Continue
no     # Cancel
edit   # Edit structured JSON

# If it doesn't respond:
# Ctrl+C to cancel
# Re-run with --non-interactive
python3 scripts/workflow.py transcript.txt --non-interactive
```

---

## 📖 Examples Library

### Example 1: Simple Feature

```bash
# Transcript: "We need a Patient Search feature. Users should be able to search 
# by name and view results in a table."

# Run workflow
python3 scripts/workflow.py transcripts/patient-search.txt

# Output: ~5 tickets
# - Backend architecture
# - RBAC permissions
# - View table
# - Search/filter
# - Navigation menu
```

### Example 2: Multi-Tab Feature

```bash
# Transcript: "Build Medication Log with Active, Discontinued, and History tabs."

# Run workflow
python3 scripts/workflow.py transcripts/medication-log.txt

# Output: ~15 tickets
# - 1 backend
# - 1 RBAC
# - 1 nav menu
# - 3 x (view + search) = 6 tickets per tab
# - Add functionality
# - Actions
```

### Example 3: Form-Heavy Feature

```bash
# Transcript: "Add Appointment form with Patient, Date, Time, Provider, Notes"

# Interactive mode
python3 scripts/create_tickets.py
# Select: Add Entity
# Fill in fields as prompted

# Or quick Python
python3 << 'EOF'
import sys
sys.path.insert(0, 'utils')
from ticket_generator import TicketGenerator

g = TicketGenerator()
desc = g.generate_description(
    "add_entity",
    entity_name="appointment",
    fields=[
        {"name": "Patient", "type": "Dropdown", "mandatory": True},
        {"name": "Date", "type": "Date picker", "mandatory": True},
        {"name": "Time", "type": "Time picker", "mandatory": True},
        {"name": "Provider", "type": "Dropdown", "mandatory": True},
        {"name": "Notes", "type": "Large text", "mandatory": False}
    ]
)
print(desc)
EOF
```

### Example 4: RBAC-Heavy Feature

```bash
# Transcript includes: "Nurses can view, Doctors can edit, Admins full access"

# Process will auto-extract RBAC
python3 scripts/workflow.py transcripts/rbac-feature.txt

# Review RBAC section
cat transcripts/rbac-feature_structured.json | \
  python3 -m json.tool | grep -A 10 '"rbac"'
```

### Example 5: Quick Backend Ticket

```bash
# Just need backend architecture ticket?

python3 << 'EOF'
import sys
sys.path.insert(0, 'utils')
from ticket_generator import TicketGenerator

g = TicketGenerator()
summary = g.generate_summary("backend_architecture", "Lab Results")
desc = g.generate_description("backend_architecture", feature_name="Lab Results")

print(f"Summary: {summary}\n")
print(f"Description:\n{desc}")
EOF
```

---

## 📊 Command Cheat Sheet

### Quick Commands

```bash
# See all available commands
ls scripts/*.py

# Get help for any script
python3 scripts/workflow.py --help
python3 scripts/process_transcript.py --help
python3 scripts/push_to_jira.py --help

# Check what files will be generated
ls transcripts/

# View script source (understand what it does)
cat scripts/workflow.py | head -50

# Test JSON validity
python3 -m json.tool transcripts/meeting_tickets.json > /dev/null

# Count tickets in batch
cat transcripts/meeting_tickets.json | \
  python3 -c "import sys, json; print(len(json.load(sys.stdin)['tickets']))"
```

### File Operations

```bash
# List all transcripts
ls -lh transcripts/*.txt

# Find all generated ticket batches
find transcripts -name "*_tickets.json"

# Clean up old outputs
rm transcripts/*_structured.json
rm transcripts/*_review.txt
rm transcripts/*_tickets.json

# Backup transcripts
tar -czf transcripts-backup-$(date +%Y%m%d).tar.gz transcripts/

# Copy example to start new
cp transcripts/medication-log-meeting.txt transcripts/my-new-feature.txt
```

---

## 🎓 Learning Path

### 1. Beginner: Start with Demo

```bash
python3 demo.py
cat /mnt/user-data/outputs/medication-log-tickets.json
```

### 2. Beginner: Try Example Transcript

```bash
python3 scripts/workflow.py transcripts/medication-log-meeting.txt
# Review all output files
```

### 3. Intermediate: Process Your Own

```bash
# Create transcript
nano transcripts/my-feature.txt

# Process it
python3 scripts/workflow.py transcripts/my-feature.txt
```

### 4. Intermediate: Interactive Creation

```bash
python3 scripts/create_tickets.py
# Explore all options
```

### 5. Advanced: Modify Extraction

```bash
# Edit extraction rules
nano extraction-rules/EXTRACTION-RULES.md

# Edit processor
nano scripts/process_transcript.py
```

### 6. Advanced: Custom Workflows

```bash
# Write custom scripts using the Python API
# See "Advanced Usage" section above
```

---

## 📝 Tips & Tricks

### Tip 1: Always Dry Run First

```bash
# ALWAYS test before creating tickets
python3 scripts/push_to_jira.py tickets.json --dry-run
```

### Tip 2: Use Tab Completion

```bash
# Enable tab completion
python3 scripts/wor<TAB>      # Completes to workflow.py
python3 scripts/workflow.py transcripts/med<TAB>  # Completes filename
```

### Tip 3: Chain Commands

```bash
# Process and immediately review
python3 scripts/workflow.py transcripts/meeting.txt && \
  cat transcripts/meeting_review.txt
```

### Tip 4: Redirect Output

```bash
# Save workflow output to log
python3 scripts/workflow.py transcripts/meeting.txt 2>&1 | \
  tee workflow.log
```

### Tip 5: Quick Validation

```bash
# Check if transcript will process
python3 scripts/process_transcript.py transcripts/test.txt --review && \
  echo "✅ Success" || echo "❌ Failed"
```

---

## 🎯 Command Decision Tree

```
What do you want to do?

├─ Process a meeting transcript?
│  └─ python3 scripts/workflow.py transcripts/meeting.txt
│
├─ Create tickets manually?
│  └─ python3 scripts/create_tickets.py
│
├─ See examples?
│  └─ python3 demo.py
│
├─ Test extraction only?
│  └─ python3 scripts/process_transcript.py transcript.txt --review
│
└─ Push tickets to JIRA?
   ├─ Test first: python3 scripts/push_to_jira.py tickets.json --dry-run
   └─ Actually push: python3 scripts/push_to_jira.py tickets.json
```

---

**For more details, see:**
- `PROJECT-INSTRUCTIONS.md` - Complete documentation
- `QUICKSTART.md` - 5-minute guide
- `extraction-rules/EXTRACTION-RULES.md` - Extraction rules

---

*CLI Guide Version 2.0*
*Last Updated: 2026-02-12*
