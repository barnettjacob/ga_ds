
# coding: utf-8

# # Recommendation System

# ### Dr J Rogel-Salazar

# In[1]:

#Let us bring the modules we need

import recsys.algorithm
from recsys.algorithm.factorize import SVD
from recsys.datamodel.data import Data
from recsys.evaluation.prediction import RMSE, MAE
from recsys.utils.svdlibc import SVDLIBC


# In[2]:

# enable verbose output
recsys.algorithm.VERBOSE = True


# In[3]:
# Formatting the data
svd = SVD()
recsys.algorithm.VERBOSE = True

    # load movielens data
dat_file = './ml-1m/ratings.dat'
svd.load_data(filename=dat_file, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': int})
 # About format parameter:
        #   'row': 1 -> Rows in matrix come from column 1 in ratings.dat file
        #   'col': 0 -> Cols in matrix come from column 0 in ratings.dat file
        #   'value': 2 -> Values (Mij) in matrix come from column 2 in ratings.dat
        #   file
        #   'ids': int -> Ids (row and col ids) are integers (not strings)

# In[4]:

# compute svd
k = 100
svd.compute(k=k, min_values=10, pre_normalize=None, mean_center=True,
    post_normalize=True)


# In[5]:

# movie id's
ITEMID1 = 1      # toy story
ITEMID2 = 1221   # godfather II

# How similar are these films
svd.similarity(ITEMID1, ITEMID2)


# In[6]:

# What about 
ITEMID3 = 2355 # A bug's life
svd.similarity(ITEMID1, ITEMID3)


# In[7]:

# We cen get films similar to Toy Story
svd.similar(ITEMID1)


# In[8]:

# Let us predict the rating for a user and a movie
def WhatRating(USERID, ITEMID):
    # get movies similar to film with ITEMID
    svd.similar(ITEMID)

    # get predicted rating for given user & movie
    MIN_RATING = 0.0
    MAX_RATING = 5.0

    # get predicted rating
    pred = svd.predict(ITEMID, USERID, MIN_RATING, MAX_RATING)
    actual = svd.get_matrix().value(ITEMID, USERID)
    print 'predicted rating = {0}'.format(pred)
    print 'actual rating = {0}'.format(actual)


# In[16]:

USERID = 1
ITEMID = 588
WhatRating(USERID, ITEMID)


# In[14]:

# Furthermore, we can recommend (non-rated) items to a user:
USERID = 1
svd.recommend(USERID, is_row=False) #cols are users and rows are items, thus we set is_row=False


# In[17]:

# Alternatively, who should go and see Toy Story 
#(e.g. which users -that have not rated Toy Story- would give it a high rating?)
svd.recommend(ITEMID1)


# In[18]:

# An example from the documentation
# http://ocelma.net/software/python-recsys/build/html/examples.html
def ex1(dat_file='./ml-1m/ratings.dat',
        pct_train=0.5):

    data = Data()
    data.load(dat_file, sep='::', format={'col':0, 'row':1, 'value':2,'ids':int})
       

    # create train/test split
    train, test = data.split_train_test(percent=pct_train)

    # create svd
    K=100
    svd = SVD()
    svd.set_data(train)
    svd.compute(k=K, min_values=5, pre_normalize=None, mean_center=True, post_normalize=True)

    # evaluate performance
    rmse = RMSE()
    mae = MAE()
    for rating, item_id, user_id in test.get():
        try:
            pred_rating = svd.predict(item_id, user_id)
            rmse.add(rating, pred_rating)
            mae.add(rating, pred_rating)
        except KeyError:
            continue

    print 'RMSE=%s' % rmse.compute()
    print 'MAE=%s' % mae.compute()


# In[19]:

ex1()


# In[ ]:



