import matplotlib.pyplot as plt
import networkx as nx
import community
import requests
import re

KEYWORD = ""
KEYWORD = input("What hashtag do you want to explore? ")    ### can make this an input variable to searh whichever #
ACCESS_TOKEN="10710681.1fb234f.5d89698eb4854a47825eeaf4842dacae"
tags = requests.get("https://api.instagram.com/v1/tags/%s/media/recent?access_token=%s" % (KEYWORD, ACCESS_TOKEN)) 

#translates KEYWORD restults with GET function into text
dataT=tags.text                                             

#In the text, finds everything in between username":" and " which = USERNAME!!
#Puts each username into listNames
listNames=re.findall(r'username":"(.*?)"', dataT)          

follows = requests.get("https://api.instagram.com/v1/users/%s/follows?access_token=%s" % (UID, ACCESS_TOKEN))


G=nx.erdos_renyi_graph(30, 0.05)
#computing the best partition
partition = community.best_partition(G)

size=float(len(set(partition.values())))
pos=nx.spring_layout(G)
count = 0.
for com in set (partition.values()):
    count = count + 1.
    list_nodes = [nodes for nodes in partition.keys()
                                  if partition[nodes]==com]
    nx.draw_networkx_nodes(G,pos,list_nodes,node_size = 20,node_color=str(count/size))

nx.draw_networkx_edges(G,pos,alpha=0.5)
plt.show()







#create graph
G=nx.Graph()     
###print(listNames)

#fill dictNames dictionary with usernames and corresponding user ids
dictNames={}
for each in listNames:
    #add a node for each user
    G.add_node(each)
    userid=requests.get("https://api.instagram.com/v1/users/search?q=%s&access_token=%s" % (each, ACCESS_TOKEN))
    dataid=userid.text
    ###print(dataid)
    #find the id, put it with key in dict
    listId=re.findall(r'id":"(.*?)"',dataid) 
    dictNames[each]=listId
###print(dictNames)

#draw all nodes in the spring layout
nx.draw_networkx_nodes(G,nx.spring_layout(G))
plt.show()


#########################################
#makes nodes for each in the dictionary
#run api for each, only pay attention to those in the dict., record edges

#For each value in dictNames, run API to see following, create nodes during
