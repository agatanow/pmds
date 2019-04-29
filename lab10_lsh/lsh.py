from collections import OrderedDict, Counter
from random import randint
from math import sqrt


N = 100 
D = 100 
S = 0.8
B = 10
R = 2

def load_facts_file(path, user_songs, func_tab):
    with open(path, 'r') as facts:
        facts.readline()
        c = 0
        max_song_id = 0
        for fact in facts:
            split = fact.split(',')
            user = int(split[0])
            song = int(split[1])
            if max_song_id < song:
                max_song_id = song

            if user not in user_songs:
                if c < N:
                        user_songs[user]=set()
                        user_songs[user].add(song)
                        c+=1
                else:
                    break
            else:
                user_songs[user].add(song)
        generate_hash_functions(func_tab, max_song_id)
        
        return max_song_id

            

def primary_gt_than(M):
    x = M + 1
    while(True):
        is_prim = True
        for i in range(2,x//2+1):
            if x%i == 0:
                is_prim = False
                x += 1
                break
        if is_prim == True:
            break
    return x

def hash_function(a,b,p, n):
    def func(x):
        return ((a*x + b ) % p ) % n
    return func

def generate_hash_functions(func_tab, n):
    p = primary_gt_than(n) # prime p
    # array of hash functions
    for i in range(D):
        a=randint(1,p-1)
        b=randint(0,p-1)
        func_tab.append( hash_function(a, b, p, n ) )

def get_signatures(max_song_id, my_songs, hash_functions):
    my_signatures = [max_song_id for i in range(D)]
    for idx, f in enumerate(hash_functions):
        for song in my_songs:
            val = f(song)
            if my_signatures[idx] > val:
                my_signatures[idx] = val
    return my_signatures


def minhash(user_songs, hash_functions, max_song_id):

    # init correct neighbours map
    neighbours = {}
    # init buckets used for creating lsh neighbours map
    buckets = {}

    for my_user, my_songs in user_songs.items():

        # update map for the correct neighbours
        neighbours[my_user] = set()
        for u in user_songs:
            common = 0
            for song in my_songs:
                if song in user_songs[u]:
                    common += 1
            jaccard = float(common) / ( len(my_songs) + len(user_songs[u]) - common )
            if (jaccard >= S):
                neighbours[my_user].add(u)

        # update buckets 
        my_signatures = get_signatures(max_song_id, my_songs, hash_functions)
        for i in range(0, len(my_signatures), R):
            buckets.setdefault(tuple(my_signatures[i:i+R]), set()).add(my_user)


    # create map for neighbours estimated by lsh method using buckets
    lsh_neighbours = {}
    for b_id, users in buckets.items():
        for first_user in users:
            for second_user in users:
                lsh_neighbours.setdefault(first_user, set()).add(second_user)

    # count recall value
    a_all = 0
    a_correct = 0
    for first_user_id, correct_n in neighbours.items():
        a_all += len(correct_n)
        for lsh_n in lsh_neighbours[first_user_id]:
            if lsh_n in correct_n:
                a_correct += 1
    print("S = {:1.2f}: {}".format(S,float(a_correct)/a_all))
            



if __name__ == "__main__": 
    user_songs = OrderedDict()
    hash_functions = []

    N = 200 

    B = 10
    R = 10
    D = R * B 
    S = (float(1)/B) ** (float(1)/R)
    
    
    max_song_id = load_facts_file("facts-nns.csv", user_songs, hash_functions)
    minhash(user_songs, hash_functions, max_song_id)


