import random

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)

class User:
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

class SocialGraph:
    def __init__(self):
        self.lastID = 0
        self.users = {}
        self.friendships = {}

    def addFriendship(self, userID, friendID):
        """
        Creates a bi-directional friendship
        """
        if userID == friendID:
            print("WARNING: You cannot be friends with yourself")
        elif friendID in self.friendships[userID] or userID in self.friendships[friendID]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[userID].add(friendID)
            self.friendships[friendID].add(userID)

    def addUser(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.lastID += 1  # automatically increment the ID to assign the new user
        self.users[self.lastID] = User(name)
        self.friendships[self.lastID] = set()

    def populateGraph(self, numUsers, avgFriendships):
        """
        Takes a number of users and an average number of friendships
        as arguments
​
        Creates that number of users and a randomly distributed friendships
        between those users.
​
        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.lastID = 0
        self.users = {}
        self.friendships = {}

        # Add users
        # call addUser() until our number of users is numUsers
        for i in range(numUsers):
            self.addUser(f"User {i+1}")

        # Create random friendships
        # totalFriendships = avgFriendships * numUsers
        # Generate a list of all possible friendships
        possibleFriendships = []
        # Avoid dups by ensuring the first ID is smaller than the second
        for userID in self.users:
            for friendID in range(userID + 1, self.lastID + 1):
                possibleFriendships.append( (userID, friendID) )

        # Shuffle the list
        random.seed(31)
        random.shuffle(possibleFriendships)
        #print("random friendships:")
        #print(possibleFriendships)

        # Slice off totalFriendships from the front, create friendships
        totalFriendships = avgFriendships * numUsers // 2
        print(f"Friendships to create: {totalFriendships}\n")
        for i in range(totalFriendships):
            friendship = possibleFriendships[i]
            self.addFriendship( friendship[0], friendship[1] )

    def bft(self, starting_user):
        """
        Print each user in user's extended network in breadth-first order
        beginning from starting_user.
        """
        q = Queue()
        q.enqueue(starting_user)
        visited = set()
        user_list = []
        while q.size() > 0:
            v = q.dequeue()
            if v not in visited:
                user_list.append(v)
                visited.add(v)
                for connection in self.friendships[v]:
                    q.enqueue(connection)
        return user_list

    def bfs(self, starting_user, destination_user):
        """
        Return a list containing the shortest path from
        starting_user to destination_user in
        breath-first order.
        """
        q = Queue()
        q.enqueue([starting_user])
        visited = set()
        while q.size() > 0:
            path = q.dequeue()
            v = path[-1]
            if v not in visited:
                if v == destination_user:
                    return path
                visited.add(v)
                for connection in self.friendships[v]:
                    copy = path.copy()
                    copy.append(connection)
                    q.enqueue(copy)


    def getAllSocialPaths(self, userID):
        """
        Takes a user's userID as an argument
​
        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.
​
        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set

        # get all users in given user's extended network using bft function
        user_list = self.bft(userID)

        # use the bfs function to get path from given user to each connected user
        for user in user_list:
            # set each user as a key in "visited" dictionary
            # set each path as a value in "visited" dictionary
            visited[user] = self.bfs(userID, user)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populateGraph(10, 2)
    print("USERS:")
    print(sg.users)
    print("FRIENDSHIPS:")
    print(sg.friendships)
    connections = sg.getAllSocialPaths(1)
    print("DICTIONARY: ")
    print(connections)
