# 📤 GitHub Upload Guide for ILPG Project

## Step-by-Step Instructions

### Prerequisites
- GitHub account (create one at https://github.com if you don't have one)
- Git installed on your computer (check with `git --version`)

---

## 🚀 Quick Start (Automated)

I'll help you initialize the repository. Then you'll need to:
1. Create a repository on GitHub
2. Connect it to your local repository
3. Push your code

---

## 📋 Manual Steps

### Step 1: Initialize Git Repository
```bash
git init
```

### Step 2: Add All Files
```bash
git add .
```

### Step 3: Create Initial Commit
```bash
git commit -m "Initial commit: ILPG Adaptive Learning Platform"
```

### Step 4: Create Repository on GitHub
1. Go to https://github.com/new
2. Repository name: `ILPG` (or your preferred name)
3. Description: "Intelligent Learning Pathway Generator - Adaptive Learning Platform"
4. Choose **Public** or **Private**
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click **"Create repository"**

### Step 5: Connect Local Repository to GitHub
After creating the repo, GitHub will show you commands. Use these:

```bash
# Replace YOUR_USERNAME with your GitHub username
git remote add origin https://github.com/YOUR_USERNAME/ILPG.git
git branch -M main
git push -u origin main
```

---

## 🔐 Alternative: Using SSH (Recommended for frequent pushes)

If you have SSH keys set up:

```bash
git remote add origin git@github.com:YOUR_USERNAME/ILPG.git
git branch -M main
git push -u origin main
```

---

## ✅ What Gets Uploaded?

### ✅ Will be uploaded:
- All source code (frontend & backend)
- Documentation files
- Configuration files (package.json, requirements.txt)
- Example files
- README.md

### ❌ Will NOT be uploaded (protected by .gitignore):
- `node_modules/` (frontend dependencies)
- `venv/` (Python virtual environment)
- `.env` files (sensitive credentials)
- `__pycache__/` (Python cache)
- IDE settings
- Log files

---

## 🔒 Security Checklist

Before pushing, make sure:

1. ✅ No `.env` files are committed (check with `git status`)
2. ✅ No API keys or passwords in code
3. ✅ MongoDB connection strings are in `.env` (not in code)
4. ✅ JWT secrets are in environment variables

---

## 📝 Recommended: Create .env.example

Create a template file for environment variables:

**backend/.env.example:**
```env
MONGODB_URI=mongodb://localhost:27017/ilpg
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
```

This helps other developers know what environment variables they need.

---

## 🎯 Next Steps After Upload

1. **Add a README.md** (if not already good) with:
   - Project description
   - Installation instructions
   - How to run the project
   - Features list

2. **Add a LICENSE** file (if needed)

3. **Set up GitHub Actions** (optional) for CI/CD

4. **Add collaborators** (if it's a group project)

---

## 🆘 Troubleshooting

### Error: "remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/ILPG.git
```

### Error: "failed to push some refs"
```bash
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Forgot to add .gitignore?
```bash
# Remove already tracked files
git rm -r --cached node_modules/
git rm -r --cached venv/
git commit -m "Remove ignored files"
```

---

## 📚 Useful Git Commands

```bash
# Check status
git status

# See what files will be committed
git status --short

# View commit history
git log

# Create a new branch
git branch feature-name

# Switch branches
git checkout feature-name

# Push to GitHub
git push origin main

# Pull latest changes
git pull origin main
```

---

## 🎉 You're Done!

Once pushed, your code will be available at:
`https://github.com/YOUR_USERNAME/ILPG`

Share this link with your team members!

