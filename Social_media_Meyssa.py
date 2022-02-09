import random

def get_index(network, user):
    '''(2Dlist, int)->int
    Given a 2D-list for friendship network, and a user ID,
    returns the index of that user in the 2D-list friendship network. Returns -1 if the user not in the network
    Precondition: user is a non-negative int'''
    
    location=-1
    for i in range(len(network)):
        if network[i][0]== user:
            location=i
    return location


def get_index_binary_search(network, user):
     '''(int, 2Dlist)->int 
     Given a 2D-list for friendship network and the user ID,
     returns the index of that user in the 2D-list friendship network.
     Returns -1 if the user not in the network
     Precondition: network is sorted and user is a non-negative int
     '''
     
     b = 0
     e = len(network)- 1

     while b <= e:
          mid = (b + e) // 2
          if user < network[mid][0]:
               e = mid - 1
          elif user > network[mid][0]:
               b=mid+1
          else:
               return mid
               
     return -1; # Now e < b

   
def create_network(file_name):
    '''(str)->list of tuples where each tuple has 2 elements the first is int and the second is list of int

    Precondition: file_name has data on social netowrk. In particular:
    The first line in the file contains the number of users in the social network
    Each line that follows has two numbers. The first is a user ID (int) in the social network,
    the second is the ID of his/her friend.
    The friendship is only listed once with the user ID always being smaller than friend ID.
    For example, if 7 and 50 are friends there is a line in the file with 7 50 entry, but there is line 50 7.
    There is no user without a friend
    Users sorted by ID, friends of each user are sorted by ID
    Returns the 2D list representing the frendship nework as described above
    where the network is sorted by the ID and each list of int (in a tuple) is sorted (i.e. each list of friens is sorted).
    '''
    friends = open(file_name).read().splitlines()
    n=int(friends[0].strip()) 
    friends.pop(0)
    network=[]

    # for every pair a,b where a<b add b to the list of a
    for pair in friends:
        pair=pair.split(" ")
        user=int(pair[0])
        friend=int(pair[1])
        if len(network)==0 or user != network[-1][0]:
            network.append( ( user, [friend] ) )
        else:
            network[-1][1].append(friend)
            
    # add "inverted pairs", i.e for every pair a,b add a to the list of b
    for pair in friends:
        pair=pair.split(" ")
        user=int(pair[1])
        friend=int(pair[0])
 
        location=get_index(network, user)
        if len(network)==0 or location==-1:
            network.append( ( user, [friend] ) )           
        else:
            network[location][1].append(friend)
    # sort eac list of friends
    network.sort()
    for item in network:
        item[1].sort()
    return network

#O(n^2)
def getCommonFriends(user1, user2, network):
    '''(int, int, 2D list) ->int
    Precondition: user1 and user2 IDs in the network. 2D list sorted by the IDs, 
    and friends of user 1 and user 2 sorted 
    Given a 2D-list for friendship network, returns the sorted list of common friends of user1 and user2
    '''
    loc1=get_index(network, user1)
    loc2=get_index(network,user2)
    friends1=network[loc1][1]
    friends2=network[loc2][1]
    common=[]
    for user in friends1:
        if user in friends2:
            common.append(user)
    return common

# for bonus
def merge_sorted_lists(a,b):
    '''(list of int, list of int)->list of int
    Precondition: a is sorted and not empty and b is sorted not empty
    Given two sorted 1D lists, returns the sorted list of all elements in a and b together.
    '''
    # reverse the lists so you can use .pop() with O(1) costs
    arev=a[::-1] # O(len(a))
    brev=b[::-1] # O(len(b))
    ab=[]
    while len(arev)>0 and len(brev)>0: #O(len(a)+len(b))
        if arev[-1]<=brev[-1]: # comare two smallest elements. they are at the end
            ab.append(arev[-1])
            arev.pop() # removing last element is O(1) -- amortized
        else:
            ab.append(brev[-1])
            brev.pop()
    if len(arev)>0:
        while len(arev)>0:
            ab.append(arev[-1])
            arev.pop() 
    if len(brev)>0:
        while len(brev)>0:
            ab.append(brev[-1])
            brev.pop()
    return ab
        
       
    

# bonus: O(#friends_user_1 + #friends_user_2 + log n) -- so better than O(n):
def getCommonFriends_v2(user1, user2, network):
    '''(int, int, 2D-list) ->int
    Precondition: user1 and user2 IDs in the network.  2D list sorted by the IDs, 
    and friends of user 1 and user 2 sorted 
    Given a 2D-list for friendship network, returns the maximum number of friends any user in the network has.Returns sorted list of common friends of user1 and user2
    '''
    
    loc1=get_index_binary_search(network, user1)
    loc2=get_index_binary_search(network, user2)
    friends1=network[loc1][1]
    friends2=network[loc2][1]
    allfriends=merge_sorted_lists(friends1,friends2)

    common=[]

    # if user1 and user 2 have commong friends they have to be next to each other in sorted all friends list
    i=0
    while i < len(allfriends)-1:
        if allfriends[i]==allfriends[i+1]:
            common.append(allfriends[i])
            i=i+1
        i=i+1
    return common
    
def recommend(user, network):
    '''(int, 2Dlist)->int or None
    Given a 2D-list for friendship network, returns None if there is no other person
    who has at least one neighbour in common with the given user and who the user does
    not know already.
    
    Otherwise it returns the ID of the recommended friend. A recommended friend is a person
    you are not already friends with and with whom you have the most friends in common in the whole network.
    If there is more than one person with whom you have the maximum number of friends in common
    return the one with the smallest ID. '''
    
    location=get_index(network, user)
    maximum=-1
    who=None

    if location==-1: return who
    
    for item in network:
        if item[0]!=user:
            if user not in item[1]:
                common=getCommonFriends(user, item[0],network)
                if len(common)>maximum and len(common)>0:
                    maximum=len(common)
                    who=item[0]
    
    return who


def k_or_more_friends(network,k):
    '''(2Dlist,int)->int
    Given a 2D-list for friendship network, returns the number of users who have at least k friends in the network'''
    count=0
    for item in network:
        if len(item[1])>=k:
            count=count+1
    return count

def maximum_num_friends(network):
    '''(2Dlist)->int
    Given a 2D-list for friendship network, returns the maximum number of friends any user in the network has.
    '''
    maximum=0
    for item in network:
        if len(item[1])>=maximum:
            maximum=len(item[1])
    return maximum
    

def people_with_most_friends(network):
    '''(2Dlist)->1D list
    Given a 2D-list for friendship network, returns a list of people (IDs) who have the most friends in network.'''
    maximum=maximum_num_friends(network)
    max_friends=[]
    for item in network:
        if len(item[1])==maximum:
            max_friends.append(item[0])
    return max_friends

def average_num_friends(network):
    '''(2Dlist)->number
    Returns an average number of friends overs all users in the network'''
    summation=0
    for item in network:
        summation=summation+len(item[1])
    return summation/len(network)
    

def knows_everyone(network):
    '''(2Dlist)->bool
    Given a 2D-list for friendship network, returns True if there is a user in the network who knows everyone and False otherwise'''
    
    for item in network:
        if len(item[1])==len(network)-1:
            return True
    return False

def is_valid_file_name():
    '''None->str or None'''
    file_name = None
    try:
        file_name=input("Enter the name of the file: ").strip()
        f=open(file_name)
        f.close()
    except FileNotFoundError:
        print("There is no file with that name. Try again.")
        file_name=None
    return file_name 

def get_file_name():
    file_name=None
    while file_name==None:
        file_name=is_valid_file_name()
    return file_name
    

def get_int():
    '''None->int or None'''
    num = None
    try:
        num=int(input("Enter an integer for a user ID:").strip())
    except ValueError:
        print("That was not an integer. Please try again.")
    return num

def get_uid(network):
    '''(2Dlist)->int'''
    uid=None
    while uid==None or get_index(network, uid)==-1:
        uid=get_int()
        if uid!=None and get_index(network, uid)==-1:
            print("That user ID does not exist. Try again.")
    return uid
    

##############################
# main
##############################
file_name=get_file_name()
    
net=create_network(file_name)

print("\nFirst general statistics about the social network:\n")

print("This social network has", len(net), "people/users.")
print("In this social network the maximum number of friends that any one person has is "+str(maximum_num_friends(net))+".")
print("The average number of friends is "+str(average_num_friends(net))+".")
mf=people_with_most_friends(net)
print("There are", len(mf), "people with "+str(maximum_num_friends(net))+" friends and here are their IDs:", end=" ")
for item in mf:
    print(item, end=" ")

print("\n\nI now pick a number at random.", end=" ")
k=random.randint(0,len(net)//4)
print("\nThat number is: "+str(k)+". Let's see how many people has that many friends.")
print("There is", k_or_more_friends(net,k), "people with", k, "or more friends")

if knows_everyone(net):
    print("\nThere at least one person that knows everyone.")
else:
    print("\nThere is nobody that knows everyone.")

print("\nWe are now ready to recommend a friend for a user you specify.")
uid=get_uid(net)
rec=recommend(uid, net)
if rec==None:
    print("We have nobody to recommend for user with ID", uid, "since he/she is dominating in their connected component")
else:
    print("For user with ID", uid,"we recommend the user with ID",rec)
    print("That is because users", uid, "and",rec, "have", len(getCommonFriends(uid,rec,net)), "common friends and")
    print("user", uid, "does not have more common friends with anyone else.")
        

print("\nFinally, you showed interest in knowing common friends of some pairs of users.")
print("About 1st user ...")
uid1=get_uid(net)
print("About 2st user ...")
uid2=get_uid(net)
print("Here is the list of common friends of", uid1, "and", uid2)
common=getCommonFriends(uid1,uid2,net)
for item in common:
    print(item, end=" ")



    
