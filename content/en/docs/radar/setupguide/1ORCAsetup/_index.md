---
title: ORCA Setup 
linktitle: 1 - ORCA Setup
description: Aquiring dependencies and setting up the repository
weight: 100
---
<link rel="stylesheet" href="../style.css">

The following instructions are for Windows devices. There may be different processes for different OS systems. If you find out how to set ORCA up for different devices, feel free to add to this documentation. 



## Installing dependencies
**If you are using a Raspberry Pi, you will want to get miniconda for the Raspberry Pi. This will be done later after SSH is set up. You can skip this section and go to Connecting to GitHub**

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
- Go to the [ORCA repository](https://github.com/radioglaciology/uhd_radar/tree/main) and click "Branch" to create your own copy of the code. Name this new repository whatever you want.

{{% alert title="" color="info" %}}
If you've already made an SSH key aand connected it to github, you can skip the next few steps. If you have no clue what SSH and want to learn more, you can read [Basics of SSH](/docs/radar/setupguide/2ORCAsetup/1SSH).
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

{{% alert title="" color="info" %}}
If you need more help with making an SSH key, here is a helpful [GitHub link](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
{{% /alert %}}

## SSH Agent Forwarding
After making your SSH key, you need to add it to your SSH agent on your lapotp. First we need the SSH agent to be running. In powershell run `Get-Service -Name ssh-agent`. If it says the status is stopped, run `Start-Service ssh-agent`. Then run `Get-Service -Name ssh-agent` again and check it says the status is running.

Now to add your key, run `ssh-add C:/Users/YOU/.ssh/id_ed25519`. You will need to insert the secure passphrase you made when you originally made your SSH key. The key should now be added. You can test this by running `ssh -T git@github.com`.
## Cloning the Repository

- We will now clone the code from GitHub onto your computer so that it can be accessed locally. Go to your fork that you just created.
- Click the green **Code** button and within the dropdown go to the **SSH** tab.
- Copy the repository link which should end in .git
- In the Git Bash terminal, navigate to whichever folder you would like the code to be copied into, and run `git clone link_to_repo.git`.
- In VSCode, you can now open this folder to see all the code

{{% alert title="" color="info" %}}
If you haven't worked with Git before, read the [Basics of Git](/docs/radar/setupguide/2ORCAsetup/2Git) 
{{% /alert %}}

## Setting up Conda

- We now need to use Conda to install the required dependencies for ORCA.
- Before we create the conda environment, check that GCC is installed by running `gcc --version` in the WSL terminal. If the gcc command is not found then install it with `sudo apt update` and `sudo apt install gcc`
- In the WSL terminal, navigate to the folder you just cloned the code to and run `conda env create -f environment-rpi.yaml`
- Once the environment is installed, run `conda activate uhd`
- The code is now installed and ready to run or modified.

{{% pageinfo %}}
Next, [set up your Raspberry Pi](/docs/radar/setupguide/3RaspPi).

{{% /pageinfo %}}