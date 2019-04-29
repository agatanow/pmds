//Read data
/*val songs = spark.read.
    option("delimiter", "," ).
   csv("./star/songs.txt").toDF("song_id", "track_long_id", "song_long_id", "artist", "song" )

val users = spark.read.
    option("delimiter", "," ).
    csv("./star/users.txt").toDF("user_id", "user_long_id" )

val dates = spark.read.
    option("delimiter", "," ).
   csv("./star/dates.txt").toDF("date_id", "year", "month", "day" )

val facts = spark.read.
   option ( "delimiter", "," ).
    csv("./star/facts.txt").
    toDF("id", "user_id", "song_id" , "date_id")


//task 1 The most  popular  songs
facts.groupBy( "song_id" ) .
    count.
    join(songs, facts("song_id")===songs("song_id")).
    select("song", "count" ).
    orderBy(desc("count") ).
    show(10)

*/ 
//task 2 mosy active users
facts.select("user_id", "song_id").
    distinct.
    groupBy("user_id").
    count.
    orderBy(desc("count")).
    limit(10).
    join(users,"user_id").
    orderBy(desc("count")).
    select("user_long_id", "count").
    show(false)
/*
//task 3 The most popular artist
facts.join(songs, "song_id").
    groupBy( "artist" ).
    count.
    orderBy(desc("count") ).
    show(1, false)

//task 4 listens in months
facts.join(dates, "date_id").
    groupBy("month").
    count.
    select("month", "count").
    orderBy(asc("month")).
    show(false)

// task 5 queen fans
val three_songs = facts.join(songs, "song_id").
  where(songs("artist") === "Queen").
    groupBy("song_id").
    count.
    select("song_id", "count").
    orderBy(desc("count")).
    limit(3).
    select("song_id")
three_songs.show(false)

three_songs.join(facts, "song_id").
    select("user_id", "song_id").
    distinct.
    groupBy("user_id").
    count.
    filter(col("count")===3).
    join(users, "user_id").
    select("user_long_id").
    orderBy("user_long_id").
   limit(10).
    show(false)


*/
