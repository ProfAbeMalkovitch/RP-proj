# GitHub Upload Commands

## Quick Upload Commands

```powershell
# 1. Initialize Git repository
git init

# 2. Add remote repository
git remote add origin https://github.com/Arshadofficial/RP-proj.git

# 3. Add all files
git add .

# 4. Commit files
git commit -m "Initial commit: ILPG project"

# 5. Set branch to main (if needed)
git branch -M main

# 6. Push to GitHub
git push -u origin main
```

## If you need to push to L_patgway folder:

```powershell
# Option 1: Clone first, then copy files
git clone https://github.com/Arshadofficial/RP-proj.git
cd RP-proj
# Copy your ILPG files to L_patgway folder
# Then commit and push

# Option 2: Push directly (files will be in root, you can organize later)
git init
git remote add origin https://github.com/Arshadofficial/RP-proj.git
git add .
git commit -m "Add ILPG project"
git branch -M main
git push -u origin main
```

