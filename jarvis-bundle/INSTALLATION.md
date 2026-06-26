# Installation Guide — Jarvis Agent Bundle

Choose your operating system below for step-by-step installation instructions.

---

## macOS Installation

### Step 1: Locate Your VS Code User Data Directory

```bash
open ~/.config/Code/User
```

If the directory doesn't exist, create it:

```bash
mkdir -p ~/.config/Code/User
```

### Step 2: Copy Bundle Files

1. **Extract the bundle** to your Downloads folder (or preferred location).

2. **Copy agent files** to VS Code agents folder:

```bash
# Create the agents directory if it doesn't exist
mkdir -p ~/.config/Code/User/prompts

# Copy agent files
cp jarvis-bundle/agents/*.agent.md ~/.config/Code/User/prompts/
```

3. **Copy skills** to VS Code skills folder:

```bash
# Create the skills directory
mkdir -p ~/.config/Code/User/.agents/skills

# Copy all skill folders
cp -r jarvis-bundle/skills/* ~/.config/Code/User/.agents/skills/
```

4. **Copy instructions**:

```bash
# Create the instructions directory
mkdir -p ~/.config/Code/User/prompts/instructions

# Copy instruction files
cp jarvis-bundle/instructions/*.instructions.md ~/.config/Code/User/prompts/instructions/
```

5. **Copy scripts**:

```bash
# Create the scripts directory
mkdir -p ~/.config/Code/User/prompts/scripts

# Copy scripts
cp jarvis-bundle/scripts/*.py ~/.config/Code/User/prompts/scripts/

# Make scripts executable
chmod +x ~/.config/Code/User/prompts/scripts/*.py
```

### Step 3: Update Script Paths (macOS)

The scripts reference hardcoded Windows paths. Update them for macOS:

1. **Edit `~/.config/Code/User/prompts/scripts/clear-old-chats.py`**:

   Find this line (around line 18):
   ```python
   DB_PATH = os.path.join(
       os.environ["APPDATA"],
       "Code", "User", "globalStorage", "state.vscdb"
   )
   ```

   Replace with:
   ```python
   DB_PATH = os.path.expanduser(
       "~/.config/Code/User/globalStorage/state.vscdb"
   )
   ```

2. **Edit `~/.config/Code/User/prompts/scripts/ai-switch.py`**:

   Find these lines (around lines 24-31):
   ```python
   DB_PATH = os.path.join(
       os.environ["APPDATA"],
       "Code", "User", "globalStorage", "state.vscdb"
   )
   STATE_FILE = os.path.join(
       os.environ["APPDATA"],
       "Code", "User", "ai-switch.state"
   )
   ```

   Replace with:
   ```python
   DB_PATH = os.path.expanduser(
       "~/.config/Code/User/globalStorage/state.vscdb"
   )
   STATE_FILE = os.path.expanduser(
       "~/.config/Code/User/ai-switch.state"
   )
   ```

### Step 4: Update Agent Script References

Update any agent files that reference hardcoded script paths. 

For example, in `~/.config/Code/User/prompts/Jarvis-clearchats.agent.md`, find:
```xml
<script>
C:\Users\hkr1\AppData\Roaming\Code\User\prompts\scripts\clear-old-chats.py
</script>
```

Replace with:
```xml
<script>
~/.config/Code/User/prompts/scripts/clear-old-chats.py
</script>
```

Do the same for `AISwitch.agent.md`.

### Step 5: Verify Installation

1. **Reload VS Code**:
   ```
   Cmd+Shift+P → Reload Window
   ```

2. **Open Command Palette**:
   ```
   Cmd+Shift+P → type "@jarvis"
   ```

   You should see all Jarvis agents listed.

### Step 6: Test Jarvis

Open a chat in VS Code and try:

```
@Jarvis test the following file for bugs: [paste a file path]
```

---

## Windows Installation

### Step 1: Locate Your VS Code User Data Directory

1. Open File Explorer.
2. Navigate to: `C:\Users\<YourUsername>\AppData\Roaming\Code\User`

   (If AppData is hidden, enable "Show hidden files" in View options)

### Step 2: Copy Bundle Files

1. **Extract the bundle** to your Downloads folder (or preferred location).

2. **Copy agent files**:

   - Create folder: `C:\Users\<YourUsername>\AppData\Roaming\Code\User\prompts`
   - Copy all `.agent.md` files from `jarvis-bundle\agents\` into this folder.

3. **Copy skills**:

   - Create folder: `C:\Users\<YourUsername>\.agents\skills`
   - Copy all folders from `jarvis-bundle\skills\` into this folder.

4. **Copy instructions**:

   - Create folder: `C:\Users\<YourUsername>\AppData\Roaming\Code\User\prompts\instructions`
   - Copy `.instructions.md` files from `jarvis-bundle\instructions\` into this folder.

5. **Copy scripts**:

   - Create folder: `C:\Users\<YourUsername>\AppData\Roaming\Code\User\prompts\scripts`
   - Copy `.py` files from `jarvis-bundle\scripts\` into this folder.

### Step 3: Update Skill File Paths

If you installed to a location different from the default, update the path references in skill folders.

For example, in skill SKILL.md files that reference scripts or configs, update any hardcoded paths to match your installation location.

### Step 4: Verify Installation

1. **Reload VS Code**:
   ```
   Ctrl+Shift+P → Reload Window
   ```

2. **Open Command Palette**:
   ```
   Ctrl+Shift+P → type "@jarvis"
   ```

   You should see all Jarvis agents listed.

### Step 5: Test Jarvis

Open a chat in VS Code and try:

```
@Jarvis test the following file for bugs: [paste a file path]
```

---

## Verify All Components Are Working

After installation, check each component:

### 1. Agents

In VS Code chat, try:

```
@Jarvis-test audit this file: [path]
@Jarvis-develop implement a new feature
@Jarvis-docs write a README
@Jarvis-clearchats clear old chats
```

### 2. Skills

In VS Code chat, try:

```
@Jarvis /caveman mode on
(responds in caveman speech)

@Jarvis /caveman mode off
(resumes normal speech)
```

### 3. Scripts

Open terminal and test:

**macOS:**
```bash
python ~/.config/Code/User/prompts/scripts/ai-switch.py status
python ~/.config/Code/User/prompts/scripts/clear-old-chats.py --dry-run
```

**Windows (PowerShell):**
```powershell
python "C:\Users\<YourUsername>\AppData\Roaming\Code\User\prompts\scripts\ai-switch.py" status
python "C:\Users\<YourUsername>\AppData\Roaming\Code\User\prompts\scripts\clear-old-chats.py" --dry-run
```

---

## Troubleshooting

### Agents Don't Appear

**Issue**: Agents not showing when you type `@jarvis`

**Solution**:
1. Ensure files are in the correct directory
2. Reload VS Code: `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows) → `Reload Window`
3. Verify file extensions are `.agent.md` (not `.md` or `.txt`)

### Scripts Fail to Run

**Issue**: "Python not found" or "Permission denied"

**Solution**:
1. **Verify Python is installed**: 
   ```bash
   python --version  # or python3 --version
   ```
2. **macOS — Make scripts executable**:
   ```bash
   chmod +x ~/.config/Code/User/prompts/scripts/*.py
   ```
3. **Windows — Run Python explicitly**:
   ```powershell
   python "C:\path\to\script.py"
   ```

### Database Locked Error

**Issue**: Script says "database is locked"

**Solution**: Close VS Code completely before running scripts that modify the chat database.

### Import Errors in Scripts

**Issue**: Script fails with "No module named sqlite3"

**Solution**: This shouldn't happen with Python 3.8+. If it does:

**macOS:**
```bash
python3 -m pip install pysqlite3
```

**Windows**:
```powershell
python -m pip install pysqlite3
```

---

## Next Steps

1. Read the [README.md](README.md) for an overview of all agents and skills.
2. Start using Jarvis in your VS Code chat with `@Jarvis` followed by your request.
3. For detailed documentation on each agent, read the corresponding `.agent.md` file.
4. For skill documentation, read each skill's `SKILL.md` file.

---

**Questions?** Check the README.md or the documentation embedded in each agent/skill file.
