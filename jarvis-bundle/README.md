# Jarvis Agent Bundle — Portable Installation

This bundle contains the complete Jarvis agent system with all subagents, skills, prompts, instructions, and utility scripts. It's designed to be portable across Windows and macOS.

## Contents

```
jarvis-bundle/
├── README.md                    # This file
├── INSTALLATION.md              # Setup instructions for Windows and macOS
├── agents/                      # Main agents and subagents
│   ├── Jarvis.agent.md
│   ├── Jarvis-develop.agent.md
│   ├── Jarvis-test.agent.md
│   ├── Jarvis-docs.agent.md
│   ├── Jarvis-clearchats.agent.md
│   └── AISwitch.agent.md
├── skills/                      # Agent skills and workflows
│   ├── caveman/
│   ├── caveman-review/
│   ├── compress/
│   ├── find-skills/
│   ├── jarvis-orchestrate/
│   ├── jarvis-develop-workflow/
│   ├── jarvis-test-workflow/
│   ├── jarvis-clearchats-workflow/
│   └── jarvis-docs-workflow/
├── instructions/                # Coding and workflow instructions
│   └── general.instructions.md
└── scripts/                      # Utility scripts
    ├── clear-old-chats.py
    └── ai-switch.py
```

## What is Jarvis?

Jarvis is an orchestrator agent for Python and PHP projects. It coordinates four specialist subagents:

- **Jarvis-test**: Lead Test Engineer — audits codebases, finds bugs, produces test findings reports
- **Jarvis-develop**: Lead Developer — implements features, fixes, and automation solutions
- **Jarvis-docs**: Lead Technical Writer — creates and maintains documentation
- **Jarvis-clearchats**: Utility — manages VS Code Copilot chat session cleanup

Additional utilities:
- **AISwitch**: Toggles between GitHub Copilot Chat and Amazon Q Developer in VS Code

## Quick Start

### 1. Extract the Bundle

Unzip this bundle to a location you'll remember, e.g.:
- **Windows**: `C:\Users\<YourName>\AppData\Roaming\Code\User\jarvis-bundle`
- **macOS**: `~/.config/Code/User/jarvis-bundle`

### 2. Install to VS Code

Follow the **INSTALLATION.md** guide for your operating system.

### 3. Verify Installation

After installation, in VS Code:
- Open Command Palette: `Ctrl+Shift+P` (Windows) or `Cmd+Shift+P` (macOS)
- Type `@jarvis` — you should see all Jarvis agents available

### 4. Use Jarvis

Invoke Jarvis by mentioning it in a chat:

```
@Jarvis test the users module for bugs and security issues
@Jarvis implement the fix from test-findings.md  
@Jarvis document the database schema and API endpoints
@Jarvis clear chat history older than 7 days
```

## Folder Structure

| Directory | Purpose |
|-----------|---------|
| `agents/` | Agent definition files (`.agent.md`) — copy to VS Code agents folder |
| `skills/` | Skill modules with workflows and checklists — copy to VS Code skills folder |
| `instructions/` | Coding style and project management instructions — copy to VS Code instructions folder |
| `scripts/` | Python utility scripts — referenced by agents and subagents |

## System Requirements

- VS Code (latest stable version)
- Python 3.8+ (for script execution)
- GitHub Copilot Chat or Amazon Q Developer (at least one enabled)

## Features by Agent

### Jarvis (Orchestrator)

- **Delegates tasks** to the appropriate specialist subagent
- **Coordinates multi-step workflows** (test → fix → document)
- **Ensures end-to-end delivery** with no gaps

### Jarvis-test

- Audits Python and PHP codebases
- Identifies bugs, security issues, and code quality problems
- Produces structured findings reports
- Checks AWS/Bedrock and Lambda integrations
- Verifies prompt configurations

### Jarvis-develop

- Implements features and fixes from test reports
- Builds automation pipelines (RPA, ETL, API integrations)
- Handles AWS Bedrock and Lambda integration
- Applies concurrency patterns (asyncio, threading, multiprocessing)
- Maintains modular architecture

### Jarvis-docs

- Writes and maintains README files
- Produces setup guides, API references, and workflow documentation
- Creates docstrings and inline comments
- Verifies all documentation against actual code

### Jarvis-clearchats

- Clears stale VS Code Copilot chat sessions
- Supports dry-run preview before deletion
- Creates automatic backups

### AISwitch

- Toggles between GitHub Copilot Chat and Amazon Q Developer
- Ensures only one assistant is active at a time
- Manages VS Code extension enablement

## Skills Included

| Skill | Purpose |
|-------|---------|
| **caveman** | Ultra-compressed communication mode to save tokens |
| **caveman-review** | Terse code review comments |
| **compress** | Compresses memory files to reduce input tokens |
| **find-skills** | Discovers and installs agent skills from the ecosystem |
| **jarvis-orchestrate** | Orchestration workflow and routing rules |
| **jarvis-develop-workflow** | Development workflow with guardrails |
| **jarvis-test-workflow** | Testing and auditing workflow |
| **jarvis-clearchats-workflow** | Safe chat session deletion workflow |
| **jarvis-docs-workflow** | Documentation standards and requirements |

## Troubleshooting

### Agents don't appear in VS Code

1. Verify files are in the correct VS Code user data directory
2. Reload the VS Code window: `Ctrl+Shift+P` → `Reload Window`
3. Check that the agent files have `.agent.md` extension (not `.md`)

### Scripts don't run

1. Ensure Python 3.8+ is installed and available in PATH
2. For `clear-old-chats.py`: Close VS Code before running (database lock issue)
3. For `ai-switch.py`: Run with `python` command, e.g., `python scripts/ai-switch.py status`

### Permission issues on macOS

If scripts show permission errors:

```bash
chmod +x scripts/clear-old-chats.py
chmod +x scripts/ai-switch.py
```

## Updating Skills

To update a skill with new content, replace the relevant folder in your installed location with the updated version from this bundle.

## Support & Documentation

For each agent/skill, detailed documentation is embedded in its `.md` or `SKILL.md` file. Read the file directly for:
- Exact constraints and guardrails
- Workflow phases
- Input/output formats
- Usage examples

## License & Credits

This Jarvis agent bundle is provided as-is for use within your VS Code environment. It is designed to work seamlessly across Windows and macOS operating systems.

---

**Next Step**: See [INSTALLATION.md](INSTALLATION.md) for OS-specific setup instructions.
