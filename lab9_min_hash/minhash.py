from collections import OrderedDict, Counter
from random import randint
from math import sqrt


N = 100 
D = 100 

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
    sum_square_diff = 0
    c = 0
    for my_user, my_songs in user_songs.items():

        my_signatures = get_signatures(max_song_id, my_songs, hash_functions)
        
        for u in user_songs:
            # naive method
            common = 0
            for song in my_songs:
                if song in user_songs[u]:
                    common += 1
            jaccard = float(common) / ( len(my_songs) + len(user_songs[u]) - common )
            if(jaccard == 0 ):
                continue

            # minhash
            other_signatures = get_signatures(max_song_id, user_songs[u], hash_functions)
            common_sigs = 0
            for idx, sig in enumerate(my_signatures):
                if sig == other_signatures[idx]:
                    common_sigs +=1
            minhash_res = float(common_sigs)/D

            # update values used for RMSE
            sum_square_diff += (jaccard - minhash_res)**2
            c += 1
    # get RMSE
    rmse = sqrt(sum_square_diff / c)
    print("{},{},{}".format(N,D,rmse))


if __name__ == "__main__": 
    user_songs = OrderedDict()
    hash_functions = []

    N = 100 
    D = 500 
    max_song_id = load_facts_file("facts-nns.csv", user_songs, hash_functions)
    minhash(user_songs, hash_functions, max_song_id)


