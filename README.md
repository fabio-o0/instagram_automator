# instagram_automator
Automatic posts to Instagram

This script allows you to post to Instagram. Used in conjunction with pythonanywhere.com or a similar service, it can be used as a scheduler. I explain it in depth in this YouTube video: LINK TO VIDEO


## How to Use
### STEP 1
Download **Complete.zip**

### STEP 2
Go to https://www.pythonanywhere.com and make an account. Upload **Complete.zip** to your home directory.

### STEP 3
In https://www.pythonanywhere.com, unzip **Complete.zip** using the Consoles tab. (Open a bash console and type in this command:
```
unzip Complete.zip
```

### STEP 4
With the console still open, install all dependencies:
```
pip3 install InstagramApi --user
pip3 install boto3 --user
pip3 install awscli --upgrade --user
```
For further info on these:
https://github.com/LevPasha/Instagram-API-python
https://docs.aws.amazon.com/cli/latest/userguide/install-linux.html

### STEP 5
Head over to https://aws.amazon.com/ and create an account. Once logged in search for **IAM** in the services. Click on the **Users** tab and create a new user. Get to the credentials screen. You will have two keys, one public access key, one private secret key, you will use these in step 6.

### STEP 6
With your Amazon codes open, go back to the https://www.pythonanywhere.com console and set up Amazon Web Services:
```
aws configure
```
It will ask you for the two numbers and a region. Your region can be found in the same place where you found **Users**. Under the **Account settings** tab. If it asks you for anything else just leave it blank (hit enter).

### STEP 7
Open **instagram_automator.py** on https://www.pythonanywhere.com and input your info (Instagram username, passowrd, phone number). Save the file.

### STEP 8
You're done. Now you just need to upload whatever you want to post. Here's how you do it. Get your image(s) and put it(them) in a folder called "1" or whatever number of scheduled posts you have (if you've scheduled 3 posts, you would call it "4", for example). Compress that folder (zip it). Upload the zip file to **postsQueue** in the Scheduler folder on https://www.pythonanywhere.com. Unzip it using the console as previously. Delete the zip file and any other files that might've snuck in ("\_MACOSX/", for example). Type in your caption in the **captions.json** file in a similar fashion: Whatever index you're on and the caption (
```
{
  "1":"this is a caption"
}
```
). If you have multiple captions, make sure to separate them by commas.

### STEP 9
Thank you. Share with your friends. Live life. Be happy, idk, do you boo.
