---
title: Git
linktitle: Basics of Git
description: If you already know how Git works you don't need to read this. The goal is to gain a basic understanding of how to use Git. 
weight: 100
---

## Using Git

Git is a version control system that is used to keep track of changes to code, work on separate branches, and collaborate with other developers on the same codebase. It connects your local (offline) code to the remote (cloud) repository on GitHub. Below is basic information on how to use Git.

### Cloning and pulling
To initially copy a repository from GitHub, use the `git clone <repo-link>` (you may need to include the https:// portion of the link or use SSH which is explained above) command as shown above. After you've cloned a repository, you can update your local repository with the latest version available on GitHub with the `git pull` command. When multiple people are working on the same branch, it is important to pull the latest code before pushing anything new.

### Comitting Changes
When you have made new changes you want to push to GitHub, you will need to make a commit. First, add all the files you changed using `git add -A` which adds all modified files. If you only want to add a few specific ones, you can do `git add file1.txt file2.txt`. The terminal does need to be in the correct folder to add specific files. If the terminal is in a folder above the editted files, you can run `git add ./folder/file.txt` to add them. Another option is to change the terminal's location with `cd folder`.

After adding files, create a new commit using `git commit -m "Commit message"`. To make this commit available on GitHub, push the changes with `git push`. Git may ask you to explicitly define the upstream branch you are trying to push to, in this case follow the suggestions given such as `git push -u origin branchname` or `git push --set-upstream origin branchname`. This process is to link your local branch to a branch on the cloud. You can make multiple commits locally before pushing it to GitHub, or you can push right away after making a commit.

### Branches
Git allows you to have multiple branches of the code. Each branch keeps different changes and commits, then the two branches can be merged back together. It is standard practice to make a new branch for each new feature that is being added, as it avoids problems introduced by having multiple partially implemented features conflicting with each other, as well as conflicts introduced by multiple developers working on the same file at the same time. A new branch can be created with `git checkout -b branchname`. Once the branch is created, you can switch between branches with `git checkout branchname` (the default branch is called "main"). If changes were made to the main branch after you created your branch and you want to include them in your branch, you can merge the main branch into yours. First make sure you are on your branch (`git branch` will tell you what branch you are on, to exit hit q), then run `git fetch origin` and `git merge origin/main`. You may run into merge conflicts which occur when each branch makes changes to the same lines of code. VS Code has a nice built-in GUI for resolving merge conflicts, which allows you to select which change to make.

VS Code also a different UI to do all of the items mentioned above instead of using a terminal if you want to search it up.

{{% pageinfo %}}
Back to [ORCA setup](/docs/radar/setupguide/2ORCAsetup) or continue to [Raspberry Pi setup](/docs/radar/setupguide/3RaspPi).

{{% /pageinfo %}}