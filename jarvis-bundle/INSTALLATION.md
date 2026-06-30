# Jarvis Agent Bundle — Installation Guide

Complete installation instructions for Windows, macOS, and Linux systems.

---

## ⚙️ Prerequisites

1. **VS Code** installed with **GitHub Copilot** extension enabled
2. **Python 3.8+** (only needed if you plan to use utility scripts)
3. **Admin/sudo privileges** (for copying files to system directories on macOS/Linux)

---

## 📥 Installation on Windows

### Step 1: Locate Your VS Code User Data Folder

Open PowerShell and run:
```powershell
echo $env:APPDATA\Code\User
```

This is typically: `C:\Users\<YourUsername>\AppData\Roaming\Code\User\`

### Step 2: Copy Agent Files

Copy all `.agent.md` files from the bundle's `agents/` folder:
```powershell
Copy-Item .\agents\*.agent.md -Destination "$env:APPDATA\Code\User\prompts\" -Force
```

### Step 3: Copy Skills

Copy the entire `skills/` folder contents:
```powershell
# Create skills directory structure if it doesn't exist
New-Item -ItemType Directory -Path "$env:USERPROFILE\.agents\skills" -Force -ErrorAction SilentlyContinue

# Copy each skill folder
Copy-Item .\skills\* -Destination "$env:USERPROFILE\.agents\skills\" -Recurse -Force
```

### Step 4: Copy Scripts

Create the scripts directory and copy Python scripts:
```powershell
New-Item -ItemType Directory -Path "$env:APPDATA\Code\User\prompts\scripts" -Force -ErrorAction SilentlyContinue
Copy-Item .\scripts\*.py -Destination "$env:APPDATA\Code\User\prompts\scripts\" -Force
```

### Step 5: Copy Instructions

Copy the instructions file:
```powershell
New-Item -ItemType Directory -Path "$env:APPDATA\Code\User\prompts\instructions" -Force -ErrorAction SilentlyContinue
Copy-Item .\instructions\general.instructions.md -Destination "$env:APPDATA\Code\User\prompts\instructions\" -Force
```

### Step 6: Reload VS Code

1. Press `Ctrl+Shift+P`
2. Type: **Reload Window**
3. Press Enter

---

## 📥 Installation on macOS / Linux

### Step 1: Locate Your VS Code User Data Folder

Open Terminal and run:
```bash
echo ~/.config/Code/User/
```

This is typically: `/Users/<YourUsername>/.config/Code/User/` (macOS) or `/home/<YourUsername>/.config/Code/User/` (Linux)

### Step 2: Copy Agent Files

```bash
cp ./agents/*.agent.md ~/.config/Code/User/prompts/
```

### Step 3: Copy Skills

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.agents/skills

# Copy all skill folders
cp -r ./skills/* ~/.agents/skills/
```

### Step 4: Copy Scripts

```bash
# Create scripts directory if it doesn't exist
mkdir -p ~/.config/Code/User/prompts/scripts

# Copy Python scripts
cp ./scripts/*.py ~/.config/Code/User/prompts/scripts/

# Make scripts executable
chmod +x ~/.config/Code/User/prompts/scripts/*.py
```

### Step 5: Copy Instructions

```bash
# Create instructions directory if it doesn't exist
mkdir -p ~/.config/Code/User/prompts/instructions

# Copy instructions file
cp ./instructions/general.instructions.md ~/.config/Code/User/prompts/instructions/
```

### Step 6: Reload VS Code

1. Press `Cmd+Shift+P` (macOS) or `Ctrl+Shift+P` (Linux)
2. Type: **Reload Window**
3. Press Enter

---

## ✅ Verify Installation

After reloading VS Code:

1. Open a **Copilot Chat** panel
2. Type `@Jarvis` — you should see Jarvis appear in the autocomplete suggestions
3. Type `@Jarvis status` to verify the agent is responding

You should also see these agents available:
- `@Jarvis-develop`
- `@Jarvis-test`
- `@Jarvis-docs`
- `@Jarvis-clearchats`
- `@AISwitch`

---

## 🧪 Test the Scripts

### Test clear-old-chats.py

**Windows:**
```powershell
python "$env:APPDATA\Code\User\prompts\scripts\clear-old-chats.py" --help
```

**macOS/Linux:**
```bash
python3 ~/.config/Code/User/prompts/scripts/clear-old-chats.py --help
```

You should see usage instructions.

### Test ai-switch.py

**Windows:**
```powershell
python "$env:APPDATA\Code\User\prompts\scripts\ai-switch.py" status
```

**macOS/Linux:**
```bash
python3 ~/.config/Code/User/prompts/scripts/ai-switch.py status
```

You should see which AI assistant is currently active.

---

## 🔧 Troubleshooting

### Agents Don't Appear in Copilot Chat

1. Verify files copied to correct location:
   - Windows: `%APPDATA%\Code\User\prompts\`
   - macOS/Linux: `~/.config/Code/User/prompts/`

2. Check file extensions are `.agent.md` (not `.agent.md.txt`)

3. Reload VS Code window again

4. Check VS Code Developer Console for errors:
   - Press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (macOS)
   - Look for errors in the Console tab

### Scripts Don't Run

1. Verify Python is installed:
   ```bash
   python --version  # or python3 --version
   ```

2. Check script permissions (macOS/Linux):
   ```bash
   chmod +x ~/.config/Code/User/prompts/scripts/*.py
   ```

3. Use full path to Python if needed:
   ```bash
   /usr/bin/python3 <script-path>
   ```

### Skills Not Loading

1. Verify skills copied to:
   - Windows: `%USERPROFILE%\.agents\skills\`
   - macOS/Linux: `~/.agents/skills/`

2. Each skill should be in its own subfolder with a `SKILL.md` file

3. Reload VS Code

---

## 🔄 Updating

To update Jarvis agents or skills:

1. Extract the new bundle
2. Repeat the installation steps (files will be overwritten)
3. Reload VS Code

---

## 🗑️ Uninstallation

### Windows

```powershell
# Remove agents
Remove-Item "$env:APPDATA\Code\User\prompts\Jarvis*.agent.md"
Remove-Item "$env:APPDATA\Code\User\prompts\AISwitch.agent.md"

# Remove skills
Remove-Item "$env:USERPROFILE\.agents\skills\jarvis-*" -Recurse
Remove-Item "$env:USERPROFILE\.agents\skills\caveman*" -Recurse
Remove-Item "$env:USERPROFILE\.agents\skills\compress" -Recurse
Remove-Item "$env:USERPROFILE\.agents\skills\find-skills" -Recurse

# Remove scripts
Remove-Item "$env:APPDATA\Code\User\prompts\scripts\clear-old-chats.py"
Remove-Item "$env:APPDATA\Code\User\prompts\scripts\ai-switch.py"

# Remove instructions
Remove-Item "$env:APPDATA\Code\User\prompts\instructions\general.instructions.md"
```

### macOS / Linux

```bash
# Remove agents
rm ~/.config/Code/User/prompts/Jarvis*.agent.md
rm ~/.config/Code/User/prompts/AISwitch.agent.md

# Remove skills
rm -rf ~/.agents/skills/jarvis-*
rm -rf ~/.agents/skills/caveman*
rm -rf ~/.agents/skills/compress
rm -rf ~/.agents/skills/find-skills

# Remove scripts
rm ~/.config/Code/User/prompts/scripts/clear-old-chats.py
rm ~/.config/Code/User/prompts/scripts/ai-switch.py

# Remove instructions
rm ~/.config/Code/User/prompts/instructions/general.instructions.md
```

Then reload VS Code.

---

## 📞 Support

For issues or questions:
- Review agent `.agent.md` files for inline documentation
- Check skill `SKILL.md` files for workflow details
- Consult VS Code Copilot documentation

---

**Installation complete!** Start using Jarvis with `@Jarvis` in Copilot Chat.
