val mfile = sc.textFile("./data2/M.txt")
val nfile = sc.textFile("./data2/N.txt")


val m = mfile.map(line => { val split = line.split(" "); (split(1).trim.toInt, (split(0).trim.toInt, split(2).trim.toDouble)) })
val n = nfile.map(line => { val split = line.split(" "); (split(0).trim.toInt, (split(1).trim.toInt, split(2).trim.toDouble)) })



val res = m.join(n).
    map{ case (k, ( ( i, mval), (j, nval) ) ) => (( i.toString, j.toString), mval * nval) }.
    reduceByKey( (x,y) => x + y ).
    sortByKey(true).collect().foreach(println)

