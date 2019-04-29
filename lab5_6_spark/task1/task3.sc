val iter = 100
val hits = sc.parallelize((1 to iter).map( x => { val x = math.random; val y = math.random; if (x*x + y*y < 1) (1, 1) else (1, 0)})).reduceByKey(_+_)
val pi = 4.0 * hits.take(1).last._2 / iter