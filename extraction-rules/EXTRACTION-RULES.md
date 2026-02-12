# Meeting Transcript Extraction Rules

> **Guidelines for extracting structured requirements from meeting transcripts**
> 
> Version: 1.0 | Date: 2026-02-12

---

## 🎯 Extraction Objectives

Transform unstructured meeting transcripts into structured requirement specifications suitable for JIRA ticket generation.

---

## 📋 Required Information Categories

### 1. Feature/Epic Information
**What to Extract:**
- Epic name or feature name
- Overall purpose/goal of the feature
- Target users or personas
- Business justification

**Indicators in Transcripts:**
- "We need to build..."
- "The new feature will..."
- "This will help users to..."
- "For the [Feature Name] module..."

**Example:**
```
Transcript: "We need to build a Medication Log to track all prescribed medications for patients in the infirmary."

Extracted:
- Epic Name: "Medication Log"
- Purpose: "Track prescribed medications for patients"
- Target Users: "Clinical staff, nurses"
- Scope: "Infirmary module"
```

---

### 2. Functional Requirements (User Stories)
**What to Extract:**
- User role/actor
- Desired action
- Expected outcome
- Acceptance criteria

**Indicators in Transcripts:**
- "Users should be able to..."
- "The system needs to..."
- "We want to..."
- "It should allow..."
- "Staff need to..."

**Pattern Matching:**
```
Template: "[Actor] should be able to [Action] so that [Outcome]"

Transcript: "Nurses should be able to view all active medications in a table so they can quickly review patient prescriptions."

Extracted Story:
- Actor: Nurse
- Action: View active medications in table
- Outcome: Quick review of patient prescriptions
- Ticket Type: view_table_data
```

---

### 3. Data Fields and Specifications
**What to Extract:**
- Field names
- Field types (text, date, dropdown, etc.)
- Mandatory vs optional
- Default values
- Validation rules
- Dropdown options

**Indicators in Transcripts:**
- "We need fields for..."
- "It should capture..."
- "Required information includes..."
- "The form should have..."
- "Options are..."

**Example:**
```
Transcript: "When adding a medication, we need patient name, medication name, dosage - all required. Also frequency with options like 'Once daily', 'Twice daily', 'As needed', and optional special instructions."

Extracted Fields:
- Patient Name * (Dropdown, mandatory)
- Medication Name * (Text field, mandatory)
- Dosage * (Text field, mandatory)
- Frequency * (Dropdown, mandatory, options: Once daily, Twice daily, As needed)
- Special Instructions (Large text, optional)
```

---

### 4. UI/UX Requirements
**What to Extract:**
- Screen layouts (tabs, sections)
- Table columns
- Action buttons
- Navigation structure
- Modals/drawers

**Indicators in Transcripts:**
- "The screen will have..."
- "Split into tabs..."
- "Show columns for..."
- "Actions include..."
- "Modal should display..."

**Example:**
```
Transcript: "The Medication Log will have three tabs: Active, Discontinued, and History. Each tab shows a table with patient name, medication, dosage, and actions."

Extracted:
Tabs: ["Active", "Discontinued", "History"]
Table Columns: ["Patient Name", "Medication", "Dosage", "Actions"]
```

---

### 5. RBAC and Permissions
**What to Extract:**
- User roles
- Permission levels (Edit, View, Hide)
- Feature access rules
- Action-level permissions

**Indicators in Transcripts:**
- "Only [role] can..."
- "[Role] should have access to..."
- "Restrict to..."
- "Permissions for..."

**Example:**
```
Transcript: "Nurses can view and add medications, but only doctors can discontinue them. Administrators have full access."

Extracted RBAC:
- Nurse: View (Active, History), Edit (Add new)
- Doctor: View (All), Edit (All), Delete (Discontinue)
- Administrator: Full access
```

---

### 6. Business Rules and Validation
**What to Extract:**
- Validation rules
- Conditional logic
- Workflow rules
- Calculated fields

**Indicators in Transcripts:**
- "Only if..."
- "When [condition], then..."
- "Should not allow..."
- "Automatically calculate..."
- "Required when..."

**Example:**
```
Transcript: "If a patient is marked as diabetic, glucose monitoring is required. Don't allow dosages over 500mg without approval."

Extracted Rules:
- Conditional mandatory: Glucose field required if patient.isDiabetic = true
- Validation: Dosage <= 500mg OR approval = true
```

---

### 7. Technical Requirements
**What to Extract:**
- Backend components needed
- API endpoints
- Database tables
- Integration points

**Indicators in Transcripts:**
- "Need backend for..."
- "Store in database..."
- "Integrate with..."
- "Call API to..."

**Example:**
```
Transcript: "We'll need a backend to store medications with CRUD operations and integrate with the pharmacy system."

Extracted:
- Backend: Yes (Models, Service, Controller, Routes)
- Database: Medication table (CRUD)
- Integration: Pharmacy system API
```

---

### 8. Priority and Timeline
**What to Extract:**
- Priority level
- Sprint/release target
- Dependencies
- Blockers

**Indicators in Transcripts:**
- "Critical for..."
- "Need by..."
- "Priority is..."
- "Depends on..."
- "Blocker:"

**Example:**
```
Transcript: "This is critical for the Q2 release. Highest priority. We need the backend ready before frontend work starts."

Extracted:
- Priority: Highest
- Release: Q2 2026
- Dependencies: Backend must complete first
```

---

## 🔍 Extraction Process

### Step 1: Initial Reading
1. Read entire transcript
2. Identify main topics/features discussed
3. Note participants and their roles
4. Flag any decisions made

### Step 2: Feature Identification
1. Extract epic/feature names
2. Group related requirements
3. Identify scope boundaries
4. Note any out-of-scope items

### Step 3: Requirement Extraction
For each feature/epic:
1. Extract user stories
2. Identify data fields
3. Note UI/UX details
4. Capture business rules
5. Document RBAC needs

### Step 4: Ticket Mapping
Map extracted requirements to ticket types:
- Backend setup → `backend_architecture`
- Permission setup → `rbac_permissions`
- Nav item → `nav_menu`
- Table view → `view_table_data`
- Add form → `add_entity`
- Actions → `perform_actions`
- Search/Filter → `search_filter`
- Download → `download`
- Upload → `upload_csv`

### Step 5: Structured Output
Generate structured JSON with:
```json
{
  "meeting_metadata": {
    "date": "2026-02-12",
    "attendees": ["Person A", "Person B"],
    "duration": "60 minutes"
  },
  "epics": [
    {
      "name": "Feature Name",
      "description": "...",
      "priority": "High",
      "tickets": [
        {
          "type": "backend_architecture",
          "summary": "...",
          "details": {...}
        }
      ]
    }
  ]
}
```

---

## 📝 Extraction Templates

### Template 1: Simple Feature
```
Transcript Pattern:
"We need [Feature] that allows [Users] to [Action]."

Extracted Structure:
- Epic: [Feature]
- User Story: Users should be able to [Action]
- Ticket Type: [Detected from Action]
```

### Template 2: Form-Based Feature
```
Transcript Pattern:
"Users fill out a form with [Field1], [Field2], [Field3]."

Extracted Structure:
- Ticket Type: add_entity
- Fields: [
    {name: Field1, type: auto-detect, mandatory: check context},
    {name: Field2, type: auto-detect, mandatory: check context},
    {name: Field3, type: auto-detect, mandatory: check context}
  ]
```

### Template 3: Table-Based Feature
```
Transcript Pattern:
"Display a table showing [Col1], [Col2], [Col3]."

Extracted Structure:
- Ticket Type: view_table_data
- Columns: [Col1, Col2, Col3]
```

---

## 🚫 Common Pitfalls to Avoid

### 1. Over-Interpretation
❌ **Don't:** Add features not explicitly mentioned
✅ **Do:** Extract only what's stated or clearly implied

### 2. Missing Context
❌ **Don't:** Ignore important qualifiers (roles, conditions)
✅ **Do:** Capture full context for each requirement

### 3. Vague Requirements
❌ **Don't:** Accept "user-friendly" as a requirement
✅ **Do:** Flag vague statements for clarification

### 4. Technical Assumptions
❌ **Don't:** Assume implementation details not discussed
✅ **Do:** Mark assumptions clearly and flag for review

### 5. Scope Creep
❌ **Don't:** Expand beyond meeting scope
✅ **Do:** Note "out of scope" items separately

---

## ✅ Quality Checklist

Before finalizing extracted requirements:

- [ ] **Completeness:** All features mentioned are captured
- [ ] **Clarity:** Each requirement is specific and actionable
- [ ] **Consistency:** Terminology is consistent throughout
- [ ] **Traceability:** Can map back to transcript source
- [ ] **Validation:** Field rules are clearly specified
- [ ] **RBAC:** Permissions are explicitly defined
- [ ] **Priority:** Each item has priority assigned
- [ ] **Ticket Mapping:** Each requirement maps to ticket type

---

## 📊 Output Format Specification

### JSON Schema
```json
{
  "meeting_metadata": {
    "date": "YYYY-MM-DD",
    "attendees": ["string"],
    "duration": "string",
    "topics": ["string"]
  },
  "epics": [
    {
      "epic_name": "string",
      "epic_description": "string",
      "priority": "Highest|High|Medium|Low",
      "scope": "facility-specific|global",
      "tabs": ["string"],
      "tickets": [
        {
          "ticket_type": "backend_architecture|view_table_data|add_entity|...",
          "summary": "string",
          "priority": "Highest|High|Medium|Low",
          "details": {
            "fields": [...],
            "columns": [...],
            "actions": [...],
            "validation_rules": [...],
            "rbac": {...}
          }
        }
      ]
    }
  ],
  "action_items": [
    {
      "item": "string",
      "owner": "string",
      "due_date": "YYYY-MM-DD"
    }
  ],
  "clarifications_needed": [
    {
      "question": "string",
      "context": "string"
    }
  ]
}
```

---

## 🎯 Example: Complete Extraction

### Input Transcript
```
Meeting: Medication Log Feature Discussion
Date: 2026-02-10
Attendees: Product Manager, Tech Lead, Clinical Director

PM: "We need to build a Medication Log feature to track prescribed medications. It should have three tabs: Active, Discontinued, and History."

Clinical Director: "Nurses need to add new medications with patient name, medication name, dosage, frequency - all mandatory. Also optional special instructions."

Tech Lead: "We'll need backend architecture first - database models, API endpoints. Also need RBAC - nurses can add and view, doctors can discontinue, admins have full access."

PM: "This is highest priority for Q2 release. Users should also be able to search by patient name and filter by date prescribed."
```

### Extracted Structure
```json
{
  "meeting_metadata": {
    "date": "2026-02-10",
    "attendees": ["Product Manager", "Tech Lead", "Clinical Director"],
    "topics": ["Medication Log feature requirements"]
  },
  "epics": [
    {
      "epic_name": "Medication Log",
      "epic_description": "Track prescribed medications for patients",
      "priority": "Highest",
      "scope": "facility-specific",
      "tabs": ["Active", "Discontinued", "History"],
      "tickets": [
        {
          "ticket_type": "backend_architecture",
          "summary": "BE: Implement backend architecture of \"Medication Log\"",
          "priority": "Highest"
        },
        {
          "ticket_type": "rbac_permissions",
          "summary": "Adding RBAC permissions related to \"Medication Log\"",
          "priority": "High",
          "details": {
            "rbac": {
              "Nurse": {"permissions": ["View", "Add"], "actions": ["View tables", "Add new medication"]},
              "Doctor": {"permissions": ["View", "Edit", "Discontinue"], "actions": ["All nurse actions", "Discontinue medications"]},
              "Administrator": {"permissions": ["Full access"], "actions": ["All actions"]}
            }
          }
        },
        {
          "ticket_type": "view_table_data",
          "summary": "User should be able to access and view data in the table of 'Active' tab",
          "priority": "High",
          "details": {
            "tab_name": "Active",
            "columns": ["Patient Name", "Medication Name", "Dosage", "Frequency", "Prescribed Date", "Status", "Actions"]
          }
        },
        {
          "ticket_type": "add_entity",
          "summary": "User should be able to add a medication",
          "priority": "High",
          "details": {
            "entity_name": "medication",
            "fields": [
              {"name": "Patient Name", "type": "Dropdown", "mandatory": true},
              {"name": "Medication Name", "type": "Text field", "mandatory": true},
              {"name": "Dosage", "type": "Text field", "mandatory": true},
              {"name": "Frequency", "type": "Dropdown", "mandatory": true},
              {"name": "Special Instructions", "type": "Large text", "mandatory": false}
            ]
          }
        },
        {
          "ticket_type": "search_filter",
          "summary": "User should be able to search and filter data in 'Active' tab",
          "priority": "High",
          "details": {
            "search_fields": ["Patient Name"],
            "filters": [
              {"name": "Prescribed Date (From/To)", "type": "Date range", "default": "Empty"}
            ]
          }
        }
      ]
    }
  ],
  "clarifications_needed": [
    {
      "question": "What columns should appear in Discontinued and History tabs?",
      "context": "Only Active tab columns were specified"
    },
    {
      "question": "What are the options for Frequency dropdown?",
      "context": "Field marked as dropdown but options not specified"
    }
  ]
}
```

---

## 🔄 Iterative Refinement

After initial extraction:
1. **Review** with stakeholders
2. **Clarify** ambiguous requirements
3. **Refine** technical details
4. **Validate** against standards
5. **Approve** before ticket generation

---

## 📚 Reference Materials

- **VDB Standards:** `/mnt/project/VDB-JIRA-Ticket-Standards.md`
- **Historical Tickets:** `/mnt/user-data/outputs/historical-tickets-data.json`
- **Ticket Generator:** `utils/ticket_generator.py`

---

*This document should be used in conjunction with the automated extraction tool.*
*Last updated: 2026-02-12*
