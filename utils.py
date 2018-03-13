import numpy as np
import re


def get_vector_average(vectors):
  if len(vectors) == 0:
    raise ValueError("No vectors passed")
  vectors = np.asarray(vectors)
  if len(vectors.shape) != 2:
    raise ValueError("Vectors passed must be of the same dimensionality")
  return np.mean(vectors, axis=0)


def get_stopwords():
  return [
    u'i',
    u'me',
    u'my',
    u'myself',
    u'we',
    u'our',
    u'ours',
    u'ourselves',
    u'you',
    u'your',
    u'yours',
    u'yourself',
    u'yourselves',
    u'he',
    u'him',
    u'his',
    u'himself',
    u'she',
    u'her',
    u'hers',
    u'herself',
    u'it',
    u'its',
    u'itself',
    u'they',
    u'them',
    u'their',
    u'theirs',
    u'themselves',
    u'what',
    u'which',
    u'who',
    u'whom',
    u'this',
    u'that',
    u'these',
    u'those',
    u'am',
    u'is',
    u'are',
    u'was',
    u'were',
    u'be',
    u'been',
    u'being',
    u'have',
    u'has',
    u'had',
    u'having',
    u'do',
    u'does',
    u'did',
    u'doing',
    u'a',
    u'an',
    u'the',
    u'and',
    u'but',
    u'if',
    u'or',
    u'because',
    u'as',
    u'until',
    u'while',
    u'of',
    u'at',
    u'by',
    u'for',
    u'with',
    u'about',
    u'against',
    u'between',
    u'into',
    u'through',
    u'during',
    u'before',
    u'after',
    u'above',
    u'below',
    u'to',
    u'from',
    u'up',
    u'down',
    u'in',
    u'out',
    u'on',
    u'off',
    u'over',
    u'under',
    u'again',
    u'further',
    u'then',
    u'once',
    u'here',
    u'there',
    u'when',
    u'where',
    u'why',
    u'how',
    u'all',
    u'any',
    u'both',
    u'each',
    u'few',
    u'more',
    u'most',
    u'other',
    u'some',
    u'such',
    u'no',
    u'nor',
    u'not',
    u'only',
    u'own',
    u'same',
    u'so',
    u'than',
    u'too',
    u'very',
    u's',
    u't',
    u'can',
    u'will',
    u'just',
    u'don',
    u'should',
    u'now']


def expand_contractions(s):
  ''' Takes a string as input, expands the contracted forms in it and returns the result. '''
  # Source:
  # http://www.englishcoursemalta.com/learn/list-of-contracted-forms-in-english/
  c = {'i\'m': 'i am',
       'you\'re': 'you are',
       'he\'s': 'he is',
       'she\'s': 'she is',
       'we\'re': 'we are',
       'it\'s': 'it is',
       'isn\'t': 'is not',
       'aren\'t': 'are not',
       'they\'re': 'they are',
       'there\'s': 'there is',
       'wasn\'t': 'was not',
       'weren\'t': ' were not',
       'i\'ve': 'i have',
       'you\'ve': 'you have',
       'we\'ve': 'we have',
       'they\'ve': 'they have',
       'hasn\'t': 'has not',
       'haven\'t': 'have not',
       'you\'d': 'you had',
       'he\'d': 'he had',
       'she\'d': 'she had',
       'we\'d': 'we had',
       'they\'d': 'they had',
       'doesn\'t': 'does not',
       'don\'t': 'do not',
       'didn\'t': 'did not',
       'i\'ll': 'i will',
       'you\'ll': 'you will',
       'he\'ll': 'he will',
       'she\'ll': 'she will',
       'we\'ll': 'we will',
       'they\'ll': 'they will',
       'there\'ll': 'there will',
       'i\'d': 'i would',
       'it\'d': 'it would',
       'there\'d': 'there had',
       'there\'d': 'there would',
       'can\'t': 'can not',
       'couldn\'t': 'could not',
       'daren\'t': 'dare not',
       'hadn\'t': 'had not',
       'mightn\'t': 'might not',
       'mustn\'t': 'must not',
       'needn\'t': 'need not',
       'oughtn\'t': 'ought not',
       'shan\'t': 'shall not',
       'shouldn\'t': 'should not',
       'usedn\'t': 'used not',
       'won\'t': 'will not',
       'wouldn\'t': 'would not',
       'what\'s': 'what is',
       'that\'s': 'that is',
       'who\'s': 'who is', }
  # Some forms of 's could either mean 'is' or 'has' but we've made a choice here.
  # Some forms of 'd could either mean 'had' or 'would' but we've made a choice here.
  # Some forms of 'll could wither mean 'will' or 'shall' but we've made a
  # choice here.
  for pat in c:
    s = re.sub(pat, c[pat], s)
  return s


def general_cleaning(s, remove_punct=False):
  ''' Takes a string as input and False or True for the argument 'remove_punct'.
    Depending on the value of 'remove_punct', all punctuation is either removed, or a space is added before and after.
    In both cases the punctuation un URLs and numbers is retained.

    Also transforms "&amp;" into "and", and removes all other HTML entities.
    Removes excessive white space. '''

  # Find all URLs and replace them with GGGG to protect them from whitespace
  # addition.
  urlpat = re.compile(r'https?://[^ ]+')
  wwwpat = re.compile(r'www\.[^ ]+')
  compat = re.compile(r'[^ ]+\.com[^ ]+')
  coms = re.findall(compat, s)
  wwws = re.findall(wwwpat, s)
  urls = re.findall(urlpat, s)
  urls += wwws + coms
  n = 0
  newurls = []
  for url in set(urls):
    if re.search(r'\)', url) and not re.search('\(', url):
      url = re.sub(r'\).*$', '', url)
    # Get rid of backslashes because else we get regex problems when trying to
    # put the URLs back.
    if re.search(r'\\', url):
      url = re.sub(r'\\', '/', url)
    s = re.sub(re.escape(url), 'GGGG' + str(n), s)
    newurls.append(url)
    n += 1

  # Protect points, commas and colon in numbers
  while re.search(r'([0-9])\.([0-9])', s):
    s = re.sub(r'([0-9])\.([0-9])', r'\1BBB\2', s)
  while re.search(r'([0-9]),([0-9])', s):
    s = re.sub(r'([0-9]),([0-9])', r'\1CCC\2', s)
  while re.search(r'([0-9]):([0-9])', s):
    s = re.sub(r'([0-9]):([0-9])', r'\1DDD\2', s)

  s = re.sub(r'&amp;', ' and ', s)

  if remove_punct:
    # Remove all sorts of punctuation
    # s = re.sub('[^a-zA-Z0-9_-]', ' ', s) # Too agressive!
    p = re.compile(r'( [a-z] \.)( [a-z] \.)+')
    l = p.finditer(s)
    contains_abbreviations = False
    for m in l:
      contains_abbreviations = True
      # Get rid of white space in abbreviations
      newbit = re.sub(r' ', '', m.group())
      # change dots in abbreviations into 'PPPP'
      newabbr = re.sub(r'\.', 'PPPP', newbit)
      s = re.sub(m.group() + ' +', ' ' + newabbr +
               ' ', s)  # protect abbreviations
      # remove all points that are not in abbreviations
      s = re.sub(r'\.', '', s)
      s = re.sub(newabbr, newbit, s)  # place dots back in abbreviations
    if not contains_abbreviations:
      s = re.sub(r'\.', ' ', s)

    s = re.sub(r',', ' ', s)
    s = re.sub(r'\?', ' ', s)
    s = re.sub(r'!', ' ', s)
    s = re.sub(r' \'([a-z])', r'  \1', s)
    s = re.sub(r'([a-z])\' ', r'\1 ', s)
    s = re.sub(r' \"([a-z])', r' \1', s)
    s = re.sub(r'([a-z])\" ', r'\1 ', s)
    s = re.sub(r'\(', ' ', s)
    s = re.sub(r'\)', ' ', s)
    s = re.sub(r'\[', ' ', s)
    s = re.sub(r'\]', ' ', s)
    s = re.sub(r'([a-z]): ', r'\1 ', s)
    s = re.sub(r';', ' ', s)
    s = re.sub(r" - ", " ", s)
    s = re.sub(r"- ", " ", s)
    s = re.sub("=", "", s)
    s = re.sub("`", "", s)
    s = re.sub('"', '', s)
    s = re.sub('#', '', s)
  else:
    # Add space around all sorts of punctuation.
    # s = re.sub('([^a-zA-Z0-9_-])', r' \1 ', s) # Too agressive!
    s = re.sub(r'\.', ' . ', s)

    # Remove space around abbreviations
    p = re.compile(r'( [a-z] \.)( [a-z] \.)+')
    for m in p.finditer(s):
      newbit = re.sub(' ', '', m.group())
      s = re.sub(m.group() + ' +', ' ' + newbit + ' ', s)

    s = re.sub(r',', ' , ', s)
    s = re.sub(r'\?', ' ? ', s)
    s = re.sub(r'!', ' ! ', s)
    s = re.sub(r' \'([a-z])', r" ' \1", s)
    s = re.sub(r'([a-z])\' ', r"\1 ' ", s)
    s = re.sub(r' \"([a-z])', r' " \1', s)
    s = re.sub(r'([a-z])\" ', r'\1 " ', s)
    s = re.sub(r'\(', ' ( ', s)
    s = re.sub(r'\)', ' ) ', s)
    s = re.sub(r'\[', ' [ ', s)
    s = re.sub(r'\]', ' ] ', s)
    s = re.sub(r'([a-z]): ', r'\1 : ', s)
    s = re.sub(r';', ' ; ', s)
    s = re.sub(r"'s", " 's", s)

  # Restore points, commas and colons in numbers
  while re.search(r'([0-9])BBB([0-9])', s):
    s = re.sub(r'([0-9])BBB([0-9])', r'\1.\2', s)
  while re.search(r'([0-9])CCC([0-9])', s):
    s = re.sub(r'([0-9])CCC([0-9])', r'\1,\2', s)
  while re.search(r'([0-9])DDD([0-9])', s):
    s = re.sub(r'([0-9])DDD([0-9])', r'\1:\2', s)

  # restore URLs
  # reverse list to GGGG1 does not match GGG10. (Source:
  # http://galvanist.com/post/53478841501/python-reverse-enumerate)
  newurllist = zip(reversed(range(len(newurls))), reversed(newurls))
  for i, u in newurllist:
    # Escaping u here leads to backslashes in URLs.
    s = re.sub('GGGG' + str(i), u, s)

  # Get rid of things we don't want, like HTML entities.
  s = re.sub(r"&[a-z]+;", "", s)
  s = re.sub(r"&#?[a-z]+;", "", s)  # &#xA; == '\n'
  # Remove excessive whitespace
  s = re.sub(r"\s+", " ", s)
  s = re.sub(r"^\s", "", s)
  s = re.sub(r"\s$", "", s)

  return s


def clean_text(s):
  s = s.lower()
  s = re.sub('\n', ' ', s)
  s = re.sub(r"<a href=\"[^\"]+\">([^<]+)</a>", r"\1", s)
  # Put some space between tags and urls or other things. So we don't
  # accidentally remove more than we should a few lines further below this
  # line.
  s = re.sub(r"<", " <", s)
  s = re.sub(r">", "> ", s)
  # Remove all tags except for code tags
  alltags = re.findall(r'(</?)([^>]+)(>)', s)  # list of tuples
  for tag in alltags:
    codetag = tag[0] + tag[1] + tag[2]
    s = re.sub(re.escape(codetag), '', s)

  s = expand_contractions(s)
  s = general_cleaning(s, True)

  s = re.sub(' \. net ', ' .net', s)
  s = re.sub(' i \. e ', ' i.e. ', s)
  # fix extensions
  s = re.sub(' \. jpeg ', '.jpeg ', s)
  s = re.sub(' \. jpg ', '.jpg ', s)

  return s
