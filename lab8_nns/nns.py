from collections import OrderedDict, Counter

CHECK_NO = 400 
NN_NUMBER = 100
USERS_NO = 100


def load_facts_file(path, user_songs, song_users):
    with open(path, 'r') as facts:
        facts.readline()
        c = 0
        for fact in facts:
            split = fact.split(',')
            user = int(split[0])
            song = int(split[1])

            user_songs.setdefault(user, set()).add(song)
            song_users.setdefault(song, set()).add(user) 

            # c += 1
            # if c >= CHECK_NO:
            #     break


def nns(exo, user):
    c = 0
    for my_user, my_songs in user_songs.items():
        # create Counter for my_user friends - counts how many common songs both have
        potential_friends = Counter()
        for song in my_songs:
            potential_friends.update(song_users[song])

        #print(potential_friends)

        # create list of tuples (similarity, friend) and sort it
        sorted_friends = []
        for potential_friend, common_songs_no in potential_friends.items():
            similarity = common_songs_no / (len(my_songs) + len(user_songs[potential_friend]) - common_songs_no)
            sorted_friends.append((similarity, potential_friend))
        sorted_friends.sort(reverse=True)

        # print results
        print('User = {}'.format(my_user))
        i = 0
        for similarity, friend in sorted_friends:
            print('{: >7} {:.5f}'.format(friend, similarity))
            i += 1
            if i >= NN_NUMBER:
                break
        print()

        # do nns for first USERS_NO only
        c+=1
        if c >= USERS_NO:
            break


if __name__ == "__main__": 
    user_songs = OrderedDict()
    song_users = {}

    load_facts_file("facts-nns.csv", user_songs, song_users)
    nns(user_songs, song_users)
