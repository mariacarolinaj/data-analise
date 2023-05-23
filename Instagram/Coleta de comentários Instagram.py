# -*- coding: utf-8 -*-
"""
Created on Mon May 22 19:29:26 2023

@author: Maria
"""

import csv
import instaloader

post_url = 'https://www.instagram.com/p/Cp8IY4FPKlF/'

il = instaloader.Instaloader()
    
usernameLogin = 'sortsapFak'

il.load_session_from_file(usernameLogin)
    
post = instaloader.Post.from_shortcode(il.context, 'Cp8IY4FPKlF')

comments = []

for comment in post.get_comments():
    comment_id = comment.id
    comment_author = comment.owner.username
    comment_content = comment.text
    comment_like_count = comment.likes_count
    comment_created_at = comment.created_at_utc

    comments.append([comment_id, comment_author, comment_content, comment_like_count, comment_created_at])

    if len(comments) >= 150:
        break

with open('Instagram_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'user/name', 'full_text', 'favorite_count', 'created_at'])

    for comment in comments:
        writer.writerow(comment)

print('Os dados da publicação foram armazenados no arquivo com sucesso.')
