##### Import Libraries #####
import pandas as pd
import matplotlib.pyplot as plt
from math import sqrt
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.mllib.clustering import KMeans ## KMeans Clustering

##### Setup Context & Session #####
sc = SparkContext('local', 'spark_app')
spark = SparkSession.builder.getOrCreate()

##### Load the Points Dataset ####
file_path = 'PySpark/5000_points.txt'

## Load the dataset into a RDD
clusterRDD = sc.textFile(file_path)

## Split the RDD based on tab
rdd_split = clusterRDD.map(lambda x: x.split('\t'))

## Transform the split RDD by creating a list of integers
rdd_split_int = rdd_split.map(lambda x: [int(x[0]), int(x[1])])

## Count the number of rows in RDD
print("There are {} rows in the rdd_split_int dataset".format(rdd_split_int.count()))

##### K-Means Training #####
## Error Function
def error(point):
    center = model.centers[model.predict(point)]
    return sqrt(sum([x ** 2 for x in (point - center)]))

## Train the model with clusters from 13 to 16 and compute WSSSE
clusters_wssse = []

for clst in range(1, 21):
    model = KMeans.train(rdd_split_int, clst, seed=1)
    WSSSE = rdd_split_int.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    clusters_wssse.append([clst, WSSSE])
    print("The cluster {} has Within Set Sum of Squared Error {}".format(clst, WSSSE))

## Train the model again with the best k
model = KMeans.train(rdd_split_int, k=15, seed=1)

## Get cluster centers
cluster_centers = model.clusterCenters

##### Visual the Clusters #####
## Convert rdd_split_int RDD into Spark DataFrame
rdd_split_int_df = spark.createDataFrame(rdd_split_int, schema=["col1", "col2"])

## Convert Spark DataFrame into Pandas DataFrame
rdd_split_int_df_pandas = rdd_split_int_df.toPandas()

## Convert "cluster_centers" that you generated earlier into Pandas DataFrame
cluster_centers_pandas = pd.DataFrame(cluster_centers, columns=["col1", "col2"])

## Create an overlaid scatter plot
plt.scatter(rdd_split_int_df_pandas["col1"], rdd_split_int_df_pandas["col2"])
plt.scatter(cluster_centers_pandas["col1"], cluster_centers_pandas["col2"], color="red", marker="x")
plt.show()