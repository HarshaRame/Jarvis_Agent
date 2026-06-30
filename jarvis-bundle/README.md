# Jarvis AI Agent Bundle

**Complete portable bundle of the Jarvis AI agent system and all subagents.**

This bundle contains everything needed to install and use the Jarvis orchestrator agent, its specialized subagents, workflow skills, utility scripts, and coding instructions across Windows, macOS, and Linux systems.

---

## 📦 What's Included

### **Agents** (6 total)
AI agent definition files (`.agent.md`) that integrate with VS Code Copilot:

- **Jarvis** — Orchestrator agent that delegates to specialist subagents
- **Jarvis-develop** — Developer subagent for implementing features, fixes, and code
- **Jarvis-test** — Test engineer subagent for auditing, finding bugs, and quality assurance
- **Jarvis-docs** — Documentation writer for README files, API docs, and guides
- **Jarvis-clearchats** — Utility to clear old VS Code chat sessions
- **AISwitch** — Toggle between GitHub Copilot Chat and Amazon Q Developer

### **Skills** (9 total)
Workflow documentation files (`SKILL.md`) for domain-specific operations:

- **caveman** — Ultra-compressed communication mode (saves ~75% tokens)
- **caveman-review** — Terse code review comments
- **compress** — Compress memory files to caveman format
- **find-skills** — Discover and install agent skills from ecosystem
- **jarvis-orchestrate** — Orchestration workflow and routing rules
- **jarvis-develop-workflow** — Implementation workflow, guardrails, modularity standards
- **jarvis-test-workflow** — Audit workflow, severity classification, AWS/AI checks
- **jarvis-clearchats-workflow** — Safe deletion workflow with dry-run gate
- **jarvis-docs-workflow** — Documentation standards, README structure

### **Scripts** (2 total)
Cross-platform Python utilities:

- **clear-old-chats.py** — Remove VS Code Copilot chat sessions older than N days
- **ai-switch.py** — Switch between GitHub Copilot and Amazon Q (only one active at a time)

### **Instructions** (1 file)
General coding standards and best practices:

- **general.instructions.md** — Lead automation developer role definition, working style, validation rules

---

## 🚀 Quick Start

1. **Extract** this bundle to a temporary location
2. **Follow** the installation guide in [INSTALLATION.md](INSTALLATION.md)
3. **Reload** VS Code after copying files
4. **Invoke** Jarvis with `@Jarvis` in a Copilot chat

---

## 🎯 Key Features

- **Cross-platform** — Works on Windows, macOS, and Linux
- **Portable** — All paths use OS-specific environment variables
- **Modular** — Each agent and skill is independent
- **Extensible** — Add new skills or customize agents
- **Well-documented** — Every component has inline documentation

---

## 📋 Requirements

- **VS Code** with GitHub Copilot extension installed
- **Python 3.8+** (for utility scripts only; agents don't require Python)
- **Access to VS Code User data folder**:
  - Windows: `%APPDATA%\Code\User\`
  - macOS: `~/.config/Code/User/`
  - Linux: `~/.config/Code/User/`

---

## 📚 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** — Step-by-step installation for Windows and macOS
- **[agents/](agents/)** — Individual agent definition files with usage examples
- **[skills/](skills/)** — Workflow documentation for each skill module
- **[scripts/](scripts/)** — Python utility scripts with inline help

---

## 🔧 Usage Examples

### Orchestrate a task with Jarvis
```
@Jarvis test the login module for security issues, then fix any findings
```

### Research before implementing
```
@Jarvis research how to implement OAuth 2.0 in this codebase
```

### Generate documentation
```
@Jarvis document the API endpoints in the user module
```

### Clear old chat sessions
```
@Jarvis-clearchats clear chats older than 7 days
```

### Switch AI assistants
```
@AISwitch amazonq
```

---

## 🛠️ Customization

All agent and skill files are plain Markdown with YAML frontmatter. You can:

- Edit agent descriptions and workflows
- Modify skill templates and rules
- Add new agents or skills following the existing patterns
- Customize general coding instructions in `instructions/general.instructions.md`

---

## 📄 License

This bundle is provided as-is for internal use. Jarvis agents and skills are built on top of VS Code Copilot's agent framework.

---

## 💡 Support

For questions or issues:
1. Check agent inline documentation (each `.agent.md` file contains usage rules)
2. Review skill SKILL.md files for workflow details
3. Consult VS Code Copilot agent documentation

---

**Version**: 1.0  
**Last Updated**: June 2025  
**Compatibility**: Windows, macOS, Linux
