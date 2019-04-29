
val grouped = data.map( x => ( x._1, (1, x._2, x._2 * x._2 ))).reduceByKey( (x,y) => (x._1 + y._1, x._2 + y._2, x._3 + y._3) )
// from groups
grouped.mapValues( x => (x._1, x._2/x._1, math.sqrt((x._3 - (x._2*x._2)/x._1)/x._1) )).toDF("nr","stats").orderBy("_1").show(false)



//global by itself
val dsa = data.map( x => ( x._1, (1, x._2, x._2 * x._2 ))).map(x => x._2).reduce( (x,y) => (x._1 + y._1, x._2 + y._2, x._3 + y._3) )
// print global stats nicely
List(("n", dsa._1),
     ("mean", dsa._2/dsa._1), 
     ("variance", (dsa._3 - (dsa._2*dsa._2)/dsa._1)/dsa._1), 
     ("st_dev", math.sqrt((dsa._3 - (dsa._2*dsa._2)/dsa._1)/dsa._1)) ).mkString("\n")

