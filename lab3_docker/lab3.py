import sqlite3 as sql
from datetime import datetime as dt

# PARTICULAR SQL STATEMENTS USED IN THIS FILE

# Creates table for songs
CREATE_SONG_TABLE = (
    'CREATE TABLE SONG ('
        'perform_id VARCHAR(18) NOT NULL, '
        'id VARCHAR(18) NOT NULL, '
        'artist VARCHAR(256) NOT NULL, '
        'title VARCHAR(256) NOT NULL, '
        'PRIMARY KEY (id));')

# Creates table for dates
CREATE_DATE_TABLE = (
    'CREATE TABLE DATE ('
        'id INTEGER PRIMARY KEY, '
        'year INTEGER NOT NULL, '
        'month INTEGER NOT NULL, '
        'day INTEGER NOT NULL, '
        'hours INTEGER NOT NULL, ' 
        'minutes INTEGER NOT NULL, ' 
        'seconds INTEGER NOT NULL);')

# Creates table for listened songs
CREATE_LISTENED_SONG_TABLE = (
    'CREATE TABLE LISTENED_SONG ('
        'user_id VARCHAR(40) NOT NULL, '
        'song_id VARCHAR(18), '
        'date_id INTEGER, '
        'FOREIGN KEY(song_id) REFERENCES SONG(id), '
        'FOREIGN KEY(date_id) REFERENCES DATE(id));')

# 1. task query
# Finds 10 most popular songs, sorted descending by popularity
MOST_POPULAR_SONGS = (
    'SELECT SONG.title, SONG.artist, SONG_RANKING.times_listened '
    'FROM ('
        'SELECT song_id, COUNT(*) as times_listened '
        'FROM LISTENED_SONG '
        'GROUP BY song_id '
        'ORDER BY times_listened DESC LIMIT 10'
    ') as SONG_RANKING '
    'LEFT JOIN SONG '
    'WHERE SONG.id = SONG_RANKING.song_id')

# 2. task query
# Finds 10 users with the biggest number of listened unique songs, sorted descending by number of songs
MOST_ACTIVE_USERS = (
    'SELECT user_id, COUNT(DISTINCT song_id) as times_listened '
    'FROM LISTENED_SONG '
    'GROUP BY user_id '
    'ORDER BY times_listened '
    'DESC LIMIT 10')

# 3. task query
# Finds the most popular artist
MOST_POPULAR_ARTIST = (
    'SELECT SONG.artist, COUNT(*) as times_listened '
    'FROM LISTENED_SONG '
    'JOIN SONG '
    'WHERE LISTENED_SONG.song_id = SONG.id '
    'GROUP BY SONG.artist '
    'ORDER BY times_listened DESC '
    'LIMIT 1')

# 4. task query
# Counts the number of listened songs in months
LISTENS_IN_MONTHS = (
    'SELECT DATE.month, COUNT(*) as times_listened '
    'FROM LISTENED_SONG '
    'JOIN DATE '
    'WHERE LISTENED_SONG.date_id = DATE.id '
    'GROUP BY DATE.month '
    'ORDER BY DATE.month')

# 5. task query
# Finds users who listened to 3 most popular songs of Queen
QUEEN_FANS = (
    'SELECT user_id '
    'FROM LISTENED_SONG '
    'WHERE song_id IN ('
        'SELECT l.song_id '
        'FROM LISTENED_SONG as l '
        'JOIN SONG '
        'WHERE SONG.artist LIKE "Queen" AND l.song_id = SONG.id '
        'GROUP BY l.song_id '
        'ORDER BY COUNT(l.song_id) DESC '
        'LIMIT 3) '
    'GROUP BY user_id '
    'HAVING COUNT(DISTINCT LISTENED_SONG.song_id) >= 3 '
    'ORDER BY user_id '
    'LIMIT 10')


class MilionSongDataset:

    def __init__(self, db_name, tracks_path, triplets_path, encoding = 'ISO-8859-1'):
        self.db = sql.connect(db_name)
        self.cursor = self.db.cursor()
        self.create_tables()
        self.load_tracks_file(tracks_path, encoding)
        self.load_triplets_file(triplets_path, encoding)
        self.db.commit()

    def create_tables(self):
        self.cursor.execute(CREATE_SONG_TABLE)
        self.cursor.execute(CREATE_DATE_TABLE)
        self.cursor.execute(CREATE_LISTENED_SONG_TABLE)
                
    def load_tracks_file(self, path, encoding):
        with open(path, 'r', encoding = encoding) as tracks:
            for track in tracks:
                self.cursor.execute('INSERT OR IGNORE INTO SONG VALUES (?, ?, ?, ?)', track.split('<SEP>'))

    def load_triplets_file(self, path, encoding):
        with open(path, 'r', encoding = encoding) as triplets:
            for triplet in triplets:
                split = triplet.split('<SEP>')
                self.cursor.execute('INSERT INTO LISTENED_SONG VALUES (?, ?, ?)', split)
                date = dt.utcfromtimestamp(int(split[2]))
                date = [split[2], date.year, date.month, date.day, date.hour, date.minute, date.second]
                self.cursor.execute('INSERT OR IGNORE INTO DATE VALUES (?, ?, ?, ?, ?, ?, ?)', date)
                
    def do_task(self, task, output_format = '{} {}'):
        res = self.cursor.execute(task).fetchall()
        for r in res:
            print(output_format.format(*r).replace('\n', ''))
       

if __name__ == '__main__':
    dt = MilionSongDataset('MilionSongs.db', './unique_tracks.txt', './triplets_sample_20p.txt')
    dt.do_task(MOST_POPULAR_SONGS,'{} {} {}')
    dt.do_task(MOST_ACTIVE_USERS)
    dt.do_task(MOST_POPULAR_ARTIST)
    dt.do_task(LISTENS_IN_MONTHS)
    dt.do_task(QUEEN_FANS, '{}')


