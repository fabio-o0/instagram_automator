import os
from os import listdir
from os.path import isfile, join
from InstagramAPI import InstagramAPI
import json
import boto3

#YOUR INFO
USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

ig = InstagramAPI(USERNAME, PASSWORD)

#AMAZON CLIENT INFO
PHONE_NUMBER = "PHONE_NUMBER"
client = boto3.client('sns', 'us-east-1') #CHANGE THE REGION IF YOU NEED TO

#PATHS
queuePath = "/Scheduler/postsQueue/"
captionsPath = "/Scheduler/captions.json"
photoFolderPath = "/Scheduler/postsQueue/1"

def getCaption(captionsPath):
    #get caption from json
    print("\nGetting caption...\n")
    with open(captionsPath, 'r') as jsonData:
        data = json.load(jsonData)

    captionText = data["1"]
    keys = list(data.keys())

    #update caption indexes
    print("Updating captions...")
    for i in range(len(keys)):
        try:
            data[keys[i]] = data[keys[i + 1]]
            print("Caption " + str((i+1)) + " done...")
        except IndexError as e:
            del data[keys[i]]
            print("Last caption done...")

    #close json
    print("\nClosing json...\n")
    with open(captionsPath, 'w') as jsonData:
        json.dump(data, jsonData)

    return captionText

def renameDirs(photoFolderPath, queuePath):
    #delete uploaded files from dir
    print("Deleting leftover files...")
    for file in os.listdir(photoFolderPath):
        filePath = os.path.join(photoFolderPath, file)
        try:
            if os.path.isfile(filePath):
                print("Deleting " + str(file) + "...")
                os.unlink(filePath)
        except Exception as e:
            print(e)

    #delete dir
    print("\nDeleting leftover directory...\n")
    os.rmdir(photoFolderPath)

    #rename dirs
    print("Updating directories...\n")
    for dir in os.listdir(queuePath):
        try:
            if dir != ".DS_Store":
                os.rename(os.path.join(queuePath,dir), os.path.join(queuePath,str(int(dir) - 1)))
                print(str(dir) + " done...")
        except Exception as e:
            print(e)

def createCarousel(files):
    #sort files
    print("Sorting files...\n")
    files.sort()

    media = []

    #add files to post
    print("Adding files to post...")
    for i in range(len(files)):
        photo = files[i]

        if photo != ".DS_Store":
            media.append(
                {
                    'type': 'photo',
                    'file': photo,
                }
            )
        print("File " + str((i+1)) + "done...")

    return media

def getPhoto(files):
    photo = None
    for file in files:
        if file != ".DS_Store":
            photo = file

    return photo

def getFiles(photoFolderPath):
    #open pictures
    print("Getting files...\n")
    os.chdir(photoFolderPath)
    files = [f for f in listdir(photoFolderPath) if isfile(join(photoFolderPath, f))]
    return files

if len(os.listdir(queuePath)) == 0:
    client.publish(PhoneNumber=PHONE_NUMBER, Message='Instagram Automator: Tried to upload but folder was empty.')
else:
    if len(os.listdir(photoFolderPath)) == 1:
        #log into instagram
        ig.login()

        photo = getPhoto(getFiles(photoFolderPath))
        captionText = getCaption(captionsPath)

        #upload to instagram
        print("Uploading to Instagram...\n")
        ig.uploadPhoto(photo, caption=captionText)

        renameDirs(photoFolderPath, queuePath)

        print("\nSending text message...\n")
        client.publish(PhoneNumber=PHONE_NUMBER, Message='Instagram Automator: Upload successful.')
    else:
        files = getFiles(photoFolderPath)

        #log into instagram
        instagramLogin(USERNAME, PASSWORD)

        media = createCarousel(files)

        captionText = getCaption(captionsPath)

        #upload to instagram
        print("Uploading to Instagram...\n")
        ig.uploadAlbum(media, caption=captionText)

        renameDirs(photoFolderPath, queuePath)

        print("\nSending text message...\n")
        client.publish(PhoneNumber=PHONE_NUMBER, Message='Instagram Automator: Upload successful.')

print("Done!")
