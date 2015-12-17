__author__ = 'acton'
import os
from pyspark import SparkContext, SparkConf
from pyspark.mllib.recommendation import ALS
import math
import json


class  BigDataProcessor(object):
    sc = SparkContext()
    #ratings_path = "file:///Users/acton/Documents/BX/Ratings.csv"
    #ratings_path = "file:///Users/acton/Documents/BX/RatingsNew.csv"
    #books_path = "file:///Users/acton/Documents/BX/BooksNew.csv"
    users_path = "file:///Users/acton/Documents/BX/Users.csv"
    ratings_path = "file:///Users/zeweijiang/Documents/ratings.csv"
    books_path = "file:///Users/zeweijiang/Documents/books.csv"
    ratings = None
    books = None

    def __init__(self):
        self.loadRDDs()

    def loadRDDs(self):

        self.ratings = self.sc.textFile(self.ratings_path)\
        .map(lambda line: line.split(","))\
        .map(lambda tokens: (tokens[0][1:-1],tokens[1][1:-1],tokens[2][1:-1]))\
        .cache()

        self.books = self.sc.textFile(self.books_path)\
        .map(lambda line: line.split(","))\
        .map(lambda tokens: (tokens[0][1:-1],tokens[1][1:-1],tokens[2][1:-1],tokens[3][1:-1],tokens[5][1:-1]))\
        .cache()

        users = self.sc.textFile(self.users_path)\
        .map(lambda line: line.split(","))\
        .map(lambda tokens: (tokens[0][1:-1],tokens[1][1:-1]))\
        .cache()

    def getUserRatingRDD(self,new_user_ratings):
        #get ratings from front-end user input
        new_user_ID = 0
        new_user_ratings_RDD = self.sc.parallelize(new_user_ratings)
        return new_user_ratings_RDD, new_user_ID

    def getIncrementedRatingsRDD(self,new_user_ratings):
        new_user_ratings_RDD,new_user_ID = self.getUserRatingRDD(new_user_ratings)
        complete_data_with_new_ratings_RDD = self.ratings.union(new_user_ratings_RDD)
        return complete_data_with_new_ratings_RDD, new_user_ratings_RDD, new_user_ID



    def collaborativeFilter(self,new_user_ratings):
        seed = 5L
        iterations = 10
        regularization_parameter = 0.1
        #best_rank is pre-tuned
        best_rank = 8

        complete_data_with_new_ratings_RDD,new_user_ratings_RDD, new_user_ID = self.getIncrementedRatingsRDD(new_user_ratings)
        new_ratings_model = ALS.train(complete_data_with_new_ratings_RDD, best_rank, seed=seed, \
                              iterations=iterations, lambda_=regularization_parameter)

        new_user_ratings_ids = map(lambda x: x[1], new_user_ratings) # get just book IDs

        new_user_unrated_books_RDD = (self.books.filter(lambda x: x[0] not in new_user_ratings_ids).map(lambda x: (new_user_ID, x[0])))
        new_user_recommendations_RDD = new_ratings_model.predictAll(new_user_unrated_books_RDD)

        complete_books_titles = self.books.map(lambda x: (int(x[0]),x[1]))
        complete_books_authors = self.books.map(lambda x: (int(x[0]),x[2]))
        complete_books_publiers = self.books.map(lambda x: (int(x[0]),x[3]))
        complete_books_imgs = self.books.map(lambda x: (int(x[0]),x[4]))

        def get_counts_and_averages(id_and_ratings_tuple):
            nratings = len(id_and_ratings_tuple[1])
            return id_and_ratings_tuple[0], (nratings, float(sum(int(x) for x in id_and_ratings_tuple[1]))/nratings)

        book_ID_with_ratings_RDD = (self.ratings.map(lambda x: (x[1], x[2])).groupByKey())
        book_ID_with_avg_ratings_RDD = book_ID_with_ratings_RDD.map(get_counts_and_averages)
        book_rating_counts_RDD = book_ID_with_avg_ratings_RDD.map(lambda x: (int(x[0]), x[1][0]))

        new_user_recommendations_rating_RDD = new_user_recommendations_RDD.map(lambda x: (x.product, x.rating))

        new_user_recommendations_rating_title_and_count_RDD = \
            new_user_recommendations_rating_RDD.join(complete_books_titles).join(complete_books_authors)\
                .join(complete_books_publiers).join(complete_books_imgs).join(book_rating_counts_RDD)

        new_user_recommendations_rating_title_and_count_RDD = \
            new_user_recommendations_rating_title_and_count_RDD.map\
                (lambda r: (r[1][0][0][0][0][1], r[1][0][0][0][0][0],r[1][0][0][0][1],r[1][0][0][1],r[1][0][1], r[1][1]))

        top_books = new_user_recommendations_rating_title_and_count_RDD.filter(lambda r: r[5]>10).takeOrdered(25, key=lambda x: -x[1])
        #return a jason list in of order of : book_name, predict_rating,author,publisher,url, review_cnt
        print top_books
        return json.dumps(top_books)

    def returnRecommendation(self):
        self.collaborativeFilter()



if __name__ == '__main__':
    bdp = BigDataProcessor()
    new_user_ratings = [
        (0,16,8),
        (0,17,7),
        (0,18,5)
    ]
    bdp.collaborativeFilter(new_user_ratings)

