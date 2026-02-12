#!/usr/bin/env python3
"""
End-to-End JIRA Automation Workflow
Complete pipeline from transcript to JIRA tickets
"""

import sys
import json
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / 'utils'))
sys.path.insert(0, str(Path(__file__).parent))

from ticket_generator import TicketGenerator
from process_transcript import TranscriptProcessor


class WorkflowOrchestrator:
    """Orchestrate the complete transcript-to-JIRA workflow"""
    
    def __init__(self):
        self.transcript_processor = TranscriptProcessor()
        self.ticket_generator = TicketGenerator()
        self.workflow_state = {}
    
    def run_complete_workflow(self, transcript_path: str, 
                             interactive: bool = True) -> dict:
        """
        Run the complete workflow from transcript to tickets
        
        Steps:
        1. Process transcript → structured requirements
        2. Review with user (if interactive)
        3. Generate JIRA tickets
        4. Save for JIRA push
        
        Args:
            transcript_path: Path to meeting transcript
            interactive: Whether to pause for user review
            
        Returns:
            dict with workflow results
        """
        
        results = {
            "steps_completed": [],
            "files_generated": [],
            "tickets_created": 0
        }
        
        print("\n" + "=" * 70)
        print("JIRA AUTOMATION WORKFLOW - COMPLETE PIPELINE")
        print("=" * 70)
        
        # STEP 1: Process Transcript
        print("\n📝 STEP 1: Processing Transcript...")
        print(f"   Input: {transcript_path}")
        
        with open(transcript_path, 'r') as f:
            transcript_text = f.read()
        
        structured_data = self.transcript_processor.process_transcript(transcript_text)
        
        # Save structured output
        structured_path = transcript_path.replace('.txt', '_structured.json')
        self.transcript_processor.save_structured_output(structured_data, structured_path)
        results["files_generated"].append(structured_path)
        results["steps_completed"].append("transcript_processing")
        
        print(f"   ✅ Structured data saved: {structured_path}")
        print(f"   📊 Found {len(structured_data['epics'])} epic(s)")
        
        # Generate review report
        review_report = self.transcript_processor.generate_review_report(structured_data)
        review_path = transcript_path.replace('.txt', '_review.txt')
        with open(review_path, 'w') as f:
            f.write(review_report)
        results["files_generated"].append(review_path)
        
        print(f"   📄 Review report: {review_path}")
        
        # STEP 2: User Review (if interactive)
        if interactive:
            print("\n" + "=" * 70)
            print("📋 STEP 2: User Review")
            print("=" * 70)
            print(review_report)
            
            response = input("\n❓ Proceed with ticket generation? (yes/no/edit): ").strip().lower()
            
            if response == 'no':
                print("\n❌ Workflow cancelled by user")
                return results
            elif response == 'edit':
                print(f"\n✏️  Please edit: {structured_path}")
                print("   Then run workflow again with edited file.")
                return results
        else:
            results["steps_completed"].append("automated_review")
        
        # STEP 3: Generate Tickets
        print("\n" + "=" * 70)
        print("🎫 STEP 3: Generating JIRA Tickets")
        print("=" * 70)
        
        all_tickets = []
        
        for epic in structured_data['epics']:
            print(f"\n   Processing epic: {epic['epic_name']}")
            
            for ticket_spec in epic['tickets']:
                ticket = self._generate_ticket_from_spec(ticket_spec, epic)
                all_tickets.append(ticket)
                print(f"      ✓ {ticket_spec['ticket_type']}: {ticket['summary'][:60]}...")
        
        results["tickets_created"] = len(all_tickets)
        results["steps_completed"].append("ticket_generation")
        
        # STEP 4: Save Ticket Batch
        print("\n" + "=" * 70)
        print("💾 STEP 4: Saving Ticket Batch")
        print("=" * 70)
        
        batch_data = {
            "project": "VDB",
            "source_transcript": transcript_path,
            "structured_data": structured_path,
            "total_tickets": len(all_tickets),
            "epics": [epic['epic_name'] for epic in structured_data['epics']],
            "tickets": all_tickets,
            "metadata": {
                "generated_date": structured_data['meeting_metadata']['date'],
                "meeting_attendees": structured_data['meeting_metadata'].get('attendees', []),
                "clarifications_needed": structured_data.get('clarifications_needed', [])
            }
        }
        
        batch_path = transcript_path.replace('.txt', '_tickets.json')
        with open(batch_path, 'w') as f:
            json.dump(batch_data, f, indent=2)
        
        results["files_generated"].append(batch_path)
        results["steps_completed"].append("batch_creation")
        
        print(f"   ✅ Ticket batch saved: {batch_path}")
        print(f"   📊 Total tickets: {len(all_tickets)}")
        
        # STEP 5: Summary
        print("\n" + "=" * 70)
        print("✨ WORKFLOW COMPLETE")
        print("=" * 70)
        
        print(f"\n📁 Files Generated:")
        for file_path in results["files_generated"]:
            print(f"   - {file_path}")
        
        print(f"\n🎫 Tickets Ready: {results['tickets_created']}")
        
        print(f"\n🚀 Next Steps:")
        print(f"   1. Review tickets: cat {batch_path}")
        print(f"   2. Dry run: python3 scripts/push_to_jira.py {batch_path} --dry-run")
        print(f"   3. Push to JIRA: python3 scripts/push_to_jira.py {batch_path} --epic-key VDB-XXXX")
        
        if structured_data.get('clarifications_needed'):
            print(f"\n⚠️  {len(structured_data['clarifications_needed'])} clarification(s) needed:")
            for clarif in structured_data['clarifications_needed'][:3]:
                print(f"   - {clarif['question']}")
        
        print("\n" + "=" * 70)
        
        return results
    
    def _generate_ticket_from_spec(self, ticket_spec: dict, epic: dict) -> dict:
        """Generate a complete ticket from specification"""
        
        ticket_type = ticket_spec['ticket_type']
        details = ticket_spec.get('details', {})
        
        # Generate description using ticket generator
        description = self.ticket_generator.generate_description(
            ticket_type=ticket_type,
            feature_name=epic['epic_name'],
            **details
        )
        
        # Build complete ticket
        ticket = {
            "type": "Story",
            "summary": ticket_spec['summary'],
            "description": description,
            "priority": ticket_spec.get('priority', 'High')
        }
        
        return ticket
    
    def run_step_by_step(self, transcript_path: str):
        """Run workflow with pause at each step"""
        
        print("\n🎯 Step-by-Step Mode")
        print("   The workflow will pause after each step for your review.")
        
        # Step 1
        input("\n▶️  Press Enter to process transcript...")
        self.run_complete_workflow(transcript_path, interactive=True)


def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Complete workflow from transcript to JIRA tickets"
    )
    parser.add_argument('transcript', help="Path to meeting transcript file")
    parser.add_argument('--non-interactive', action='store_true',
                       help="Run without user review pauses")
    parser.add_argument('--step-by-step', action='store_true',
                       help="Pause after each step")
    
    args = parser.parse_args()
    
    orchestrator = WorkflowOrchestrator()
    
    if args.step_by_step:
        orchestrator.run_step_by_step(args.transcript)
    else:
        orchestrator.run_complete_workflow(
            args.transcript,
            interactive=not args.non_interactive
        )


if __name__ == "__main__":
    main()
