#!/usr/bin/env python3
"""
Meeting Transcript Processor
Extracts structured requirements from unstructured meeting transcripts
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class TranscriptProcessor:
    """Process meeting transcripts and extract requirements"""
    
    def __init__(self):
        self.extraction_patterns = self._load_extraction_patterns()
    
    def _load_extraction_patterns(self) -> dict:
        """Load regex patterns for requirement extraction"""
        return {
            # Feature/Epic patterns
            "epic_name": [
                r"(?:build|create|implement|develop)\s+(?:a\s+|an\s+|the\s+)?([A-Z][A-Za-z\s]+?)(?:\s+feature|\s+module|\s+system)",
                r"(?:for\s+the\s+)([A-Z][A-Za-z\s]+?)(?:\s+feature|\s+module)"
            ],
            
            # User story patterns
            "user_story": [
                r"(users?|nurses?|doctors?|admins?|staff)\s+(?:should\s+be\s+able\s+to|need\s+to|must|can)\s+([^.]+)",
                r"(?:the\s+system|it)\s+(?:should|must|needs?\s+to)\s+(?:allow|enable|let)\s+(?:users?|nurses?|doctors?)\s+to\s+([^.]+)"
            ],
            
            # Field specifications
            "field_spec": [
                r"(?:fields?\s+(?:for|include)|need|require|capture)\s+([^.]+?)\s*[-–—]\s*(all\s+)?(?:required|mandatory|optional)",
                r"with\s+fields?\s+(?:for\s+)?([^.]+)"
            ],
            
            # Table/UI patterns
            "table_columns": [
                r"(?:table|columns?)\s+(?:showing|with|for|displaying)\s+([^.]+)",
                r"(?:show|display)\s+(?:columns?\s+for\s+)?([^.]+)\s+in\s+(?:the\s+)?table"
            ],
            
            # Tab patterns
            "tabs": [
                r"(?:tabs?|sections?)\s*:\s*([^.]+)",
                r"(?:split|divided)\s+into\s+(?:\d+\s+)?tabs?\s*:\s*([^.]+)"
            ],
            
            # Priority indicators
            "priority": [
                r"(?:priority\s+is\s+|)(?:highest|high|medium|low|critical)",
                r"(?:critical|urgent|important)\s+for"
            ],
            
            # RBAC patterns
            "rbac": [
                r"(nurses?|doctors?|admins?|staff|users?)\s+can\s+([^.]+)",
                r"only\s+(nurses?|doctors?|admins?)\s+(?:can|should|may)\s+([^.]+)"
            ],
            
            # Validation rules
            "validation": [
                r"(?:should\s+not\s+allow|don't\s+allow|prevent|block)\s+([^.]+)",
                r"(?:required\s+when|only\s+if|mandatory\s+when)\s+([^.]+)"
            ]
        }
    
    def process_transcript(self, transcript_text: str, 
                          metadata: Dict = None) -> Dict:
        """
        Process a transcript and extract structured requirements
        
        Args:
            transcript_text: Raw meeting transcript text
            metadata: Optional metadata (date, attendees, etc.)
            
        Returns:
            Structured requirement dictionary
        """
        
        # Initialize structure
        structure = {
            "meeting_metadata": metadata or self._extract_metadata(transcript_text),
            "epics": [],
            "action_items": [],
            "clarifications_needed": []
        }
        
        # Extract epics
        epics = self._extract_epics(transcript_text)
        
        for epic_name in epics:
            epic_data = self._process_epic(transcript_text, epic_name)
            structure["epics"].append(epic_data)
        
        # Extract action items
        structure["action_items"] = self._extract_action_items(transcript_text)
        
        # Identify needed clarifications
        structure["clarifications_needed"] = self._identify_clarifications(structure)
        
        return structure
    
    def _extract_metadata(self, text: str) -> Dict:
        """Extract meeting metadata from transcript"""
        metadata = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "attendees": [],
            "duration": "Unknown",
            "topics": []
        }
        
        # Try to extract date
        date_match = re.search(r"(?:date|meeting)\s*:\s*(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4})", text, re.IGNORECASE)
        if date_match:
            metadata["date"] = date_match.group(1)
        
        # Try to extract attendees
        attendees_match = re.search(r"(?:attendees|participants)\s*:\s*([^\n]+)", text, re.IGNORECASE)
        if attendees_match:
            attendees_text = attendees_match.group(1)
            metadata["attendees"] = [a.strip() for a in re.split(r'[,;]', attendees_text) if a.strip()]
        
        return metadata
    
    def _extract_epics(self, text: str) -> List[str]:
        """Extract epic/feature names from transcript"""
        epics = []
        
        for pattern in self.extraction_patterns["epic_name"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                epic_name = match.group(1).strip()
                if epic_name and epic_name not in epics:
                    epics.append(epic_name)
        
        return epics if epics else ["Unnamed Feature"]
    
    def _process_epic(self, text: str, epic_name: str) -> Dict:
        """Process requirements for a specific epic"""
        
        epic_data = {
            "epic_name": epic_name,
            "epic_description": self._extract_epic_description(text, epic_name),
            "priority": self._extract_priority(text),
            "scope": "facility-specific",  # Default, can be overridden
            "tabs": self._extract_tabs(text),
            "tickets": []
        }
        
        # Generate tickets based on extracted information
        tickets = self._generate_tickets_from_text(text, epic_name, epic_data)
        epic_data["tickets"] = tickets
        
        return epic_data
    
    def _extract_epic_description(self, text: str, epic_name: str) -> str:
        """Extract description for an epic"""
        # Look for sentences mentioning the epic name
        sentences = re.split(r'[.!?]', text)
        
        for sentence in sentences:
            if epic_name.lower() in sentence.lower():
                # Clean and return
                description = sentence.strip()
                if len(description) > 20:
                    return description
        
        return f"Feature for {epic_name}"
    
    def _extract_priority(self, text: str) -> str:
        """Extract priority from transcript"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["highest", "critical", "urgent"]):
            return "Highest"
        elif "high priority" in text_lower or "important" in text_lower:
            return "High"
        elif "low priority" in text_lower:
            return "Low"
        else:
            return "Medium"
    
    def _extract_tabs(self, text: str) -> List[str]:
        """Extract tab names from transcript"""
        tabs = []
        
        for pattern in self.extraction_patterns["tabs"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                tabs_text = match.group(1)
                # Split on commas, 'and', etc.
                tab_names = re.split(r'[,;]|\s+and\s+', tabs_text)
                tabs.extend([t.strip() for t in tab_names if t.strip()])
        
        return tabs
    
    def _generate_tickets_from_text(self, text: str, epic_name: str, 
                                    epic_data: Dict) -> List[Dict]:
        """Generate ticket structures from text analysis"""
        tickets = []
        
        # Always add backend architecture
        tickets.append({
            "ticket_type": "backend_architecture",
            "summary": f"BE: Implement backend architecture of \"{epic_name}\"",
            "priority": "High"
        })
        
        # Check for RBAC mentions
        if self._has_rbac_requirements(text):
            tickets.append({
                "ticket_type": "rbac_permissions",
                "summary": f"Adding RBAC permissions related to \"{epic_name}\"",
                "priority": "High",
                "details": {
                    "rbac": self._extract_rbac(text)
                }
            })
        
        # Check for navigation menu
        if any(word in text.lower() for word in ["menu", "navigation", "nav bar", "sidebar"]):
            tickets.append({
                "ticket_type": "nav_menu",
                "summary": f"FE: User should be able to view a new menu \"{epic_name}\" under \"Clinical\" in nav panel",
                "priority": "High"
            })
        
        # Generate tab-specific tickets
        for tab in epic_data.get("tabs", []):
            # View table ticket
            tickets.append({
                "ticket_type": "view_table_data",
                "summary": f"User should be able to access and view data in the table of '{tab}' tab",
                "priority": "High",
                "details": {
                    "tab_name": tab,
                    "columns": self._extract_columns(text, tab)
                }
            })
            
            # Search/filter ticket
            if any(word in text.lower() for word in ["search", "filter", "find"]):
                tickets.append({
                    "ticket_type": "search_filter",
                    "summary": f"User should be able to search and filter data in '{tab}' tab",
                    "priority": "High",
                    "details": {
                        "tab_name": tab
                    }
                })
        
        # Check for add/create functionality
        if any(word in text.lower() for word in ["add", "create", "new", "form"]):
            entity_name = self._extract_entity_name(text, epic_name)
            tickets.append({
                "ticket_type": "add_entity",
                "summary": f"User should be able to add a {entity_name}",
                "priority": "High",
                "details": {
                    "entity_name": entity_name,
                    "fields": self._extract_fields(text)
                }
            })
        
        return tickets
    
    def _has_rbac_requirements(self, text: str) -> bool:
        """Check if transcript mentions RBAC"""
        rbac_keywords = ["permission", "access", "role", "only", "can view", "can edit", "restricted"]
        return any(keyword in text.lower() for keyword in rbac_keywords)
    
    def _extract_rbac(self, text: str) -> Dict:
        """Extract RBAC requirements"""
        rbac = {}
        
        for pattern in self.extraction_patterns["rbac"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                role = match.group(1).capitalize()
                action = match.group(2) if len(match.groups()) > 1 else match.group(1)
                
                if role not in rbac:
                    rbac[role] = {"permissions": [], "actions": []}
                
                rbac[role]["actions"].append(action.strip())
        
        return rbac
    
    def _extract_columns(self, text: str, tab_name: str = None) -> List[str]:
        """Extract table column names"""
        columns = []
        
        for pattern in self.extraction_patterns["table_columns"]:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                columns_text = match.group(1)
                # Split on commas, 'and', etc.
                column_names = re.split(r'[,;]|\s+and\s+', columns_text)
                columns.extend([c.strip() for c in column_names if c.strip()])
        
        return columns if columns else ["<Column 1>", "<Column 2>", "<Column 3>"]
    
    def _extract_entity_name(self, text: str, epic_name: str) -> str:
        """Extract entity name for add/create operations"""
        # Try to find what's being added
        add_match = re.search(r"add\s+(?:a\s+|an\s+)?(\w+)", text, re.IGNORECASE)
        if add_match:
            return add_match.group(1).lower()
        
        # Default to epic name
        return epic_name.lower().replace(" ", "_")
    
    def _extract_fields(self, text: str) -> List[Dict]:
        """Extract field specifications"""
        fields = []
        
        # Look for field mentions
        field_patterns = [
            r"fields?\s+(?:for|include)\s+([^.]+)",
            r"(?:need|require|capture)\s+([^.]+?)\s*[-–—]\s*(?:all\s+)?(?:required|mandatory|optional)"
        ]
        
        for pattern in field_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                fields_text = match.group(1)
                # Split on commas, 'and', etc.
                field_names = re.split(r'[,;]|\s+and\s+', fields_text)
                
                for field_name in field_names:
                    field_name = field_name.strip()
                    if field_name and len(field_name) > 2:
                        fields.append({
                            "name": field_name.capitalize(),
                            "type": self._guess_field_type(field_name),
                            "mandatory": self._is_mandatory(text, field_name)
                        })
        
        return fields if fields else [
            {"name": "<Field 1>", "type": "Text field", "mandatory": True}
        ]
    
    def _guess_field_type(self, field_name: str) -> str:
        """Guess field type from name"""
        field_lower = field_name.lower()
        
        if "date" in field_lower:
            return "Date picker"
        elif "name" in field_lower:
            return "Text field"
        elif "email" in field_lower:
            return "Email field"
        elif "phone" in field_lower:
            return "Phone field"
        elif "note" in field_lower or "comment" in field_lower or "instruction" in field_lower:
            return "Large text field"
        elif "status" in field_lower or "type" in field_lower or "frequency" in field_lower:
            return "Dropdown"
        else:
            return "Text field"
    
    def _is_mandatory(self, text: str, field_name: str) -> bool:
        """Determine if a field is mandatory"""
        # Look for context around the field name
        context_pattern = f"{field_name}[^.]*?(required|mandatory|optional)"
        match = re.search(context_pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1).lower() in ["required", "mandatory"]
        
        # Default to mandatory
        return True
    
    def _extract_action_items(self, text: str) -> List[Dict]:
        """Extract action items from transcript"""
        action_items = []
        
        # Look for action item patterns
        patterns = [
            r"(?:action item|todo|task)\s*:\s*([^.]+)",
            r"([A-Z][^.]+?)\s+(?:will|should|needs? to)\s+([^.]+)\s+by\s+(\d{1,2}/\d{1,2}|\w+ \d{1,2})"
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                action_items.append({
                    "item": match.group(0).strip(),
                    "owner": "TBD",
                    "due_date": "TBD"
                })
        
        return action_items
    
    def _identify_clarifications(self, structure: Dict) -> List[Dict]:
        """Identify areas needing clarification"""
        clarifications = []
        
        for epic in structure.get("epics", []):
            # Check for incomplete field specs
            for ticket in epic.get("tickets", []):
                if ticket.get("ticket_type") == "add_entity":
                    fields = ticket.get("details", {}).get("fields", [])
                    if any("<" in f.get("name", "") for f in fields):
                        clarifications.append({
                            "question": f"Field specifications incomplete for {ticket['summary']}",
                            "context": "Field names or types contain placeholders"
                        })
                
                # Check for missing column specs
                if ticket.get("ticket_type") == "view_table_data":
                    columns = ticket.get("details", {}).get("columns", [])
                    if any("<" in col for col in columns):
                        clarifications.append({
                            "question": f"Column specifications incomplete for {ticket['summary']}",
                            "context": "Column names contain placeholders"
                        })
        
        return clarifications
    
    def save_structured_output(self, structure: Dict, output_path: str):
        """Save structured output to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(structure, f, indent=2)
    
    def generate_review_report(self, structure: Dict) -> str:
        """Generate a human-readable review report"""
        report = []
        report.append("=" * 70)
        report.append("EXTRACTED REQUIREMENTS - REVIEW REPORT")
        report.append("=" * 70)
        
        # Metadata
        metadata = structure.get("meeting_metadata", {})
        report.append(f"\nMeeting Date: {metadata.get('date', 'Unknown')}")
        report.append(f"Attendees: {', '.join(metadata.get('attendees', ['Unknown']))}")

        # Epics
        report.append(f"\nEpics Found: {len(structure.get('epics', []))}")
        
        for i, epic in enumerate(structure.get("epics", []), 1):
            report.append(f"\n{i}. {epic['epic_name']}")
            report.append(f"   Priority: {epic['priority']}")
            report.append(f"   Tickets: {len(epic.get('tickets', []))}")
            report.append(f"   Tabs: {', '.join(epic.get('tabs', ['None']))}")
        
        # Action Items
        action_items = structure.get("action_items", [])
        if action_items:
            report.append(f"\nAction Items: {len(action_items)}")
            for item in action_items[:3]:  # Show first 3
                report.append(f"   - {item['item']}")

        # Clarifications
        clarifications = structure.get("clarifications_needed", [])
        if clarifications:
            report.append(f"\nClarifications Needed: {len(clarifications)}")
            for clarif in clarifications:
                report.append(f"   - {clarif['question']}")
        
        report.append("\n" + "=" * 70)
        
        return "\n".join(report)


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Process meeting transcripts")
    parser.add_argument('transcript_file', help="Path to transcript file")
    parser.add_argument('--output', '-o', help="Output JSON file path")
    parser.add_argument('--review', '-r', action='store_true', 
                       help="Generate review report")
    
    args = parser.parse_args()
    
    # Read transcript
    with open(args.transcript_file, 'r') as f:
        transcript_text = f.read()
    
    # Process
    processor = TranscriptProcessor()
    structure = processor.process_transcript(transcript_text)
    
    # Output
    output_path = args.output or args.transcript_file.replace('.txt', '_structured.json')
    processor.save_structured_output(structure, output_path)

    print(f"[SUCCESS] Structured output saved to: {output_path}")
    
    # Review report
    if args.review:
        report = processor.generate_review_report(structure)
        print("\n" + report)

        # Save report
        report_path = output_path.replace('.json', '_review.txt')
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\n[SUCCESS] Review report saved to: {report_path}")


if __name__ == "__main__":
    main()
