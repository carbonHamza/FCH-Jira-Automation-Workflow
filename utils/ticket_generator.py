#!/usr/bin/env python3
"""
JIRA Ticket Generator Utility
Generates JIRA tickets based on VDB project standards
"""

import json
import re
from typing import Dict, List, Optional, Tuple

class TicketGenerator:
    """Generate JIRA tickets following VDB project standards"""
    
    def __init__(self, standards_path: str = None, historical_data_path: str = None):
        """Initialize with standards and historical data"""
        self.standards_path = standards_path
        self.historical_data_path = historical_data_path
        self.standards = self._load_standards() if standards_path else {}
        self.historical_data = self._load_historical_data() if historical_data_path else {}
        
    def _load_standards(self) -> dict:
        """Load standards from markdown file"""
        # This would parse the standards markdown
        # For now, returning empty dict as placeholder
        return {}
    
    def _load_historical_data(self) -> dict:
        """Load historical ticket data"""
        if not self.historical_data_path:
            return {}
        try:
            with open(self.historical_data_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}
    
    def detect_ticket_type(self, description: str) -> str:
        """Detect the type of ticket based on description patterns"""
        description_lower = description.lower()
        
        # Pattern matching
        if "user should be able to access and view data in the table" in description_lower:
            return "view_table_data"
        elif "user should be able to add" in description_lower:
            return "add_entity"
        elif "user should be able to perform actions" in description_lower:
            return "perform_actions"
        elif "user should be able to search and filter" in description_lower or "user should be able to filter" in description_lower:
            return "search_filter"
        elif "user should be able to download" in description_lower:
            return "download"
        elif "user should be able to upload" in description_lower:
            return "upload_csv"
        elif "implement backend architecture" in description_lower:
            return "backend_architecture"
        elif "adding rbac" in description_lower or "permissions related to" in description_lower:
            return "rbac_permissions"
        elif "user should be able to view a new menu" in description_lower:
            return "nav_menu"
        elif "handling deleted data" in description_lower or "edge case" in description_lower:
            return "edge_cases"
        else:
            return "generic_story"
    
    def generate_summary(self, ticket_type: str, feature_name: str, 
                        tab_name: str = None, entity_name: str = None,
                        scope: str = None) -> str:
        """Generate ticket summary based on type and parameters"""
        
        templates = {
            "view_table_data": f"User should be able to access and view data in the table of '{tab_name or feature_name}' tab",
            "add_entity": f"User should be able to add a {entity_name or 'record'} by clicking on \"+ {entity_name or 'Add'}\" CTA",
            "perform_actions": f"User should be able to perform actions on {entity_name or 'records'} in '{tab_name or feature_name}' tab",
            "search_filter": f"User should be able to Search and Filter data in '{tab_name or feature_name}' tab",
            "download": f"User should be able to download all the records in \"{feature_name}\" feature",
            "upload_csv": f"User should be able to upload data in bulk in \"{feature_name}\" feature",
            "backend_architecture": f"BE: Implement backend architecture of \"{feature_name}\"",
            "rbac_permissions": f"Adding RBAC permissions related to \"{feature_name}\" in Permission tab of Administration menu",
            "nav_menu": f"FE: User should be able to view a new menu \"{feature_name}\" under \"Clinical\" in nav panel",
            "edge_cases": f"Handling deleted data edge cases in {feature_name}",
        }
        
        summary = templates.get(ticket_type, f"User should be able to {feature_name}")
        
        # Add scope prefix if specified
        if scope and scope.upper() in ["FE", "BE"]:
            if not summary.startswith(scope.upper() + ":"):
                summary = f"{scope.upper()}: {summary}"
        
        return summary
    
    def generate_description(self, ticket_type: str, **kwargs) -> str:
        """Generate ticket description based on type"""
        
        if ticket_type == "backend_architecture":
            return self._template_backend_architecture(**kwargs)
        elif ticket_type == "view_table_data":
            return self._template_view_table_data(**kwargs)
        elif ticket_type == "add_entity":
            return self._template_add_entity(**kwargs)
        elif ticket_type == "rbac_permissions":
            return self._template_rbac_permissions(**kwargs)
        elif ticket_type == "search_filter":
            return self._template_search_filter(**kwargs)
        else:
            return self._template_generic(**kwargs)
    
    def _template_backend_architecture(self, feature_name: str = "", **kwargs) -> str:
        """Generate backend architecture ticket description"""
        return f"""**Acceptance criteria:**

Create following:

* Model for database
* Service
* Entity
* Controller
* Routes
"""
    
    def _template_view_table_data(self, feature_name: str = "", 
                                  tab_name: str = "", columns: List[str] = None,
                                  facility_scope: str = "facility-specific", **kwargs) -> str:
        """Generate view table data ticket description"""
        
        columns_text = ""
        if columns:
            columns_text = "\n".join([f"{i+1}. {col}" for i, col in enumerate(columns)])
        else:
            columns_text = "1. <Column 1> (<Format>)\n2. <Column 2> (<Format>)\n3. <Column 3>"
        
        return f"""User should be able to access and view data in the table of '{tab_name or feature_name}' tab.

**Acceptance criteria:**

The table should have the following columns:

{columns_text}

---

### Important Notes

* Table should be sorted in descending order. Latest records should appear on top.
* Pagination to be implemented.
* Will be {facility_scope} feature
* Actions will be freezed for mobiles and smaller screens where horizontal scroll comes.
* Use new design tokens as provided in Figma designs.
"""
    
    def _template_add_entity(self, entity_name: str = "record", 
                            fields: List[Dict] = None,
                            facility_scope: str = "facility-specific", **kwargs) -> str:
        """Generate add entity ticket description"""
        
        fields_text = ""
        if fields:
            for field in fields:
                mandatory = "*" if field.get("mandatory", False) else ""
                fields_text += f"* {field['name']} {mandatory} (Type: {field.get('type', 'Text field')}. "
                if field.get("default"):
                    fields_text += f"Default: {field['default']}. "
                fields_text += ")\n"
        else:
            fields_text = """* <Field 1> * (Type: <Type>. Default: <Default>)
* <Field 2> * (Type: <Type>)
* <Field 3> (Type: <Type>. Mandatory only when <Condition>)
* <Comments/Notes> (Type: Large expandable text. <Mandatory/Optional>)"""
        
        return f"""User should be able to add a {entity_name} by clicking on "+ {entity_name.capitalize()}" CTA that will open a modal with fields:

{fields_text}
* Save CTA

**Submit workflow:**

* Add a record in table
* Auto-populate <auto fields>
* Send notification to <RBAC> users. Details:
  Type: <Type>;
  Title: <Title>;
  Body: <Body text>;
  View CTA takes user to <destination>

---

### Important Notes

* Will be {facility_scope} feature
* <Mobile behavior>
"""
    
    def _template_rbac_permissions(self, feature_name: str = "", 
                                   permissions: List[str] = None, **kwargs) -> str:
        """Generate RBAC permissions ticket description"""
        
        perms_list = ""
        perms_details = ""
        if permissions:
            perms_list = "\n".join([f"* {perm}" for perm in permissions])
            perms_details = "\n\n".join([
                f"**{perm}**: EDIT of this should allow the user to <actions>. VIEW access should only allow <read actions>."
                for perm in permissions
            ])
        else:
            perms_list = "* <Permission 1>\n* <Permission 2>"
            perms_details = """**<Permission 1>**: EDIT of this should allow the user to <actions>. VIEW access should only allow <read actions>.

**<Permission 2>**: EDIT of this should allow <actions>. VIEW access should allow <read actions>."""
        
        return f"""Add RBAC permissions related to "{feature_name}" in Permission tab of Administration menu under the <Sub-tab> sub-tab.

**Acceptance criteria:**

Under <Sub-tab>, there should be a heading of {feature_name} with the following permissions:

{perms_list}

{perms_details}

---

### Important Notes

* HIDE of <Permission 1> should hide <UI element>.
* HIDE of <Permission 2> should hide <UI element>.
* If both are HIDE for a role, then the feature should not appear in the nav bar.
"""
    
    def _template_search_filter(self, feature_name: str = "", 
                               tab_name: str = "",
                               search_fields: List[str] = None,
                               filters: List[Dict] = None, **kwargs) -> str:
        """Generate search and filter ticket description"""
        
        search_text = "User should be able to perform Search on Patient Name. Implement Fuzzy Logic"
        if search_fields:
            search_text = f"User should be able to perform Search on {', '.join(search_fields)}. Implement Fuzzy Logic"
        
        filters_text = ""
        if filters:
            for i, f in enumerate(filters, 1):
                filters_text += f"{i}. {f['name']} ({f.get('type', 'Dropdown')}, by default {f.get('default', 'All')})\n"
        else:
            filters_text = """1. <Filter 1> (by default <Default>)
2. <Filter 2> (by default <Default>)
3. <Filter 3> (by default <Default>)"""
        
        return f"""User should be able to filter the records in table of {tab_name or feature_name}. 

**Acceptance criteria:** 

User should be able to view and click on "Filter CTA" that will open a drawer. Including:  

**Search**

{search_text}

Text Placeholder: "_**Search Patient Name**_"

---

**Filters**

User should be able to click on the Filters CTA and access filters drawer and apply the following filters:

{filters_text}

---

### Important Notes

* Table should be filtered based on selected filter options
"""
    
    def _template_generic(self, **kwargs) -> str:
        """Generate generic ticket description"""
        return """**Acceptance criteria:**

<Description of what the user should be able to do>

---

### Important Notes

* <Note 1>
* <Note 2>
"""
    
    def suggest_priority(self, ticket_type: str, context: str = "") -> str:
        """Suggest priority based on ticket type and context"""
        context_lower = context.lower()
        
        # Highest priority indicators
        if any(word in context_lower for word in ["demo", "blocker", "critical", "bug", "urgent"]):
            return "Highest"
        
        # High priority for core feature stories
        if ticket_type in ["view_table_data", "add_entity", "perform_actions", "backend_architecture", "nav_menu", "rbac_permissions"]:
            return "High"
        
        # Medium for supporting features
        return "Medium"
    
    def create_ticket(self, issue_type: str, summary: str, description: str,
                     priority: str = "Medium", epic_key: str = None) -> Dict:
        """Create a ticket data structure ready for JIRA"""
        
        ticket = {
            "fields": {
                "project": {"key": "VDB"},
                "summary": summary,
                "description": description,
                "issuetype": {"name": issue_type},
                "priority": {"name": priority}
            }
        }
        
        if epic_key:
            ticket["fields"]["parent"] = {"key": epic_key}
        
        return ticket
    
    def generate_epic_tickets(self, epic_name: str, 
                             include_backend: bool = True,
                             include_rbac: bool = True,
                             include_nav: bool = True,
                             tabs: List[str] = None) -> List[Dict]:
        """Generate standard set of tickets for a new epic"""
        
        tickets = []
        
        # 1. Backend Architecture (if requested)
        if include_backend:
            summary = self.generate_summary("backend_architecture", epic_name)
            description = self.generate_description("backend_architecture", feature_name=epic_name)
            tickets.append({
                "type": "Story",
                "summary": summary,
                "description": description,
                "priority": "High"
            })
        
        # 2. RBAC Permissions (if requested)
        if include_rbac:
            summary = self.generate_summary("rbac_permissions", epic_name)
            description = self.generate_description("rbac_permissions", feature_name=epic_name)
            tickets.append({
                "type": "Story",
                "summary": summary,
                "description": description,
                "priority": "High"
            })
        
        # 3. Navigation Menu (if requested)
        if include_nav:
            summary = self.generate_summary("nav_menu", epic_name)
            description = self._template_generic()
            tickets.append({
                "type": "Story",
                "summary": summary,
                "description": description,
                "priority": "High"
            })
        
        # 4. Tab-specific tickets
        if tabs:
            for tab in tabs:
                # View table data
                summary = self.generate_summary("view_table_data", epic_name, tab_name=tab)
                description = self.generate_description("view_table_data", tab_name=tab)
                tickets.append({
                    "type": "Story",
                    "summary": summary,
                    "description": description,
                    "priority": "High"
                })
                
                # Search and filter
                summary = self.generate_summary("search_filter", epic_name, tab_name=tab)
                description = self.generate_description("search_filter", tab_name=tab)
                tickets.append({
                    "type": "Story",
                    "summary": summary,
                    "description": description,
                    "priority": "High"
                })
        
        return tickets


if __name__ == "__main__":
    # Example usage
    generator = TicketGenerator()
    
    # Generate a backend architecture ticket
    summary = generator.generate_summary("backend_architecture", "Patient Management")
    description = generator.generate_description("backend_architecture", feature_name="Patient Management")
    
    print("=" * 70)
    print("EXAMPLE: Backend Architecture Ticket")
    print("=" * 70)
    print(f"Summary: {summary}")
    print(f"\nDescription:\n{description}")
    print("=" * 70)
