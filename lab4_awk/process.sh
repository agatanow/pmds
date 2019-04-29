#!/bin/bash

#configuration
WORK_DIR="."
##INPUT
UNIQUE_TRACKS="input_data/unique_tracks_utf8.txt"
TRIPLETS="input_data/triplets_sample_20p_utf8.txt"

##OUTPUT
SONGS="songs.txt"
USERS="users.txt"
PLAYED_SONGS="played_songs.txt"
DATES="dates.txt"

#CONSTANTS (don't touch)
UTRACKS_PATH="$WORK_DIR/$UNIQUE_TRACKS"
TRIPLETS_PATH="$WORK_DIR/$TRIPLETS"
SONGS_PATH="$WORK_DIR/$SONGS"
USERS_PATH="$WORK_DIR/$USERS"
PSONGS_PATH="$WORK_DIR/$PLAYED_SONGS"
DATES_PATH="$WORK_DIR/$DATES"

#if input files don't exist don't do anything
if [ ! -f $TRIPLETS_PATH ]; then
    echo "Triplets file ($TRIPLETS_PATH) doesn't exist!"
    exit 1
fi

if [ ! -f $UTRACKS_PATH ]; then
    echo "Triplets file ($UTRACKS_PATH) doesn't exist!"
    exit 1
fi

#if output files exist remove them
if [ -f $SONGS_PATH ]; then
    if ! rm $SONGS_PATH; then
        echo "Can't remove existing output file ($SONGS_PATH)"
        exit 1
    fi
fi

if [ -f $USERS_PATH ]; then
    if ! rm $USERS_PATH; then
        echo "Can't remove existing output file ($USERS_PATH)"
        exit 1
    fi
fi

if [ -f $DATES_PATH ]; then
    if ! rm $DATES_PATH; then
        echo "Can't remove existing output file ($DATES_PATH)"
        exit 1
    fi
fi

if [ -f $PSONGS_PATH ]; then
    if ! rm $PSONGS_PATH; then
        echo "Can't remove existing output file ($PSONGS_PATH)"
        exit 1
    fi
fi

#transform data to csv and star schema
awk -v songs="$SONGS_PATH" -v users="$USERS_PATH" -v dates="$DATES_PATH" -v psongs="$PSONGS_PATH" -F'<SEP>' \
'FNR == NR && !($2 in songs_map) { songs_map[$2] = ++songs_counter; printf "%s,%s,%s,%s,%s\n", songs_counter, $1, $2, $3, $4 > songs; next };'\
'FNR != NR && !($1 in users_map) { users_map[$1] = ++users_counter; printf "%s,%s\n", users_counter, $1 > users };'\
'FNR != NR && (tmp = strftime("%Y,%m,%d", $3,1)) && !(tmp in dates_map) { dates_map[tmp] = ++dates_counter; printf "%s,%s\n", dates_counter, tmp > dates };'\
'FNR != NR { printf "%s,%s,%s,%s\n", ++psongs_counter, users_map[$1], songs_map[$2], dates_map[tmp] > psongs }' \
$UTRACKS_PATH $TRIPLETS_PATH 

# #task 1
# awk -F',' \
# '{ count[$3]++ };'\
# 'END { for (key in count) { printf "%s,%s\n", key, count[key]} }' $PSONGS_PATH | sort -t, -rnk2 | head -n 10 | \
# awk -F',' \
# 'FNR == NR { values[$1] = $2; next };'\
# '$1 in values { printf "%s,%s,%s\n", $5, $4, values[$1] }' \
# - $SONGS_PATH | sort -t, -rnk3 | sed 's/,/ /g'

# #task 2
# awk -F',' \
# 'FNR == NR { users_map[$1] = $2; next };'\
# '!unique[$2, $3]++ { count[$2]++ };'\
# 'END { for (key in count) { printf "%s %s\n", users_map[key], count[key]} }' $USERS_PATH $PSONGS_PATH | sort -t' ' -rnk2 | head -n 10

# #task 3
# awk -F',' \
# 'FNR == NR { artists_map[$1] = $4; next };'\
# '{ count[artists_map[$3]]++ };'\
# 'END { for (key in count) { printf "%s %s\n", key, count[key]} }' \
# $SONGS_PATH $PSONGS_PATH | sort -t' ' -rnk2 | head -n 1

# #task 4
# awk -F',' \
# 'FNR == NR { months_map[$1] = $3; next };'\
# '{ count[months_map[$4]]++ };'\
# 'END { for (key in count) { printf "%s %s\n", key, count[key]} }' \
# $DATES_PATH $PSONGS_PATH | sort -t' ' -nk1

# #task 5
# awk -F',' \
# 'FNR == NR { if ($4 == "Queen") queen_songs[$1]; next };'\
# '$3 in queen_songs { count[$3]++ };'\
# 'END { for (key in count) { printf "%s,%s\n", key, count[key]} }' \
# $SONGS_PATH $PSONGS_PATH | sort -t',' -rnk2 | head -n 3 | \
# awk -v users="$USERS_PATH" -v psongs="$PSONGS_PATH" -F',' \
# 'FILENAME == "-" { queen_top[$1] ; next }'\
# 'FILENAME == psongs { if (($3 in queen_top) && !unique[$2, $3]++) count[$2]++; next };'\
# 'FILENAME == users { if (count[$1] >= 3) print $2 }' \
# - $PSONGS_PATH $USERS_PATH | sort | head -n 10
