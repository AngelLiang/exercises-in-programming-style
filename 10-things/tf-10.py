#!/usr/bin/env python
import sys, re, operator, string
from abc import ABCMeta

#
# The classes
#
class TFExercise():
    __metaclass__ = ABCMeta

    def info(self):
        return self.__class__.__name__

class DataStorageManager(TFExercise):
    """ Models the contents of the file """

    def __init__(self, path_to_file):
        """
        从程序外部获取文本数据，并将其转化为能被应用程序其他部分所使用的单词。
        本类是用来处理与问题文本数据输入相关的数据和行为的抽象。

        :param path_to_file: str, 文件路径
        """
        with open(path_to_file) as f:
            self._data = f.read()
        pattern = re.compile('[\W_]+')
        self._data = pattern.sub(' ', self._data).lower()

    def words(self):
        """ Returns the list words in storage """
        return self._data.split()

    def info(self):
        return super(DataStorageManager, self).info() + ": My major data structure is a " + self._data.__class__.__name__

class StopWordManager(TFExercise):
    """ Models the stop word filter """

    def __init__(self):
        """向应用程序其他部分提供鉴别停止词的服务。"""
        # 获取停止词
        with open('../stop_words.txt') as f:
            self._stop_words = f.read().split(',')
        # add single-letter words
        self._stop_words.extend(list(string.ascii_lowercase))

    def is_stop_word(self, word):
        """鉴别停止词"""
        return word in self._stop_words

    def info(self):
        return super(StopWordManager, self).info() + ": My major data structure is a " + self._stop_words.__class__.__name__

class WordFrequencyManager(TFExercise):
    """ Keeps the word frequency data """
    
    def __init__(self):
        """用于管理单词技术，其内部使用了字典来实现单词与计数的映射。"""
        self._word_freqs = {}

    def increment_count(self, word):
        if word in self._word_freqs:
            self._word_freqs[word] += 1
        else:
            self._word_freqs[word] = 1

    def sorted(self):
        return sorted(self._word_freqs.items(), key=operator.itemgetter(1), reverse=True)

    def info(self):
        return super(WordFrequencyManager, self).info() + ": My major data structure is a " + self._word_freqs.__class__.__name__

class WordFrequencyController(TFExercise):
    """程序的入口"""

    def __init__(self, path_to_file):
        # 组合各种 Manager
        self._storage_manager = DataStorageManager(path_to_file)
        self._stop_word_manager = StopWordManager()
        self._word_freq_manager = WordFrequencyManager()

    def run(self):
        """主方法"""
        for w in self._storage_manager.words():
            if not self._stop_word_manager.is_stop_word(w):
                self._word_freq_manager.increment_count(w)

        word_freqs = self._word_freq_manager.sorted()
        for (w, c) in word_freqs[0:25]:
            print(w, ' - ', c)

#
# The main function
#
WordFrequencyController(sys.argv[1]).run()
