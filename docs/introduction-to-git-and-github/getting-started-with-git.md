# Getting Started with Git

#### 1. Install Git

First, you need to install Git on your computer. You can download it from the [official Git website](https://git-scm.com/).

#### 2. Configure Git

After installation, configure your Git settings:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### 3. Initialize a Repository

Navigate to your project directory and initialize a Git repository:

```bash
cd your-project-directory
git init
```

#### 4. Add Files to the Repository

Add files to your repository to start tracking them:

```bash
git add .
```

#### 5. Commit Changes

Commit your changes with a message describing what you've done:

```bash
git commit -m "Initial commit"
```

#### 6. Connect to a Remote Repository

If you want to push your code to a remote repository (e.g., GitHub), you need to add the remote URL:

```bash
git remote add origin https://github.com/yourusername/your-repo.git
```

#### 7. Push Changes to the Remote Repository

Push your changes to the remote repository:

```bash
git push -u origin master
```

#### 8. Pull Changes from the Remote Repository

To update your local repository with changes from the remote repository:

```bash
git pull origin master
```

#### 9. Branching and Merging

Create a new branch to work on a feature:

```bash
git checkout -b new-feature
```

After making changes, commit them and switch back to the main branch:

```bash
git commit -m "Add new feature"
git checkout master
```

Merge the new feature branch into the main branch:

```bash
git merge new-feature
```

#### 10. Viewing the Commit History

To see the commit history of your project:

```bash
git log
```

This guide covers the basics to get you started with Git. If you need more detailed information, you can refer to the [Git documentation](https://git-scm.com/doc) or the [GitHub Docs](https://docs.github.com/en/get-started/getting-started-with-git).
