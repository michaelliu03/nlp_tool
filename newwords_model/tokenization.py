# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 17:01:07 2020

@author: cm
"""



import six
import unicodedata
import nltk
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from .utils import sentence_split_regex
nltk.download('wordnet')



SPIECE_UNDERLINE = u"▁".encode("utf-8")


def _is_whitespace(char):
    """Checks whether `chars` is a whitespace character."""
    # \t, \n, and \r are technically control characters but we treat them
    # as whitespace since they are generally considered as such.
    if char == " " or char == "\t" or char == "\n" or char == "\r":
        return True
    cat = unicodedata.category(char)
    if cat == "Zs":
        return True
    return False


def _is_control(char):
    """Checks whether `chars` is a control character."""
    # These are technically control characters but we count them as whitespace
    # characters.
    if char == "\t" or char == "\n" or char == "\r":
        return False
    cat = unicodedata.category(char)
    if cat in ("Cc", "Cf"):
        return True
    return False

def convert_to_unicode(text):
    """Converts `text` to Unicode (if it's not already), assuming utf-8 input."""
    if type(text) in [str, bytes]:
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return six.ensure_text(text, "utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        return text

def whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


class BasicTokenizer(object):
    """Runs basic tokenization (punctuation splitting, lower casing, etc.)."""

    def __init__(self, do_lower_case=True):
        """Constructs a BasicTokenizer.

        Args:
          do_lower_case: Whether to lower case the input.
        """
        self.do_lower_case = do_lower_case

    def tokenize(self, text):
        """Tokenizes a piece of text."""
        text = convert_to_unicode(text)
        text = self._clean_text(text)      # 处理空格

        # This was added on November 1st, 2018 for the multilingual and Chinese
        # models. This is also applied to the English models now, but it doesn't
        # matter since the English models were not trained on any Chinese data
        # and generally don't have any Chinese data in them (there are Chinese
        # characters in the vocabulary because Wikipedia does have some Chinese
        # words in the English Wikipedia.).
        # print("text", text)
        orgig_txts = sentence_split_regex(text)

        orig_tokens = []
        for orgig_txt in orgig_txts:
            orig_token = orgig_txt.rstrip().split(" ")     # 将字符串转化为列表 ['usa', '和', 'CHINA', '都', '是', '世', '界', '上', '的', '大', '国', ',Donald', 'Trump', '是', '美', '国', '总', '统']
            orig_tokens.append(orig_token.copy())




        split_tokens = []
        lems = []
        lemmatizer = WordNetLemmatizer()


        for tokens in orig_tokens:
            temp = []
            for token in tokens:

                if self.do_lower_case:
                    token = token.lower()
                # stem = stemmer.stem(token)
                # stems.append(stem)
                lem = lemmatizer.lemmatize(token)
                temp.append(lem)
            lems.append(temp.copy())

        #print(lems)


        orig_tokens = lems
        #print(output_tokens)
        return orig_tokens


    def _clean_text(self, text):
        """Performs invalid character removal and whitespace cleanup on text."""
        output = []
        for char in text:
            cp = ord(char)
            if _is_whitespace(char):   #\t \r \n 用空格代替
                output.append(" ")
            else:
                output.append(char)
        return "".join(output)





class FullTokenizer(object):
    """Runs end-to-end tokenziation."""

    def __init__(self, do_lower_case=True, spm_model_file=None):
        self.basic_tokenizer = BasicTokenizer(do_lower_case=do_lower_case)

    @classmethod
    def from_scratch(cls, do_lower_case, spm_model_file):
        return FullTokenizer(do_lower_case, spm_model_file)

    def tokenize(self, text):
        split_tokens = []
        # print("tokenize", self.basic_tokenizer.tokenize(text))
        for token in self.basic_tokenizer.tokenize(text):
            split_tokens.append(token)
                # print("su_token", self.wordpiece_tokenizer.tokenize(token))

        return split_tokens



if __name__ == '__main__':
    # vocab_file = 'dict/vocabulary.txt'
    tokenizer = FullTokenizer.from_scratch(do_lower_case=True,
                                           spm_model_file=None)
    text = 'stones speaking bedroom jokes lisa purple earrings running '

    print(tokenizer.tokenize(text))
    
    
    










