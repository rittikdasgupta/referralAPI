import networkx as nx
from datetime import datetime
import pytz
import matplotlib.pyplot as plt
from referral.creds import db

flag=1
root="b70949f6-1256-4ffa-9556-cefdd2aa4216"
users=1
trees=dict()
wallet=dict()
joining=500
percentage=0.2
topup=percentage*joining

def createTree(User):
    trees[User]=nx.DiGraph() 
    wallet[User]=0
    G=trees[User]
    G.add_node(User)

def addNodeEdge(Ref,User):
    all_trees=list(trees.keys())
    for x in all_trees:
        G=trees[x]
        nodes=list(G.nodes())
        if(Ref in nodes):
            G.add_node(User)
            G.add_edge(Ref,User)
    
def displayGraph():
    all_trees=list(trees.keys())
    for x in all_trees:
        G=trees[x]
        plt.title('Tree of user : '+x)
        pos = nx.spring_layout(G)
        f = plt.figure()
        nx.draw(G, pos, with_labels=True,node_color='yellow',arrows=True)
        file_User="Tree_"+x+".png"
        f.savefig('assets/{}'.format(file_User),dpi=300)

def calculateWalletBalance():
    users=list(wallet.keys())
    for x in users:
        G=trees[x]
        nodes=list(G.nodes())
        levels=dict()
        paths=[]
        for y in nodes:
            if(x!=y):
                level_len=len(list(nx.shortest_path(G, source=x, target=y)))-2
                levels[y]=level_len
                paths.append(level_len)
        for z in paths:
                wallet[x]+=(topup)/2**z
    
def displayStats():
    print("")
    print("STATISTICS : ")
    print("Joining Fee =",joining)   
    print("Percentage = "+str(percentage*100))
    print("Number of Users =",users)
    print("WALLET STATS :")
    print(wallet)

#-------------------------MAIN DRIVER FUNCTION---------------------------
def DriverFunction(UserID,RefID=root): 
    fetch_ref=db.users.find_one({"referralId":RefID})
    fetch_user=db.users.find_one({"referralId":UserID})
    if fetch_ref and fetch_user:
        trees[RefID]=fetch_ref["trees"]
        trees[UserID]=fetch_user["trees"]
        wallet[RefID]=fetch_ref["wallet"]
        wallet[UserID]=fetch_user["wallet"]
    addNodeEdge(RefID,UserID)
    calculateWalletBalance()
    displayGraph()
    updateReferrer=db.users.update({"referralId":RefID},
    {
        "$set":{
            "trees":trees[RefID],
            "wallet":wallet[RefID]
        }
    })
    updateUser=db.users.update({"referralId":UserID},
    {
        "$set":{
            "trees":trees[UserID],
            "wallet":wallet[UserID]
        }
    })
    if updateReferrer and updateUser:
        return True
    return False


#-----------------DRIVER FUNCTION FOR TERMINAL-----------------------
# createTree(root)      #Root User
# while(flag):
#     if(users==1):
#         ref=root
#     else:
#         ref=input('Enter Referral User ID : ')
#     usr=input('Enter your User ID: ')
#     addNodeEdge(ref,usr)
#     flag=int(input("Press 0 to stop : "))
#     users+=1

# if(flag==0):
#     calculateWalletBalance()
#     displayStats()
#     displayGraph()