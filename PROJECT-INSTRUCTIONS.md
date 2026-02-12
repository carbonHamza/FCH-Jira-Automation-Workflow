# JIRA Ticket Automation Project - Complete Instructions

> **Automated JIRA ticket generation from meeting transcripts to production tickets**
> 
> Project: FCH Dev (VDB) | Version: 2.0 | Date: 2026-02-12

---

## 🎯 Project Overview

This automation system transforms unstructured meeting transcripts into production-ready JIRA tickets following VDB project standards. The complete pipeline includes:

1. **Transcript Processing** - Extract structured requirements from meeting notes
2. **User Review** - Validate extracted requirements before ticket generation
3. **Ticket Generation** - Create properly formatted JIRA tickets
4. **JIRA Integration** - Push tickets directly to JIRA via API

---

## 📁 Project Structure

```
jira-automation/
├── transcripts/                    # Meeting transcript files
│   ├── medication-log-meeting.txt  # Example transcript
│   └── [your-transcripts].txt      # Add your transcripts here
│
├── extraction-rules/               # Rules for requirement extraction
│   └── EXTRACTION-RULES.md         # Complete extraction guidelines
│
├── structured-output/              # Generated structured data
│   ├── [transcript]_structured.json  # Extracted requirements
│   ├── [transcript]_review.txt       # Human-readable review
│   └── [transcript]_tickets.json     # Final ticket batch
│
├── scripts/                        # Automation scripts
│   ├── workflow.py                 # End-to-end orchestrator
│   ├── process_transcript.py       # Transcript processor
│   ├── create_tickets.py           # Interactive ticket creator
│   └── push_to_jira.py             # JIRA API integration
│
├── utils/                          # Core libraries
│   └── ticket_generator.py         # Ticket generation engine
│
├── README.md                       # Complete documentation
├── QUICKSTART.md                   # 5-minute getting started
└── EXTRACTION-RULES.md             # Moved to extraction-rules/
```

---

## 🚀 Complete Workflow

### End-to-End Process

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Meeting Happens                                           │
│    - Requirements discussed                                  │
│    - Transcript generated (manual or automated)              │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 2. Place Transcript                                          │
│    - Save to: transcripts/[meeting-name].txt                 │
│    - Can be structured or unstructured text                  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 3. Run Extraction (Automated)                                │
│    python3 scripts/workflow.py transcripts/[name].txt        │
│                                                              │
│    AI analyzes transcript and extracts:                      │
│    - Epic/feature names                                      │
│    - User stories                                            │
│    - Data fields & specifications                            │
│    - UI/UX requirements                                      │
│    - RBAC rules                                              │
│    - Business logic                                          │
│    - Priority levels                                         │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 4. Generate Structured Output                                │
│    Creates 3 files:                                          │
│    - [name]_structured.json  (Machine-readable data)         │
│    - [name]_review.txt       (Human-readable summary)        │
│    - [name]_tickets.json     (JIRA-ready tickets)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 5. USER REVIEW (Interactive Checkpoint)                      │
│    Workflow pauses and shows:                                │
│    - Extracted epics & features                              │
│    - Number of tickets to be created                         │
│    - Identified clarifications needed                        │
│                                                              │
│    User can:                                                 │
│    ✓ Approve and continue                                    │
│    ✗ Cancel and revise transcript                            │
│    ✏️  Edit structured.json and re-run                        │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 6. Generate JIRA Tickets (Automated)                         │
│    For each epic:                                            │
│    - Backend architecture ticket                             │
│    - RBAC permissions ticket                                 │
│    - Navigation menu ticket                                  │
│    - Tab-specific tickets (view + search/filter)             │
│    - Custom feature tickets                                  │
│                                                              │
│    All tickets follow VDB standards:                         │
│    ✓ Proper naming conventions                               │
│    ✓ Acceptance criteria formatting                          │
│    ✓ Field specifications                                    │
│    ✓ Priority assignment                                     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 7. Review Generated Tickets                                  │
│    cat transcripts/[name]_tickets.json                       │
│                                                              │
│    Review:                                                   │
│    - Ticket summaries                                        │
│    - Descriptions                                            │
│    - Priorities                                              │
│    - Field specifications                                    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 8. Dry Run (Test)                                            │
│    python3 scripts/push_to_jira.py \                         │
│      transcripts/[name]_tickets.json --dry-run               │
│                                                              │
│    Preview what will be created without actually creating    │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│ 9. Push to JIRA                                              │
│    python3 scripts/push_to_jira.py \                         │
│      transcripts/[name]_tickets.json --epic-key VDB-XXXX     │
│                                                              │
│    Tickets created in JIRA!                                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Extraction Rules

The system follows comprehensive extraction rules documented in:
`extraction-rules/EXTRACTION-RULES.md`

### Key Extraction Categories

1. **Feature/Epic Information**
   - Epic name & description
   - Purpose & target users
   - Business justification

2. **Functional Requirements**
   - User roles/actors
   - Desired actions
   - Expected outcomes
   - Acceptance criteria

3. **Data Fields**
   - Field names & types
   - Mandatory vs optional
   - Default values & validation
   - Dropdown options

4. **UI/UX Requirements**
   - Screen layouts & tabs
   - Table columns
   - Action buttons
   - Modals & navigation

5. **RBAC & Permissions**
   - User roles
   - Permission levels (Edit/View/Hide)
   - Action-level restrictions

6. **Business Rules**
   - Validation logic
   - Conditional requirements
   - Workflow rules
   - Calculated fields

7. **Technical Requirements**
   - Backend components
   - Database tables
   - API integrations

8. **Priority & Timeline**
   - Priority levels
   - Sprint targets
   - Dependencies

### Extraction Process

The AI follows this process:

```python
1. Read entire transcript
2. Identify main topics/features
3. Extract epic/feature names
4. Group related requirements
5. Map to ticket types:
   - Backend → backend_architecture
   - Permissions → rbac_permissions
   - Navigation → nav_menu
   - Table view → view_table_data
   - Add form → add_entity
   - Actions → perform_actions
   - Search/Filter → search_filter
   - Download → download
   - Upload → upload_csv
6. Generate structured JSON
7. Create review report
8. Flag clarifications needed
```

---

## 🎯 Usage Instructions

### Method 1: Complete Automated Workflow (Recommended)

```bash
cd /mnt/user-data/outputs/jira-automation

# Run complete pipeline with user review
python3 scripts/workflow.py transcripts/your-meeting.txt

# Non-interactive (no review pauses)
python3 scripts/workflow.py transcripts/your-meeting.txt --non-interactive

# Step-by-step (pause after each step)
python3 scripts/workflow.py transcripts/your-meeting.txt --step-by-step
```

**What happens:**
1. Transcript processed automatically
2. Structured requirements extracted
3. Review report generated
4. **Workflow pauses for your approval**
5. Tickets generated after approval
6. Batch file created
7. Ready for JIRA push

### Method 2: Manual Step-by-Step

```bash
# Step 1: Process transcript
python3 scripts/process_transcript.py \
  transcripts/meeting.txt \
  --output transcripts/meeting_structured.json \
  --review

# Step 2: Review output
cat transcripts/meeting_review.txt

# Step 3: Edit if needed
nano transcripts/meeting_structured.json

# Step 4: Generate tickets (if you need manual control)
# Use the ticket_generator.py directly or via create_tickets.py

# Step 5: Push to JIRA
python3 scripts/push_to_jira.py \
  transcripts/meeting_tickets.json \
  --epic-key VDB-1234
```

### Method 3: Interactive Ticket Creation

```bash
# If you prefer manual ticket creation
python3 scripts/create_tickets.py
```

---

## 📝 Transcript Format Guidelines

### Recommended Format

```
Meeting: [Feature Name] Discussion
Date: YYYY-MM-DD
Attendees: [Name (Role), Name (Role)]
Duration: [X] minutes

==================== TRANSCRIPT ====================

[Speaker Name]: "Actual spoken content..."

[Speaker Name]: "More content..."

==================== END TRANSCRIPT ====================

Key Decisions Made:
- Decision 1
- Decision 2

Out of Scope:
- Item 1
- Item 2
```

### Extraction Works Best When Transcript Includes:

✅ **Clear speaker attribution** - "Sarah (PM): ..."
✅ **Explicit requirements** - "We need...", "Users should be able to..."
✅ **Field specifications** - "Required fields: X, Y, Z"
✅ **Priority indicators** - "This is highest priority"
✅ **Technical details** - "Backend needs...", "RBAC: Nurses can..."
✅ **UI/UX descriptions** - "Three tabs:", "Table with columns:"

### Types of Transcripts Supported

1. **Structured transcripts** (with speaker names, sections)
2. **Unstructured notes** (raw meeting notes)
3. **Requirements documents** (formal specifications)
4. **Email chains** (requirement discussions)

---

## 🔍 User Review Checkpoint

### What You'll See During Review

```
======================================================================
EXTRACTED REQUIREMENTS - REVIEW REPORT
======================================================================

📅 Meeting Date: 2026-02-10
👥 Attendees: Product Manager, Tech Lead, Clinical Director

📦 Epics Found: 1

1. Medication Log
   Priority: Highest
   Tickets: 15
   Tabs: Active, Discontinued, History

📋 Action Items: 5
   - Tech Lead: Create backend architecture ticket
   - Product: Create detailed wireframes
   - QA: Prepare test scenarios

❓ Clarifications Needed: 2
   - What columns should appear in Discontinued tab?
   - What are the options for Frequency dropdown?

======================================================================
```

### Review Checklist

Before approving, verify:

- [ ] **Epic names** are correct
- [ ] **Number of tickets** seems reasonable
- [ ] **Priority levels** are appropriate
- [ ] **Tabs/sections** match discussion
- [ ] **No critical requirements missed**
- [ ] **Clarifications** are noted

### How to Handle Clarifications

If clarifications are needed:

1. **Option A:** Edit the structured JSON
   ```bash
   nano transcripts/meeting_structured.json
   # Add missing details
   # Re-run workflow
   ```

2. **Option B:** Cancel and update transcript
   ```bash
   # Add missing info to transcript
   nano transcripts/meeting.txt
   # Re-run workflow
   python3 scripts/workflow.py transcripts/meeting.txt
   ```

3. **Option C:** Proceed and fix tickets later
   ```bash
   # Generate tickets
   # Edit the tickets JSON before pushing
   nano transcripts/meeting_tickets.json
   ```

---

## 🎫 Generated Ticket Structure

### Example Output

```json
{
  "project": "VDB",
  "source_transcript": "transcripts/medication-log-meeting.txt",
  "total_tickets": 15,
  "tickets": [
    {
      "type": "Story",
      "summary": "BE: Implement backend architecture of \"Medication Log\"",
      "description": "**Acceptance criteria:**\n\nCreate following:\n\n* Model for database\n* Service\n* Entity\n* Controller\n* Routes",
      "priority": "High"
    },
    {
      "type": "Story",
      "summary": "User should be able to access and view data in the table of 'Active' tab",
      "description": "...",
      "priority": "High"
    }
  ],
  "metadata": {
    "meeting_attendees": ["PM", "Tech Lead", "Clinical Director"],
    "clarifications_needed": [...]
  }
}
```

---

## 🔧 Advanced Configuration

### Customizing Extraction Rules

Edit `extraction-rules/EXTRACTION-RULES.md` to modify:
- Extraction patterns
- Ticket type mappings
- Field type detection
- Priority assignment logic

### Customizing Ticket Templates

Edit `utils/ticket_generator.py`:
- Modify `_template_*` methods
- Update field specifications
- Change description formatting
- Adjust priority suggestions

### Adding New Ticket Types

1. Add template method to `ticket_generator.py`
2. Update `detect_ticket_type()` pattern matching
3. Add to `generate_description()` routing
4. Test with sample transcript

---

## 📊 Quality Assurance

### Automated Checks

The system automatically:
- ✅ Validates field specifications
- ✅ Checks for incomplete requirements
- ✅ Identifies ambiguous requirements
- ✅ Flags missing RBAC details
- ✅ Detects placeholder values
- ✅ Ensures VDB standards compliance

### Manual Review Points

Before pushing to JIRA:

1. **Ticket Summaries** - Follow VDB patterns?
2. **Descriptions** - Include acceptance criteria?
3. **Field Specs** - All fields have types?
4. **Priorities** - Correctly assigned?
5. **Facility Scope** - Specified everywhere?
6. **Mobile Notes** - Included for tables?

---

## 🚨 Troubleshooting

### Common Issues

**Issue:** Extraction missed a requirement
**Solution:** 
- Add more explicit language to transcript
- Manually edit structured JSON
- Use extraction keywords (see EXTRACTION-RULES.md)

**Issue:** Too many/few tickets generated
**Solution:**
- Review structured JSON
- Adjust epic boundary in transcript
- Manually filter tickets before push

**Issue:** Field types incorrect
**Solution:**
- Edit `_guess_field_type()` in process_transcript.py
- Manually specify in structured JSON

**Issue:** Priority seems wrong
**Solution:**
- Add priority keywords to transcript
- Edit ticket priority in batch JSON
- Adjust `_extract_priority()` logic

---

## 📚 Reference Materials

### Core Documentation
- `README.md` - Complete system documentation
- `QUICKSTART.md` - 5-minute getting started
- `extraction-rules/EXTRACTION-RULES.md` - Extraction guidelines
- `/mnt/project/VDB-JIRA-Ticket-Standards.md` - VDB standards

### Data Sources
- `historical-tickets-data.json` - 75 analyzed tickets
- `transcripts/medication-log-meeting.txt` - Example transcript
- `demo.py` - Code examples

### Key Scripts
- `scripts/workflow.py` - Complete automation
- `scripts/process_transcript.py` - Transcript processor
- `scripts/create_tickets.py` - Interactive creator
- `scripts/push_to_jira.py` - JIRA integration
- `utils/ticket_generator.py` - Core engine

---

## 🎯 Best Practices

### For Transcripts

1. **Be explicit** - "Users should be able to..." not "Maybe we could..."
2. **Name things clearly** - Use exact feature/tab/field names
3. **Specify types** - "Dropdown with options: A, B, C"
4. **Include RBAC** - "Nurses can..., Doctors can..."
5. **State priority** - "This is highest priority"
6. **Document decisions** - Add "Key Decisions" section

### For Review

1. **Read carefully** - Don't rush the review step
2. **Check completeness** - All features covered?
3. **Validate tickets** - Do summaries make sense?
4. **Note clarifications** - Address before finalizing
5. **Test first** - Always dry-run before production push

### For Workflow

1. **Start simple** - Test with one transcript first
2. **Use interactive mode** - Until familiar with output
3. **Keep transcripts** - Version control your transcripts
4. **Document changes** - Track manual edits
5. **Iterate** - Refine extraction rules over time

---

## 🔮 Future Enhancements

Planned features:
- [ ] Real-time transcript processing (during meetings)
- [ ] Integration with Figma for UI specs
- [ ] Automatic epic decomposition suggestions
- [ ] Dependency detection and linking
- [ ] Conflict detection with existing tickets
- [ ] AI-powered clarification generation
- [ ] Batch editing UI
- [ ] Template library expansion

---

## 📞 Support

### Getting Help

1. Check `QUICKSTART.md` for common scenarios
2. Review `extraction-rules/EXTRACTION-RULES.md` for extraction issues
3. Examine example transcript: `transcripts/medication-log-meeting.txt`
4. Test with demo: `python3 demo.py`

### Reporting Issues

When something doesn't work:
1. Share the transcript (sanitized if needed)
2. Include the structured JSON output
3. Note the specific issue (missed requirement, wrong type, etc.)
4. Provide expected vs actual output

---

## ✅ Success Criteria

You're successfully using the system if:

- ✅ Transcripts process without errors
- ✅ Structured output captures all requirements
- ✅ Review reports are clear and accurate
- ✅ Generated tickets follow VDB standards
- ✅ Ticket descriptions are complete
- ✅ Priorities are correctly assigned
- ✅ Clarifications are properly identified
- ✅ Tickets push to JIRA successfully

---

*Project maintained for VDB/FCH Dev*
*Last updated: 2026-02-12*
*Based on 75 historical tickets + 1 sample transcript*
