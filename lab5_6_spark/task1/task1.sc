val textFile = spark.read.textFile("../data/all-shakespeare")
val counts = (textFile.flatMap(line => line.split("\\s+")).map(word => (word, 1)).reduceByKey(_._2+_._2).sortBy(_._2))
counts.toDF.orderBy("_1").show