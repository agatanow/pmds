import  scala.util.Random

// generate data
val  groups = Map( 0 -> (0,1), 1 -> (1,1), 2 -> (2,2),  3 -> (3,3), 4 -> (4,3), 5 -> (5,2), 6 -> (6,1) )
val n = 100000
val  random = Random
val data = sc.parallelize(for (i <- 1 to n) yield { val g = random.nextInt (7) ; val (mu, sigma ) = groups(g); (g, mu + sigma*random.nextGaussian() ) })



