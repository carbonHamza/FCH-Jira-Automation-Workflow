# Transcripts Directory

This directory is for your meeting transcript files.

## Usage

1. Place your transcript `.txt` files here
2. Run the processing scripts on them
3. Generated files (JSON, review reports) will be created here

## Generated Files

The system will create these files from your transcripts:
- `*_structured.json` - Extracted structured data
- `*_review.txt` - Human-readable review report
- `*_tickets.json` - Generated JIRA tickets

## Note

All transcript files and generated outputs are automatically excluded from Git (via `.gitignore`), so your private meeting notes won't be committed to the repository.

## Example

```bash
# Add your transcript
cp your-meeting-notes.txt transcripts/

# Process it
python3 scripts/process_transcript.py transcripts/your-meeting-notes.txt --review

# Or use the full workflow
python3 scripts/workflow.py transcripts/your-meeting-notes.txt
```
