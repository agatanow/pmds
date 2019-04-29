val matrixFile = sc.textFile("../data/M.txt")
val vectorFile = sc.textFile("../data/v.txt")
val vector = vectorFile.map(line => { val split = line.split(","); (split(0).trim.toInt, split(1).trim.toDouble) }).map{case(i ,v) => v}.collect
val vector_b = sc.broadcast(vector)
val matrix = matrixFile.map(line => { val split = line.split(","); (split(0).trim.toInt, split(1).trim.toInt, split(2).trim.toDouble) })
val result = matrix.map{case (i, j, a) => (i, a * vector_b.value(j-1))}.reduceByKey(_+_)
result.toDF.orderBy("_1").show