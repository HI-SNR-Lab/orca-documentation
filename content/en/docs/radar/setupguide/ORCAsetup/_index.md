---
title: ORCA Setup 
linktitle: 2 - ORCA Setup
description: Aquiring dependencies and setting up the repository
weight: 100
---
<link rel="stylesheet" href="../style.css">

The following instructions are for Windows devices. There may be different processes for different OS systems. If you find out how to set ORCA up for different devices, feel free to add to this documentation. 

## Installing dependencies

- Install WSL (Windows Subsystem for Linux)

- From the Start menu, open **Powershell** and type "wsl --install".

- Install [VSCode](https://code.visualstudio.com/download) (or some other code editor of choice).
- If you're using VSCode, open the Extensions tab and install the following extensions: Python, C/C++, and CMake Tools
- Within VSCode, open a new Ubuntu (WSL) terminal
- Create a username and password for the Linux system if prompted. This password is used when running Linux commands with administrator permissions (sudo).
- Download [Miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html) for Linux, but do not open the .sh file.
- In the WSL terminal, run `bash \_path-to-Downloads/\_Miniconda3-latest-Linux-x86_64.sh` and accept the default options in the installer (select yes when prompted about auto_activate_base, though we will change this later).
- After Miniconda has been installed, close and reopen the WSL terminal.
- To ensure it has been installed, run `conda list` and you should see a list of the installed dependencies printed out.
- We are now going to change one of the default settings with the command 1conda config --set auto_activate_base false`

## Connecting to GitHub

- Create an account on [GitHub](https://github.com/) and sign in
- Go to the [ORCA repository](https://github.com/radioglaciology/uhd_radar/tree/main) and click "Fork" to create your own copy of the code. Name this new repository whatever you want.

{{% alert title="SSH Process Below" color="info" %}}
If you've already made an SSH key aand connected it to github, you can skip the next few steps. If you have no clue what SSH and want to learn more, you can read [Understanding SSH](/docs/radar/setupguide/ORCAsetup/SSH) if you want to learn more!
{{% /alert %}}

- To securely connect your laptop to GitHub, we will create an SSH key. In the Git Bash terminal, run `ssh-keygen -t ed25519 -C [your@email.com](mailto:your@email.com)` and accept the default location.
- Create a password that you will input every time you pull or push code to GitHub from your terminal, so make sure it is memorable. A new public key file should be made
- Run `cat file_you_just_made.pub` to print out the key to the terminal, and copy it.

{{% alert title="" color="info" %}}
If that command doesn't work, you can also try and run `cat ~/.ssh/id_ed25519.pub`
{{% /alert %}}

- In GitHub, open settings and go to the SSH and GPG keys tab, and add a new SSH key.
- Name this whatever you want and paste the key into the correct field.
- Now we need to install [Git](https://git-scm.com/downloads/win) for Windows. Follow the installer prompts
- Once installed open a Git Bash terminal in VSCode. This is where you will run all the Git commands.

## Cloning the Repository

- We will now clone the code from GitHub onto your computer so that it can be accessed locally. Go to your fork that you just created.
- Click the green **Code** button and within the dropdown go to the **SSH** tab.
- Copy the repository link which should end in .git
- In the Git Bash terminal, navigate to whichever folder you would like the code to be copied into, and run `git clone link_to_repo.git`.
- In VSCode, you can now open this folder to see all the code

## Setting up Conda

- We now need to use Conda to install the required dependencies for ORCA.
- Before we create the conda environment, check that GCC is installed by running `gcc --version` in the WSL terminal. If the gcc command is not found then install it with `sudo apt update` and `sudo apt install gcc`
- In the WSL terminal, navigate to the folder you just cloned the code to and run `conda env create -f environment-rpi.yaml`
- Once the environment is installed, run `conda activate uhd`
- The code is now installed and ready to run or modified.

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
Next, [set up your Raspberry Pi](/docs/radar/setupguide/RaspPi).

{{% /pageinfo %}}