import sqlite3
import time

conn = sqlite3.connect('C:/BigData/reddit.db')
subreddits_iterator = conn.cursor()
cursor = conn.cursor()
vocabularies_list = []

# Copyright to David Kofoed Wind
def get_words_from_string(s):
    symbols = ['\n', '`', '~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '{', '[', ']', '}',
               '|', '\\', ':', ';', '"', "'", '<', '>', '.', '?', '/', ',']
    s = s.lower()
    for sym in symbols:
        s = s.replace(sym, " ")
    words = set()
    for w in s.split(" "):
        if len(w.replace(" ", "")) > 0:
            words.add(w)
    return words

def iterate_over_subreddits():
    start_time = time.time()
    subreddits_iterator.execute("SELECT id FROM subreddits LIMIT 1")
    for row in subreddits_iterator:
        size = calculate_subreddit_vocabulary_size(row[0])
        vocabularies_list.append((row, size))
    print(vocabularies_list)
    print("Runing time: %s seconds" % (time.time() - start_time))

def calculate_subreddit_vocabulary_size(subreddit_id):
    unique_words = set()
    cursor.execute("SELECT comm.body "
                   "FROM subreddits sub INNER JOIN comments comm "
                   "WHERE sub.id = ?", (subreddit_id,))
    for row in cursor:
        unique_words.update(get_words_from_string(row[0]))

    return len(unique_words)

iterate_over_subreddits()