# Importing all important libraries
from bz2 import BZ2File as bzopen
from collections import defaultdict
import xml.etree.ElementTree as ET
import string
import bz2
import re
import requests
import json
import random

# Important
# Change the following file names as required
# The file from where You want to read the graph from
graph_store_file = 'demo.txt'
# The bz2 file from where you read data
dump_file = 'test.bz2'
# File where you want to store the random walk process
result_publish_file = 'demo_result.txt'

def dump_to_text():
    # tags represent the starting and ending of a page on wikipedia in xml format
    tag1='<page>'
    tag2='</page>'
    # page_title stores the title of all pages we encounter in the dump
    page_title=[]
    # ct represents the number of pages we have already traversed
    ct=0

    # Resetting the file in which we will store the graph
    f=open(graph_store_file, 'w',encoding='utf-8')
    print('')
    f.close()

    print('-----Reading data from wikidump page by page-----')

    # reading a bz2 archive page by page
    with bzopen(dump_file, "r") as bzfin:
        for i, line1 in enumerate(bzfin):
            line1=line1.decode()
            line1=line1.rstrip()
            # page will store the entire text in a wikipage
            page=''
            # links will store all the links present in the wikipage taken
            links=[]
            j=0
            # We check line by line if tag1 is present
            # If yes, then my page starts from that line
            if tag1 in line1:
                page+=line1
                j=i+1
                # With this for loop we continue to store data in the 
                # page variable till we find tag2 representing end of that page
                for j,line2 in enumerate(bzfin):
                    line2=line2.decode()
                    line2=line2.rstrip()
                    if tag2 in line2:
                        page+=tag2
                        break
                    page+=line2
                ct+=1
                if(ct%5000==0): print('Progress: ',ct, 'pages read...')
                # Finding title of each page by converting string to xml
                # Then processing it using xml ElementTree
                root = ET.fromstring(page)
                name=str(root[0].text)
                page_title.append(name)
                # Using Regular Expression to find all the links stored (present within [[]])
                res1 = re.findall(r'\[.*?\]', page)
                # Filtering the list as it might also contain empty lists
                res2 = list(filter(None, res1))
                links=[]
                # Filtering Links that contain ':' and '.' as they might not be legit
                c=':'
                d='.'
                for link in res2:
                    if c in link or d in link:
                        continue
                    else:
                        links.append(link)
                # Removing square brackets from the links stored
                for t in range(len(links)):
                    s=links[t]
                    s=s.replace('[','')
                    s=s.replace(']','')
                    links[t]=s
                # One of the most common useless link is shown below (found by observation)
                # Removing it from our list of links
                x='Project:AWB|AWB'
                if x in links:
                    links.remove(x)
                # Removing the substring from each link which starts from '|'
                # as it represents alternate name while we require only one
                for t in range(len(links)):
                    ch='|'
                    s=links[t]
                    if ch in s:
                        q=s.rfind(ch)
                        s=s[0:q]
                        links[t]=s
                # Writing the adjacency list in form of a text file while each line represents a single page
                # Each line contains page title followed by links contained in it separated by #
                f=open(graph_store_file, 'a',encoding='utf-8')
                f.write(name)
                for link in links:
                    f.write('#')
                    f.write(link)
                f.write('\n')
            i=j+1
    print('BZ2 file read and stored. Exiting...')
    # Closing the files
    f.close()
    bzfin.close()

def text_to_graph_to_random_walk(disp):
    # To store adjacency list in form of index assigned to each node
    graphs_with_num={}
    # To store page titles of every page in form of index
    page_title_num=[]
    # To keep count of pages read while executing 
    ct=0
    # mp1 stores index corresponding to name of each node
    mp1={}
    # mp2 stores name corresponding to index of each node
    mp2={}
    # To assign indices to each title name and link
    count=0

    # Reading number of pages in the given file
    f = open(graph_store_file,'r',encoding='utf-8')
    total=0
    print('---Please wait for 1-2 min---')
    for line in f:
        total+=1
    f.close()
    print('Total Number of pages : ',total)
    print('Reading Adjacency list and making graph')

    # Opening the text file containing the adjacency list
    with open(graph_store_file, "r",encoding="utf-8") as f:
        # Reading each line as a single line represents a single page
        for line in f:
            ct+=1
            if(ct%1000000==0): print('Pages read: ',ct,' Progress: ',(ct/total)*100,'%')
            newline=line.strip()
            # Spliting each line read at '#' as we did to store it in the first place
            ndes=newline.split('#')
            # Title of the page is represented by the first element in the list
            title=ndes[0]
            # Assigning index to title and storing in the map
            if title not in mp1:
                mp1[title]=count
                mp2[count]=title
                count+=1
            page_title_num.append(mp1[title])
            ndes.remove(title)
            # Now all other elements except first in the list represent the links present
            # Storing them in nodes
            nodes=[]
            # After assigning index to each link storing in nodes_with_num
            nodes_with_num=[]
            # Filtering the nodes of the empty list 
            for nd in ndes:
                if(nd!=''):
                    nodes.append(nd)
            # Assigning indices to each link in the page and storing in the nodes_with_num
            for node in nodes:
                if node not in mp1:
                    mp1[node]=count
                    mp2[count]=node
                    count+=1
                nodes_with_num.append(mp1[node])
            # Storing the data in a dictionary in adjacency list
            graphs_with_num[mp1[title]]=nodes_with_num
    print('---Graph Made---')
    f.close()

    print('---Now Performing Random Walk---')
    # Now Performing the Random Walk
    # Storing all the keys of adjacency list in keys
    keys=list(graphs_with_num.keys())
    source=random.choice(keys)
    # Storing frequency of each node visited in freq
    freq=defaultdict(int)
    freq[source]+=1
    itr=1
    # Running random walk for 10000000 iterations
    while(itr<10000000):
        r = False
        value =  graphs_with_num.get(source)
        # Adding condition for teleportation
        tp=0
        if(random.random()<0.15):tp=1
        if(tp==0):
            if (value==None or len(list(graphs_with_num[source]))==0):
                r = True
            if(r == False):
                new=random.choice(list(graphs_with_num[source]))
            else:
                new=random.choice(keys)
        else:
            new=random.choice(keys)
        freq[new]+=1
        source=new
        itr+=1
        if itr%100000==0:
            print('Progress: ',(itr/10000000)*100,'%')
    print('---Random Walk Done---')

    # Printing top 100 sorted list of frequency of nodes visited
    def keyfunction(k):
        return freq[k]

    g=open(result_publish_file,'w',encoding='utf-8')
    for key in sorted(freq, key=keyfunction, reverse=True)[:disp]:
        g.write(mp2[key])
        g.write(' : ')
        g.write(str(freq[key]))
        g.write('\n')
        print("%s: %i" % (mp2[key], freq[key]))
    g.close()
    print('Number of links we visited are :',len(freq.keys()))

def main():
    choice=0
    print('---Important---')
    print('To Read and make Graph from full wikidump will take approx 3-4 hours!!!')
    print('Kindly use already stored graph as adjacency list provided in the drive link')
    print('---')
    print('To read BZ2 file and store adjacency list, Press 1')
    print('To read data from already stored graph and perform random walk, Press 2')
    choice = int(input())
    if(choice == 1):
        disp=0
        print('Specify top number of pages to be displayed : ')
        disp = int(input())
        dump_to_text()
        text_to_graph_to_random_walk(disp)
    elif(choice == 2):
        print('Specify top number of pages to be displayed : ')
        disp = int(input())
        text_to_graph_to_random_walk(disp)
    else:
        print('Invalid Choice')

main()