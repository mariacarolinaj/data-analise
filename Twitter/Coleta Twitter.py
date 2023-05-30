# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 11:06:01 2023

@author: Maria
"""

import tweepy

apiKey = "dVpFRlNRcWltVHRneGxsWWxGc1o6MTpjaQ"
apiSecretKey = "SM6KDUzKTeI4usO3yzYJD0ltaRVfEdWmdtniPzpmkqq2fUMr_N"
accessToken = "1064921435175616512-NzI0VktpqrBDBw4yIc6vjTX9Vi8dM2"
accessTokenSecret = "c5boxh6V1ABGN0zpjKwJ1hkOFCyK3IdGQvu9wo05psf6U"

auth = tweepy.OAuthHandler(apiKey, apiSecretKey)
auth.set_access_token(accessToken, accessTokenSecret)
api = tweepy.API(auth)

user = api.get_user(screen_name="m_ariacarolin_a")
followers_ids = api.followers_ids(user_id=user.id)

followers = api.lookup_users(user_ids=followers_ids)
for follower in followers:
    print(follower.name)


