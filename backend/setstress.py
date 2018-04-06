#!/usr/bin/python
# coding=utf8
"""
Created on 08.09.14
@author: igor"""
import re
import pymorphy2
import csv
import os
from functools import reduce

print(os.getcwd())


def parse_string_stress(k, s):
    splitted = s.split("|")
    try:
        res = tuple([int(x) for x in splitted])
    except ValueError:
        print(k, s, splitted)
        res = ()
    return res


def csv_dct(fl):
    with open(fl) as f:
        return {l[0]: parse_string_stress(l[0], l[1]) for l in csv.reader(f)}


# %timeit d = csv_dct("dict_data/lem_df.csv")
# %timeit d1 = pd.read_csv("dict_data/lem_df.csv",encoding = "utf8",index_col = 0,squeeze = True).to_dict()

def pm_setup():
    # must be a bug in morph:
    # эту - етот
    conv = {u"етот": u"этот"}
    morph = pymorphy2.MorphAnalyzer()

    def pymorphy_lemmas(w):
        return {conv.get(x.normal_form, x.normal_form) for x in morph.parse(w)}

    return pymorphy_lemmas


# comp_df = pd.read_csv("dict_data/lem_df.csv",encoding = "utf8",index_col = 0,squeeze = True).to_dict()
# stss_df = pd.read_csv("dict_data/tok_df.csv",index_col = 0, encoding = "utf8",squeeze = True).to_dict()
# # jo_sr = pd.read_csv("dict_data/jo_sr.csv",encoding = "utf8",index_col = 0,squeeze = True).to_dict()
# bl_dct = pd.read_csv("dict_data/biglit_sr.csv",encoding = "utf8",index_col = 0,squeeze = True).to_dict()
NO_VOWS = 998
NOT_FOUND = 999  # string because of split
ONE_VOW = 1
RUS_VOWELS = u"[`иеаоуяюыёэ]"
RUS_VOWELS_re = re.compile(RUS_VOWELS)


def setup_stress(data_path="./dict_data", exclude=()):
    comp_df = csv_dct("%s/lem_df.csv" % data_path)
    stss_df = csv_dct("%s/tok_df.csv" % data_path)
    # jo_dct = csv_dct("%s/jo_sr.csv" %data_path)
    bl_dct = csv_dct("%s/biglit_sr.csv" % data_path)
    # this loop is for bootstrapping the correctness: excluding dicts
    for i, e in enumerate([stss_df, comp_df, bl_dct]):
        if i in exclude:
            print(i)
            e.clear()

    def set_stress(fn, w):
        w = w.lower()
        vows = RUS_VOWELS_re.findall(w)  # look if word has russian vowels -> seed out the one syllables
        if not vows:
            return {(NO_VOWS, "no-vows")}
        if len(vows) == 1:
            return {(ONE_VOW, "one-vow")}
        try:
            return {(vows.index(u"ё") + 1, "jo-stress")}  # jo is always stressed
        except ValueError:
            try:
                res = {(x, "tok-stress") for x in stss_df[w]}  # first try the tokens db
            except KeyError:
                # conv.get account for bug
                lemmas = fn(w)  # now lemmatize with the function
                if len(lemmas) > 1:
                    print(lemmas)
                res = reduce(
                    lambda a, l: a.union(
                        {(x, "lem-stress") for x in
                         comp_df.get(l, bl_dct.get(l, (NOT_FOUND,)))}),
                    lemmas,
                    set())
                if len(res) and (NOT_FOUND, "lem-stress") in res:
                    return {(NOT_FOUND, "not-found")}
            return res

    return set_stress, pm_setup()
