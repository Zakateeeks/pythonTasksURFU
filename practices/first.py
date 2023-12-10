# A. donuts
# Given an int count of a number of donuts, return a string
# of the form 'Number of donuts: <count>', where <count> is the number
# passed in. However, if the count is 10 or more, then use the word 'many'
# instead of the actual count.
# So donuts(5) returns 'Number of donuts: 5'
# and donuts(23) returns 'Number of donuts: many'
def donuts(count):
    return f"Number of donuts: {count}" if count < 10 else "Number of donuts: many"


# B. both_ends
# Given a string s, return a string made of the first 2
# and the last 2 chars of the original string,
# so 'spring' yields 'spng'. However, if the string length
# is less than 2, return instead the empty string.
def both_ends(s):
    return s[:2:] + s[-2::] if len(s) >= 2 else ""


# C. fix_start
# Given a string s, return a string
# where all occurences of its first char have
# been changed to '*', except do not change
# the first char itself.
# e.g. 'babble' yields 'ba**le'
# Assume that the string is length 1 or more.
# Hint: s.replace(stra, strb) returns a version of string s
# where all instances of stra have been replaced by strb.
def fix_starts(s):
    return s[0] + s[1::].replace(s[0], "*")


# D. MixUp
# Given strings a and b, return a single string with a and b separated
# by a space '<a> <b>', except swap the first 2 chars of each string.
# e.g.
#   'mix', pod' -> 'pox mid'
#   'dog', 'dinner' -> 'dig donner'
# Assume a and b are length 2 or more.
def mix_up(a, b):
    return b[:2:] + a[2::] + " " + a[:2:] + b[2::]


# E. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    if len(s) > 3:
        return s + "ing" if s[-3::] != "ing" else s + "ly"
    else:
        return s


# F. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
    return s.replace(s[s.find("not"):s.find("bad") + 3:], "good") if s.find("not") < s.find("bad") else s


# G. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
    array_with_string = []
    for i in (a, b):
        if len(i) % 2 == 0:
            array_with_string.append(i[:len(i) // 2:])
            array_with_string.append(i[len(i) // 2::])
        else:
            array_with_string.append(i[:len(i) // 2 + 1:])
            array_with_string.append(i[len(i) // 2 + 1::])

    return array_with_string[0] + array_with_string[2] + array_with_string[1] + array_with_string[3]


# Last task
# Посчитать сколько раз встречается каждый человек на сайте
from urllib import request


def last_task():
    page = request.urlopen("http://shannon.usu.edu.ru/ftp/python/hw2/home.html")
    page_text = page.read().decode('cp1251')
    filter_page = page_text[page_text.find('<body>'):page_text.find('</body>'):]
    two_filter_page = filter_page.split("href")
    dict = {}
    years = []
    for i in range(0, len(two_filter_page)):
        years.append(two_filter_page[i][two_filter_page[i].find("<h3>"): two_filter_page[i].find("</h3>")])
        two_filter_page[i] = two_filter_page[i][two_filter_page[i].find(">") + 1:two_filter_page[i].find("<"):]

        dict[two_filter_page[i]] = two_filter_page.count(two_filter_page[i])

    print(str(dict).replace(',', '\n'))
