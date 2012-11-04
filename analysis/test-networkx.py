"""
Recreated on September 25, 2012
Another version of data analysis.
@author: kat-drexel
"""


"""
This script takes raw data files, processed into tables and text files.
"""

"""
Notes: Relationship is defined as 2 people in the following samples:
* IN FORUM, who participate in same thread,
* IN JOURNAL, who participate in same journal entry,
* IN NOTES, where X receive from Y.
"""

#============================================================
import re
import numpy
import datetime 
import networkx

class DataTables (object):
    def __init__(self, TblFP=None, TblFC=None, TblJP=None, TblN=None):
        self.TblFP = TblFP #[['urlID', 'creator', 'commenters', '#comments']]
        self.TblFC = TblFC #[]
        self.TblJP = TblJP
        self.TblN = TblN
             
    def set_TblFP (self, Tbl):
        self._TblFP = Tbl     
    
    def get_TblFP (self):
        return self._TblFP
    
    def set_TblFC (self, Tbl):
        self._TblFC = Tbl     
    
    def get_TblFC (self):
        return self._TblFC

    def set_TblJP (self, Tbl):
        self._TblJ = Tbl     
    
    def get_TblJP (self):
        return self._TblJ
    
    def set_TblN (self, Tbl):
        self._TblFN = Tbl     
    
    def get_TblN (self):
        return self._TblFN 
    
class Prepare (object): 
    global Everyone
    global Members
    Everyone = {}
    Members = {} 

    def pair(self, num, handle, pair):
        if num not in pair.keys(): pair[num]=handle
        return pair

    def PrintAllUsers(self, filename): 
#        Try putting global Everyone[] list into a dictionary
#        t =  [(k, Everyone[k]) for k in Everyone]
#        t.sort()
#        d={}
#        for k,v in t:
#            if v in d.values():
#                continue
#            d[k] = v
        
        list1 = []
        data = open(filename,"w")
        data.write('\nuserID\thandle\n')  
        
        ## combine
        for id1 in sorted(Everyone, key=str): 
            data.write("%s: %s" % (id1, Everyone[id1]) + " \n") 
            list1.append(id1)# copy into a list
                
        data.close()  
        print ("_____________________________ \n[" + date + "-AllUsers.txt]")
        print ("- " + str(len(Everyone)) + " users active in community\n")
        print ("Finished finding all users.\n")
        print ("_____________________________ ")
        
        return sorted(list1, key=str)
    
    def print_status(self, collection, CMC, date, filename):
        print ("\n_____________________________ \n[" + date + "-" + filename + ".txt]")
        print ("- " + str(len(collection)) +  " " + CMC) 
         
    def slice (self, user, part):  
        x = user.split('(')
        handle = x[0]
        y = x[1].split(')')
        id2 = y[0]
        u = "" 
        if part=="id":
            u = id2
        if part=="handle":
            u = handle
        return u     
    
    def stats(self, dict1, CMCsample):
        users.print_len(dict1, CMCsample)     
            
    # ============================================================
    # function DataForumThreads 
    # reads forum posts and comments and create list of users
    # 1. create an index of user names
    # 2. add to postsData matrix
    # ============================================================       
    def DataForumThreads (self, filename):
        TblFP = [['urlID', 'creator', 'commenters', '#comments']]
        ForumThreadID = ['urlID']           # List of data arrays in this class
        UsersInForum = {}
        authors = {}
        replyers = {} 
        
        data = open(foFP,"w")
        data.write('urlID\tcreator\t\t\t#comments\t\tcommenters\n')
    
        ## read forum posts file
        file = open(filename)  
        for line in file:                       
                ## Skip blank Lines & Beginning or end
            if line.strip()==_beg or line.strip()==_end:
                pass                                       
            else: 
                ## Split Line into fields
                fields = line.strip().split(_sep)
                #title = fields[0]
                url = fields[1].split('/')
                urlID = url[7]
                poster = fields[2].strip() 
                cNum = fields[4]
                commenters = fields[5].split(';')
                
                ## Author data: ID & Handle
                posterHandle = self.slice(poster,"handle")
                posterID = self.slice(poster,"id")
               
                ## Save data
                authors[posterID] = posterHandle
                if posterID not in Everyone.keys(): Everyone[posterID] = posterHandle
                UsersInForum = self.pair(posterID, posterHandle, UsersInForum)  
                TblFP.append([urlID, posterID, posterHandle, commenters, cNum]) 
                ForumThreadID.append(urlID)
                data.write(urlID + '\t' + poster + '\t\t' + cNum + '\t\t' + fields[5].strip() + '\n')        

                 
                for i in commenters: 
                    if len(i)>0:
                        userHandle = self.slice(i,"handle") 
                        userID = self.slice(i,"id")
                        UsersInForum = self.pair(userID, userHandle, UsersInForum) 
                        if userID not in Everyone: Everyone[userID]=userHandle 
                        if userID not in replyers: replyers[userID]=userHandle 
                        #Should replyers also be counted as authors? 
                            

        data.close()
        
        ## Saving data for later use
        dataTables.TblFP = TblFP
        users.uF = UsersInForum
        #users.uF = Everyone 
        
        ## Print update for log
        self.print_status(dataTables.TblFP, "threads", date, "TblForumThreads") 
#        print ("- # comments (& per thread)")
        self.stats(users.uF, "participating in forum") 
        print ("- " + str(len(authors)) + " people who start threads") 
        print ("- " + str(len(replyers)) + " people who comment") 

    #    end DataForumThreads
     

    # ============================================================
    # function DataJournals 
    # reads forum posts and comments and create list of users
    # 1. create an index of user names
    # 2. add to postsData matrix
    # ============================================================
    
    def DataJournals (self, filename): 
        TblJournal = [['urlID', 'creator', 'commenters', '#comments']] 
        currLine = ""
        userListj = []
        totalComments = []
        UsersInJournals = {}
        replies = {}
        authors = {}
                 
        data = open(foJP,"w")
        data.write('urlID\tcreator\t#comments\tcommenters\n')
    
        # now read for journal users
        fileJ = open(filename)
        for line in fileJ:          # create an index of user names
            if line.strip()==_beg: 
                currLine = ""       #clear temporary string
            elif line.strip()==_end:
                fields = currLine.strip().split(_sep) 
                temp = fields[0].split("\t")
                
                # parse fields
                creator = temp[0] 
                url = temp[1]
#                title = fields[1]
#                datestamp = fields[2]
#                entry = fields[3]
                commenters = fields[5].split(';')  #users who make comments to the post
                comments = fields[4]  
                
                
                totalComments.append(comments)
                TblJournal.append([url, creator, comments, len(commenters), commenters])
#                jPost.append([url, creator, comments, len(commenters), commenters])   
#                TblJournal.append(jPost)
                data.write(url+'\t'+creator+'\t\t'+comments+'\t\t'+str(len(commenters)-1)+'\t\t'+fields[5]+ '\n')
                
                ## ADDING JOURNAL AUTHORS TO EVERYONE
                if creator not in Everyone.keys(): Everyone[creator] = ''
                if creator not in UsersInJournals: UsersInJournals[creator] = ''
                
                if len(comments)>0: 
                    userListj.append(comments) 
                    
                    for i in commenters: 
                        if i=="":
                            pass
                        else:
                            handle = self.slice(i,"handle")  
                            num = self.slice(i,"id") 
                            UsersInJournals = self.pair(num, handle, UsersInJournals)
                            replies = self.pair(num, handle, replies)
                            if num not in Everyone.keys(): Everyone[num]=handle 
                
                authors[creator] = "x" #position in TblJournal
                   
            else: 
                currLine = currLine + "\n" + line
        
        data.close()     
        
        
        ## save data in variables   
        dataTables.TblJP = TblJournal
        self.print_status(dataTables.TblJP, "journal posts", date, "TblJournalEntry") 
        users.uJ = UsersInJournals 
        
        ## print data to log
        n=[int(x) for x in totalComments]
        print ("- " + str(sum(n)) + " of comments")
        print ("- " + str(sum(n)/len(totalComments)) + " per post") 
        self.stats(UsersInJournals, "journal users") 
        self.stats(replies, "journals who comment") 
        print ("- " + str(len(authors)) + " authors of journals")
            



    # calculate users who write notes
    # create an index of user names

    # ============================================================
    # function DataJournals 
    # reads forum posts and comments and create list of users
    # 1. create an index of user names
    # 2. add to postsData matrix
    # ============================================================
        
    def DataNotes (self, filename):
    
        TblNotes = []
        Commenters = []
        UsersInNotes={} 
        n = 0
        
        data = open(foN,"w")
        data.write('userID\t#notes\t\tfriends\t\tcommenters\n')
        
        fileN = open(fiN)
        for line in fileN:   
            line = str.strip(line)
            if line.strip()==_beg or line.strip()==_end:
                pass                
            else:
                field = line.split('\t') 
                if field[0] not in Everyone.keys(): Everyone[field[0]]= ''

                if re.match("no notes", field[1]):
                    pass
                else:
                    # user id      # notes     #of friends   list of friends
                    friendsOut = ""
                    friendsIn = field[3].split(';')
                    for friend in friendsIn:
                        x = friend.split('=')
                        if len(x)>1: 
                            user = x[0]
#                            count1 = x[1]
                            id1 = self.slice(user,"id") 
                            handle = self.slice(user,"handle")
                            if id1 not in Everyone: Everyone[id1]=handle
                            friendsOut = friendsOut + user  + ";"

                    data.write(field[0]+'\t'+field[1]+'\t\t\t'+field[2]+'\t\t\t'+friendsOut+'\n')
                    
                    TblNotes.append([field[0], field[1], field[2], friendsOut]) 
                    Commenters = field[3].split(';') 
                    if len(Commenters) > 0:  
                        for i in Commenters: 
                            if i=="":
                                pass
                            else:
                                x = i.split('(')
                                handle = x[0] 
                                n = x[1].split(')')
                                num = int(n[0])  
                                UsersInNotes = self.pair(num, handle, UsersInNotes)
                                if n[0] not in Everyone: Everyone[n[0]]=handle
                            
        data.close()
        dataTables.TblN = TblNotes
        users.uN = UsersInNotes 
        self.print_status(TblNotes, "users receiving notes", date, "TblNotes")
        n=[int(x[1]) for x in TblNotes]
        print ("- " + str(sum(n)) + " notes in this sample")
        f=[int(x[2]) for x in TblNotes]
        print ("- " + str(sum(f)/len(TblNotes)) + " friends posting to each person")
        self.stats(UsersInNotes, "in notes who post")    
    
        
    def ActiveUsersForum(self, allUsers): 
        temp = []
        nodes = []
        edgesInForum=[] 
        FPusers = numpy.zeros(shape=(len(allUsers), 4),dtype=numpy.int) 
        
        # fill in matrix for FORUM USERS
        for row in dataTables.TblFP :                       # [urlID, posterID, posterHandle, commenters, cNum]
            poster = row[1]                                 # poster handle 
            if poster=="creator": 
                pass
            else:   
                #UserID and Starting Thread Columns
                u = allUsers.index(row[1])                  # user's ID  
                FPusers[u][0] = row[1]
                FPusers[u][1] = FPusers[u][1]  + 1          # calculating the times user started a thread 
                
                set1 = []                                   # creating a collection for commenters
                for p in row[3]: 
                    if (p != ''): 
                        set1.append(Prepare().slice(p, "id"))  # if person exists as commenter, add to set1
                        
                        #FC Column
                        replyer = Prepare().slice(p,"id")
                        mX = allUsers.index(replyer)           # sender's position in final array?
                        FPusers[mX][0] = replyer 
                        FPusers[mX][2] = FPusers[mX][2]+1   # set frequency of communication between users
                        
                        #Responses Column
                        FPusers[u][3] = FPusers[u][3]+1 
                        
                # build pairs of communication 
                set2 = set1
                set2.insert(0, poster)
                
                
        ## algorithm for creating pairs in one long list
                partialPairs=[(x,y) for y in set1 for x in set2 if set2.index(x)>set1.index(y)] 
                if len(partialPairs)>0: 
                    for x in partialPairs:
                        edgesInForum.append(x)
        
        ## save edges in text file
        numpy.savetxt(foLF+".pairs", edgesInForum, fmt='%s')      
                                                            #completed row == FPusers =====> # times START THREAD; # times RESPOND TO THREADs;  # OF PEOPLE RESPOND in THREAD??
        for row in FPusers:                                 #filter: remove blank rows
            if (sum(row[1:3]) >= 5):                        #before cut off zero, now slim down to at least 5 posts.
                temp.append(row) 
                nodes.append(row[0])                        # [UserID, times user started a thread, freq of comm btwn users, responses to threads]
        numpy.savetxt(foLF, temp, fmt='%s')
        
        print (str(len(nodes)) + " active forum users")
        
        ## make matrix with data
        matrixF = numpy.zeros(shape=(len(nodes),len(nodes)), dtype=numpy.int)
        fG=networkx.MultiDiGraph() 
        for sender,target in edgesInForum:
            try:
                x = nodes.index(int(target))
                y = nodes.index(int(sender))
                weight = matrixF[x][y]
                matrixF[x][y] = weight+1 
                fG.add_edge(sender, target)  
            except:
                pass 
        numpy.savetxt(foMF, matrixF, fmt='%s')
        print ("saved matrix for active forum users.")
        
       print ("\tdegree centrality" )
       print (networkx.degree_centrality(fG))
       print ("\tin degree centrality" )
       print (networkx.in_degree_centrality(fG))
       print ("\tout degree centrality") 
       print (networkx.out_degree_centrality(fG) )
        return edgesInForum 
     
    def ActiveUsersJournal(self, list1): 
        edgesInJournal=[]
        nodesInJournal=[]
        temp=[]
        size = len(list1)
        JPusers = numpy.zeros(shape=(size, 4),dtype=numpy.int) 
        
        # fill in matrix for JOURNAL USERS
        for row in dataTables.TblJP :                       # [URL, Author, CommentCount, len(commenters), ListOfCommentersfields[5]
            poster = row[1]                                 # poster handle 
            if poster=="creator": 
                pass
            else:  
                #UserID and Starting Thread Columns
                u = list1.index(row[1])                     # user's ID  
                JPusers[u][0] = row[1]
                JPusers[u][1] = JPusers[u][1]  + 1         # times user started a thread 
                
                set1 = []
                for p in row[4]: 
                    if (p != ''):                       # if not blank, go ahead and fill in the fields
                        set1.append(Prepare().slice(p, "id"))
                        
                        #FC Column
                        mX = list1.index(Prepare().slice(p,"id"))    # sender's position in array
                        JPusers[mX][0] = Prepare().slice(p,"id") 
                        JPusers[mX][2] = JPusers[mX][2]+1              # set frequency of communication between users
                        
                        #Responses Column
                        JPusers[u][3] = JPusers[u][3]+1
                
                # build pairs of communication 
                set2 = set1
                set2.insert(0, poster)
                
        ## algorithm for creating pairs
                partialPairs=[[x,y] for y in set1 for x in set2 if set2.index(x)>set1.index(y)] 
                if len(partialPairs)>0: 
                    for x in partialPairs:
                        edgesInJournal.append(x) 
        ## save edges in text file
        numpy.savetxt(foLJ+".pairs", edgesInJournal, fmt='%s')  
                                                        #completed row =====> # times WRITE IN BLOG; # times RESPOND TO BLOG;  # OF PEOPLE RESPOND in BLOG Post??
                                                        #filter: remove blank rows
        for row in JPusers: 
            if ((row[1]>=5) | (row[2]>=5) | (row[3]>=5)):
                temp.append(row) 
                nodesInJournal.append(row[0])

        numpy.savetxt(foLJ, temp, fmt='%s')
        print (str(len(nodesInJournal)) + " active journal users")
        
        ## make matrix with data
        matrixJ = numpy.zeros(shape=(len(nodesInJournal),len(nodesInJournal)), dtype=numpy.int)
        jG=networkx.MultiDiGraph() 
        for sender,target in edgesInJournal:
            try:
                x = nodesInJournal.index(int(target))
                y = nodesInJournal.index(int(sender))
                weight = matrixJ[x][y]
                matrixJ[x][y] = weight+1 
                jG.add_edge(sender, target)
            except:
                pass 
        numpy.savetxt(foMJ, matrixJ, fmt='%s')
        print ("saved matrix for active journal users.")
        
        print ("\tdegree centrality" )
        print (networkx.degree_centrality(jG))
        print ("\tin degree centrality" )
        print (networkx.in_degree_centrality(jG))
        print ("\tout degree centrality") 
        print (networkx.out_degree_centrality(jG) )

        return edgesInJournal 
        
    def ActiveUsersNotes(self, list1): 
        edgesInNotes = []
        nodesInNotes = []
        temp = [] 
        temp2 = []
        Nusers = numpy.zeros(shape=(len(list1), 4),dtype=numpy.int) 
        
        # fill in matrix for JOURNAL USERS
        for row in dataTables.TblN :                       # userID; #notes; friends; commenters
            poster = row[0]                                # poster handle 
            if poster=="creator": 
                pass
            else:  
                #UserID and times written a note 
                u = list1.index(poster)                     # user's ID  
                Nusers[u][0] = poster
                Nusers[u][2] = row[1]                      # the times poster received notes 
                Nusers[u][3] = row[2]                      # calculate # of people receive from
                        
                temp = row[3].split(';')
                set1=[]
                for p in temp: 
                    if (p != ''):  
                        set1.append(Prepare().slice(p, "id"))
                        
                        # sender's position in array
                        mX = list1.index(Prepare().slice(p,"id"))    
                        
                        # times a user wrote notes
                        Nusers[mX][0] = Prepare().slice(p,"id") 
                        Nusers[mX][1] = Nusers[mX][1]  + 1    
                        
                        #calculate number of ppl written to 
                        #[u][4]
                        
                # build pairs of communication 
                set2 = set1
                set2.insert(0, poster)
                
        ## algorithm for creating pairs
                partialPairs=[(x,y) for y in set1 for x in set2 if set2.index(x)>set1.index(y)] 
                if len(partialPairs)>0: 
                    for x in partialPairs:
                        edgesInNotes.append(x)
                        print (x)
        ## save edges in text file
        numpy.savetxt(foLN+".pairs", edgesInNotes, fmt='%s') 
        
                                                    #completed row =====> # times WRITE a note; # times receive a note;  # OF people receive from, # of ppl write to
                                                    #filter: remove blank rows
        for row in Nusers:
            if ((row[1]>=5)): # limit to active users, 5+ notes written
#            if (((row[0] >= 5) ) | (row[1]>=5) | (row[2]>=5)):
                temp2.append(row)
                nodesInNotes.append(row[0])
        
        numpy.savetxt(foLN, temp2, fmt='%s')
        print (str(len(nodesInNotes)) + " active notes users")
        
        ## make matrix with data
        matrixN = numpy.zeros(shape=(len(nodesInNotes),len(nodesInNotes)), dtype=numpy.int)
        nG = networkx.MultiDiGraph()
        for sender,target in edgesInNotes:
            try:
                x = nodesInNotes.index(int(target))
                y = nodesInNotes.index(int(sender))
                weight = matrixN[x][y]
                matrixN[x][y] = weight+1
                nG.add_edge(sender, target) 
            except:
                pass 
        numpy.savetxt(foMN, matrixN, fmt='%s')
        print ("saved matrix for active notes users of this community.")
        
        print ("\tdegree centrality" )
        print (networkx.degree_centrality(nG))
        print ("\tin degree centrality" )
        print (networkx.in_degree_centrality(nG))
        print ("\tout degree centrality") 
        print (networkx.out_degree_centrality(nG) )
        return edgesInNotes  
    
    def findusers(self, list1):
        FPu= {}
        
        for x,y in list1:
            try:
                x in FPu[x]
                i = FPu[x]
                FPu[x] = i+1
            except:
                FPu[x] = 1
            try:
                y in FPu[y]
                i = FPu[y]
                FPu[y] = i+1
            except:
                FPu[y] = 1
        return FPu
    
    ## SNA library version
    def CutOffLessThan5D(self, pairs, dataTbl, cmc): 

       # build matrix from pairs  
       sna.loadGraphFromCsv(foMF+".pairs", " ")
       sna.runMeasure("totaldegreeCentrality")
       
       
       print ("\n display results .\n")
       sna.displayResults("totaldegreeCentrality")
       print ("\n")
       try:
           print ("Loading network from file\n(%s)"%(foMF+".pairs"))
           self.graph = networkx.read_edgelist(foMF+".pairs",delimiter=" ") 
           self.graph.name = "Social Network"
           
           
           print ("Attempt to draw graph.\n") 
           G=networkx.cubical_graph()
           
           print ("created G")
           networkx.draw(G)
           
           plt.show() # display
           
           print("Degree centrality")
           d=degree_centrality(G)
           for v in G.nodes():
               print("%0.2d %5.3f"%(v,d[v]))

       except:
          print ("Unable to open file:",filename)
          
       print ("cutoff < 5 degrees end method.\n")
          

class UserData (object): 
    global everyone
    everyone = {}
    
    def __init__(self, uF=None, uJ=None, uN=None, uA={}):
        self.uN = uN
        self.uF = uF
        self.uJ = uJ
        self.uA = uA
    
    def set_uN (self, dict1):
        self._uN = dict1 
    
    def get_uN (self):
        return self._uN

    def set_uJ (self, dict1):
        self._uJ = dict1 
    
    def get_uJ (self):
        return self._uJ
    
    def set_uF (self, dict1):
        self._uF = dict1 
    
    def get_uF (self):
        return self._uF
        
    def set_uA (self, dict1):
        self._uA = dict1
    
    def get_uA (self):  
        return self._uA
        
    def addUser(self, id1, handle):
        everyone.setdefault(id1)   
      
        
    def print_len(self, dict1, sample):
        print ("   " + str(len(dict1)) + " " + sample)

    def print_keys(self, dict1={}): 
        for key in sorted(dict.iterkeys()):
            print ("%s: %s" % (key, dict1[key])) 
             

        
def Settings(): 
    #Set Global Variables
    global foFP
    global foFC
    global foJP
    global foJC
    global foN
    global foLF
    global foLJ
    global foMF
    global foMJ
    global foLN
    global foMN
    global foU 
    global _sep
    global _beg
    global _end 
    global dataTables
    global users
    global prepare 
    global sna
    global date
    global fiFP
    global fiFC
    global fiJP
    global fiJC
    global fiN  
    global maindictionary
    
    # Get a date object
    today = datetime.date.today() 
    ##########################
    # Get today's date.
    ##########################
    date = str(today.year)+"."+str(today.month)+str(today.day) 
    #============================================================ 
    workspace = "workspace"
    rawData = "workspace/rawdata"

    #  This is a list of data files generated by this script.
    datapath = workspace + "data/"
    listspath = workspace + "lists/"
    matricespath = workspace + "matrices/"
    
    foFP = datapath + date +"-TblForumThreads.txt"
    foFC = datapath + date +"-TblForumComments.txt"
    foJP = datapath + date +"-TblJournalEntry.txt"
    foJC = datapath + date +"-TblJournalComments.txt"
    foN = datapath + date +"-TblNotes.txt"
    foLF = listspath + date + "-ForumUsers.txt"
    foLJ = listspath + date +"-JournalUsers.txt"
    foMF = matricespath + date +"-Forum.txt"
    foMJ = matricespath + date +"-Journals.txt"
    foLN = listspath + date +"-NotesUsers.txt"
    foMN = matricespath + date +"-Notes.txt"
    foU = listspath + date +"-AllUsers.txt"
    #end data files
    #============================================================
    
    ## This is a list of raw data files imported by the script.
    fiFP = rawData + "/Posts.txt"
    fiFC = rawData + "/PostComment.txt"
    fiJP = rawData + "/Journals.txt"
    fiJC = rawData + "/JournalComments.txt"
    fiN  = rawData + "/UserNotes.txt" 
    
    ## List of separator variables
    _sep = "#@XTSEP@#"
    _beg = "#XTSTART#"
    _end = "#XTEND#"
    
    ## define classes below
    dataTables = DataTables()
    users = UserData()
    prepare = Prepare() 
    sna = libSNA.SocialNetwork()

def Run():     
    ##transform textfiles to tables
    prepare.DataForumThreads(fiFP)
    prepare.DataJournals(fiJP)
    prepare.DataNotes(fiN) 
    
    ## print user information into files
    maindictionary = prepare.PrintAllUsers(foU)  
    
    ## apply cut offs for number of messages  (at least 5 of post, respond, etc)
    print ("\nRemoving inactive users and creating matrices...")
    edgesF = prepare.ActiveUsersForum(maindictionary)          # forum matrix
    edgesJ = prepare.ActiveUsersJournal(maindictionary)        # journal matrix
    edgesN = prepare.ActiveUsersNotes(maindictionary)          # notes matrix
    edgesA = prepare.ActiveUsersCommunity() all matrix
    
Settings()
Run()