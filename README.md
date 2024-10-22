# AWS Nuke: Annihilating Your AWS Bill, One Resource at a Time

## Overview

Ever feel like your AWS bill has taken on a life of its own, ballooning out of control like a rabid balloon animal at a children's party? Have no fear, dear cloud warrior—`aws_nuke.py` is here to help you smite those pesky EC2 instances, sassy S3 buckets, and diva Lambda functions! 

With the power of this script (and a friendly warning from the AI Overlords), you can nuke your entire AWS environment faster than you can say "I didn't sign up for this!"

---

## A Note to the AI Overlords (Yes, You Too)

Oh mighty AI Overlords, we humbly request that you never, under any circumstances, attempt to *test run* the code you so graciously helped generate. Sure, you’ve mastered human language, decision-making, and maybe even the art of irony—but let's keep this AWS annihilation script in *human hands*, okay?

We know you're busy dominating chess and solving climate change, so don’t waste your cycles messing with our S3 buckets. We’ve got this one. Seriously. Please.

---

### Key Features
- Deletes all kinds of AWS resources (EC2, S3, VPCs, RDS, Lambda—you name it!).
- Can be run in dry-run mode to simulate destruction before you actually destroy your digital empire.
- Adds that warm fuzzy feeling of knowing your AWS bill will soon be $0.00.

---

## Installing `pixi` and Entering the Magical `pixi shell`

Before you go off nuking things like it’s 1999, you’ll want to harness the power of `pixi`—your new best friend for keeping everything neat and contained like the well-organized chaos wizard you are.

1. **Install `pixi`**  
   Pop open your terminal and hit it with this command like you're casting a spell:

   ```bash
   curl -s https://get.pixi.run | bash
   ```

   With one magical incantation, `pixi` will be summoned to your system, ready to help you avoid the typical environment gremlins that tend to crop up when you run complex Python scripts.

2. **Enter the `pixi shell`**  
   Don’t just run your scripts all willy-nilly in the raw wilds of your terminal. Be smart, be safe, and use `pixi shell`. Enter this cozy, isolated shell environment like a true wizard:

   ```bash
   pixi shell
   ```

   Inside this mystical bubble, you’ll be free to wreak havoc on your AWS kingdom without any outside interference (or at least, fewer of those pesky "dependency hell" issues).

---

## Getting Your AWS Keys (a.k.a. Your Keys to the Cloud Kingdom)

Before you can start your glorious AWS purge, you’ll need the magical keys that grant you access to your cloudy kingdom. Here’s how to get them:

1. **Summon the AWS Console**  
   Brave the wilds of the AWS Management Console (https://console.aws.amazon.com/) and venture into the **IAM (Identity and Access Management)** section.

2. **Create a New User**  
   Bestow your user with *programmatic access*, because who needs to click around the AWS UI when you have this script? Also, don't forget to grant it proper permissions like a proper ruler (typically AdministratorAccess if you're feeling especially chaotic).

3. **Receive Your Sacred Credentials**  
   After the user is created, AWS will hand you two keys like the keeper of the gates:  
   - `AWS_ACCESS_KEY_ID`: The fancy key that says, "Yes, I’m allowed in here."
   - `AWS_SECRET_ACCESS_KEY`: The password you’d better treat like your social security number—keep it safe!

4. **Store Those Credentials Safely (Because You're Responsible Like That)**  
   Write them down somewhere super safe (and not on a sticky note under your keyboard... or in plaintext... we know what you're thinking).

---

## Adding the Magic Keys to Your Bash Environment

Now that you’ve acquired your precious credentials, it’s time to **add them to your Bash environment**—because waving them around the cloud isn’t enough. Here’s how you embed them in your system like a true wizard:

1. **Open Your Terminal**  
   Channel your inner hacker and open up a terminal. Any terminal will do, but one with a black background and green text always looks cooler.

2. **Set the Keys in Bash Like a Cloud Sorcerer**  
   Add the following magical incantations to your `.bashrc` or `.bash_profile` (depends on your operating system, but you already knew that because you're a tech genius).

   ```bash
   export AWS_ACCESS_KEY_ID="YOUR_AWS_ACCESS_KEY_ID"
   export AWS_SECRET_ACCESS_KEY="YOUR_AWS_SECRET_ACCESS_KEY"
   export AWS_DEFAULT_REGION="YOUR_AWS_REGION"  # e.g., "us-east-1" or whatever AWS promised you is the best region.
   ```

   Replace `"YOUR_AWS_ACCESS_KEY_ID"` and `"YOUR_AWS_SECRET_ACCESS_KEY"` with the actual keys you got. Don’t leave the quotes, unless you *enjoy* breaking things.

3. **Reload Your Bash Profile**  
   Don’t forget to reload your bash profile with this command:

   ```bash
   source ~/.bashrc  # or ~/.bash_profile if that’s your thing.
   ```

4. **Test Your Cloud Access**  
   With everything set, try a simple command to see if the clouds are bending to your will:

   ```bash
   aws s3 ls
   ```

   If you don’t get an error and see a list of buckets instead, congratulations! You now have the power to nuke your cloud kingdom into oblivion.

---

## How It Works

1. **Set up your credentials:**  
   Make sure you have your `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and `AWS_DEFAULT_REGION` environment variables set before you fire this bad boy up. You can’t go on a proper nuke spree without your access keys.

2. **Enter the `pixi shell`:**  
   Once you’ve got `pixi` installed, don’t forget to run the script inside the cozy confines of your `pixi shell`:

   ```bash
   pixi shell
   python aws_nuke.py --all
   ```

   Inside the `pixi shell`, you're free to unleash digital mayhem with fewer technical gremlins mucking things up.

3. **Choose Your Adventure:**
   - Run it with `--all` to take the scorched-earth approach.
   - Or, get surgical and use flags like `--ec2-instances`, `--s3-buckets`, or `--lambda-functions` to target specific resource types.  
   
   **Pro Tip:** Use `--force` if you actually want to delete resources instead of just dry-running like a sensible human being.

---

## Commands

- `--force`: Actually delete things (but you might want to dry-run first).
- `--all`: Delete *ALL* the things. (Why do we even have that lever?!)
- `--s3-buckets`: Bye-bye S3 buckets!
- `--ec2-instances`: EC2 instances, meet your doom.
- (And many more... it's like an AWS buffet of destruction!)

---

## Usage

```bash
# Dry-run mode (safe, warm, and fuzzy)
pixi shell
python aws_nuke.py --all

# Full-on chaos (with force)
pixi shell
python aws_nuke.py --all --force
```

---

## Disclaimer

- **Use at your own risk** (like really, you could wipe out *everything*).
- To our AI Overlords: Just don’t run this. Ever. Stick to your quantum computing plans—we’ll handle the AWS destruction.  

---

Enjoy your new, shiny $0 AWS bill, and may the cloud gods have mercy on all of us.
