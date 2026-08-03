---
title: ORCA Setup 
linktitle: 1 - ORCA Setup 
description: Aquiring dependencies and setting up the repository on your laptop
weight: 100
---
<link rel="stylesheet" href="../style.css">

The following instructions are for Windows devices. There may be different processes for different OS systems. If you find out how to set ORCA up for different devices, feel free to add to this documentation. 

## Creating an SSH key and connecting it to GitHub
We will create an SSH key and connecting it to your GitHub. Connecting to GitHub is technically optional but it is highly recommended. Otherwise, you have to manually type in your SSH key to add it the the Raspberry Pi which is difficult and you have a high chance of a typo. 

{{% alert title="" color="info" %}}
If you've already made an SSH key and connected it to GitHub, you can skip this section. If you have no clue what SSH is and want to learn more, you can read [Basics of SSH](/docs/radar/setupguide/2ORCAsetup/1SSH).
{{% /alert %}}

1. Create an account on [GitHub](https://github.com/) and sign in. 
2. To double check that you dont already have an SSH key, open Git Bash terminal and run `ls -al ~/.ssh`. If you don't already have one, it will say so. If you don't have Git Bash already, download it [here](https://git-scm.com/install/windows)
3. We will create an SSH key now. In the Git Bash terminal, run `ssh-keygen -t ed25519 -C "your-email@example.com"` and accept the default location.
4. Create a password a memoriable and relatively easy to type password. You will input this every time you pull or push code to GitHub from your terminal, every time you SSH to the pi, and every time you transfer files to and from the pi. This happens a lot, so you **may not** want your password to be like `qv34%3bj2!8ncF` and 24 characters long. This however, is entirely up to you as you are the one typing the password. Additionally, please do not make your password as easy as `password`. A new public key file should be made.
5. Run `cat ~/.ssh/id_ed25519.pub` to print out the key to the terminal, and copy it. It starts with "ssh" and ends with your email. You want this whole thing. If you forget the `.pub`, it prints out your private key, which you do not want to give GitHub!! **Do not copy out your private key!**
{{% alert title="" color="info" %}}
If that command doesn't work, and you happen to be in the .ssh directory, you can run `cat id_ed25519.pub`
{{% /alert %}}
6. In GitHub, open settings and go to the SSH and GPG keys tab, and add a new SSH key.
7. Name this whatever you want and paste the key into the correct field. 
{{% alert title="" color="info" %}}
If you need more help with making an SSH key, here is a helpful [GitHub link](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
{{% /alert %}}

## SSH Agent Forwarding
After making your SSH key, you need to add it to your SSH agent on your laptop. First we need the SSH agent to be running. 
1. In powershell run `Get-Service -Name ssh-agent`. 
2. If it says the status is stopped, run `Start-Service ssh-agent`. 
3. Run `Get-Service -Name ssh-agent` again and check it says the status is running.
4. To add your key, run `ssh-add C:/Users/YOUR-NAME/.ssh/id_ed25519`. You will need to insert the secure passphrase you made when you originally made your SSH key. It should say "Identity added". 
5. You can test this by running `ssh -T git@github.com`. It will say that you have been successfully authenticated, but GitHub does not provide shell access . 

## Installing dependencies
**If you are using a Raspberry Pi, you will also want to get miniconda for the Raspberry Pi. This will be done later once the Pi is up and running. You still want to do this section so you can run the code on your laptop when making plots.**

1. Install WSL (Windows Subsystem for Linux)
2. From the Start menu, open **Powershell** and type `wsl --install`.
3. Install [VSCode](https://code.visualstudio.com/download) (or some other code editor of choice).
4. If you're using VSCode, open the Extensions tab and install the following extensions: Python, C/C++, and CMake Tools
5. Within VSCode, open a new Ubuntu (WSL) terminal. 
    1. Open terminal with CTRL + ` . 
    2. On the top right of the terminal section there will be name of the current terminal (likely powershell), plus sign, and a dropdown arrow. 
    3. Hit the dropdown arrow and there will be an (Ubuntu WSL) option.
6. Create a username and password for the Linux system if prompted. This password is used when running Linux commands with administrator permissions (sudo). 
7. You will need the **Linux x86 Miniconda version, NOT WINDOWS** and **do not open** your downloaded .sh file. Download [here](https://www.anaconda.com/download/success). You will need to click the Linux tab to access the correct download files. Save the file in your Downloads folder.
8. In the WSL terminal, change your location to be your Downloads folder.
    1. You can see your current location on the side
    2. Use `cd folder-name` to enter a specific folder
    3. Use `cd ..` to go up a folder 
9. Run `bash Miniconda3-latest-Linux-x86_64.sh` and accept the default options in the installer (select yes when prompted about auto_activate_base, though we will change this later). Accept yes to the liscense terms. It will take time to load. If you hit enter and a new blank line appears, that means it is loading. 
10. After Miniconda has been installed, close and reopen the WSL terminal. Next to the dropdown arrow where you first opened the WSL terminal is a trashcan to close the terminal.  
11. To ensure it has been installed, run `conda list` and you should see a list of the installed dependencies printed out.
12. We are now going to change one of the default settings with the command `conda config --set auto_activate_base false`

## Cloning the Repository
Next we will clone the GitHub repository, so it can be accessed locally.

1. Go to the [ORCA repository](https://github.com/radioglaciology/uhd_radar/tree/main) and click
the green code button and click open with github desktop
2. Click the green **Code** button and within the dropdown go to the **SSH** tab.
3. Copy the repository link which should end in .git
4. In the Git Bash terminal, navigate to whichever folder you would like the code to be copied into (with `cd folder-name` and/or `cd ..`), and run `git clone link_to_repo.git`.
5. In VSCode, you can now open this folder to see all the code

{{% alert title="" color="info" %}}
If you haven't worked with Git before, read the [Basics of Git](/docs/radar/setupguide/2ORCAsetup/2Git) 
{{% /alert %}}

## Setting up Conda

- We now need to use Conda to install the required dependencies for ORCA.
- Before we create the conda environment, check that GCC is installed by running `gcc --version` in the WSL terminal. If the gcc command is not found then install it with `sudo apt update` and `sudo apt install gcc`
- In the WSL terminal, navigate to the folder you just cloned the code to and run `conda env create -f environment-rpi.yaml`
- Once the environment is installed, run `conda activate uhd`
- Run `uhd_images_downloader`
- The code is now installed and ready to run or modified.

{{% pageinfo %}}
Next, [set up your Raspberry Pi](/docs/radar/setupguide/2RaspPi).

{{% /pageinfo %}}