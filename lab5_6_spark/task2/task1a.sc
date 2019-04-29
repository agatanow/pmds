
val grouped = data.map( x => ( x._1, (1, x._2, x._2 * x._2 ))).reduceByKey( (x,y) => (x._1 + y._1, x._2 + y._2, x._3 + y._3) )

grouped.cache()
grouped.take(1)

// from groups
grouped.mapValues( x => (x._1, x._2/x._1, math.sqrt((x._3 - (x._2*x._2)/x._1)/x._1) )).toDF("nr","stats").orderBy("_1").show(false)


// global from groups
val asd = grouped.map( x => x._2 ).reduce( (x,y) => (x._1 + y._1, x._2 + y._2, x._3 + y._3) )
// print global stats nicely
List(("n", asd._1),
     ("mean", asd._2/asd._1), 
     ("variance", (asd._3 - (asd._2*asd._2)/asd._1)/asd._1), 
     ("st_dev", math.sqrt((asd._3 - (asd._2*asd._2)/asd._1)/asd._1)) ).mkString("\n")

