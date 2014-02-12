from instagram.client import InstagramAPI
import redis
import simplejson 
import requests
import re
import matplotlib.pyplot as plt
import networkx as nx
import community

#KEYWORD = input("What hashtag do you want to explore? ")    ### can make this an input variable to searh whichever #
ACCESS_TOKEN="10710681.1fb234f.5d89698eb4854a47825eeaf4842dacae"
#r = requests.get("https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s" % (KEYWORD, ACCESS_TOKEN))
#data=simplejson.loads(r.read())
api=InstagramAPI(access_token=ACCESS_TOKEN)
#This returns media ids for the photos that are tagged
tagged=api.tag_recent_media(count=20,tag_name="bystrothetortoise")
#tagged is a tuple
#media is the list in tuple index 0
media=str(tagged)
#generates a list of mediaIDs
mediaID=re.findall(r'Media: (\d+_\d+)',media)
#each is each picture posted

#usernames empty list to store regex results in from comments and likes
usernames=[]
comments=""
likes=""
print "im about to start the loop of putting users into a list"
for each in mediaID:
    comments=comments+str(api.media_comments(media_id=each))
    likes=likes+str(api.media_likes(media_id=each))

comments=comments.replace(",","")
likes=likes.replace(",","")
likes=likes.replace("["," ")
likes=likes.replace("]"," ")

usrComm=re.findall(r'Comment: (\S+)',comments)
usrLike=re.findall(r'\[?User: (\S+)', likes)
###you can use REDIS SINTER HERE
print "im gonna now add commenters/likers to the list"
for each in usrComm:
    if each not in usernames:
        usernames.append(each)
for each in usrLike:
    if each not in usernames:
        usernames.append(each)
print "now i'm entering get the id loop"
#get user ids in order to run more api calls
listID=[]
for each in usernames:
    #put each in quotes to use in api call
    '"{}"'.format(each)
    #find its user_id
    userid=requests.get("https://api.instagram.com/v1/users/search?q=%s&access_token=%s" % (each, ACCESS_TOKEN))
    #convert to text
    dataid=userid.text
    #dataid is a unicode value
    ##with below code, dataA contains usernames and ids for every username including the searched word (so gonzoa returns gonzoana gonzoangeles....)
    dataA=dataid.encode('ascii','ignore')
    #extract the id and make it new dataid
    listID.append(re.findall(r'id":"(.*?)"',dataA)[0])
#print listID

#make dict. key:value; id:followers/follwing
#or use Redis?
#get the data:::get follows for each user, get followed by for each 
red=redis.Redis()

##gotta listify the strings
print "now i'm at the redis part"
for each in listID:
    idInt=int(each)
    follows=api.user_follows(user_id=idInt) #returns a list
    followedBy=api.user_followed_by(user_id=idInt) #returns a list of ids
    ####now get rid of dups aka intersect
    connectList=red.sinterstore('connections', follows, followedBy)
    print connectList








#exexexex
#f = open('output.json', 'w')
#f.write(dumps(json_obj, indent=4))
#f.close()





#for each in json:
    



#translates KEYWORD restults with GET function into text
