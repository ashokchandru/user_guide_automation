# User Guide Automation
This readme gives an overview of user guide automation process

There are different release cycles. <br>
**Major release (Version level)**
* The product version changes. Almost 50% of the chapters are affected.
* Overall change to content would be about 20%

**Minor release**
* Depends upon the release. Content changes vary from 5% - 10%

**Patch release**
* Minimal changes.

Files required for the workflow:
* userguide.md 
* updates.json
* mapping.py
* guide_review.md

## Important Changes to define updates.json file:
* Change version numbers throghout the document
* Map each section with mapping tags in the Python file. e.g. "Run a Scan" could be defined as "run_scan"

## Workflow
* User guide text is in md format. We break the file into JSON object files.
* Technical writer checks the tickets and authors content.
* Checks the mapping document
* Updates updates.json file in with updates
* Uploads the JSON file to the AI agent
* AI agent updates userguide.md with changes in the JSON file
