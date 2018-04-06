#!/usr/bin/python
# coding=utf8
"""
Igor:
Fr 19. Sep 14:14:33 CEST 2014
"""
import pandas as pd
from setstress import setup_stress, RUS_VOWELS_re, NO_VOWS, ONE_VOW
import os
import lxml.etree as etree
import itertools


def find_stss_syl(x):
    vows = "".join(RUS_VOWELS_re.findall(x.lower()))
    if len(vows) == 1:
        return ONE_VOW
    if u"ё" in vows:
        return vows.index(u"ё") + 1
    if not vows:
        return NO_VOWS
    # case when no stress is set
    if not vows.count("`"):
        return 997
    if vows.count("`") > 1:
        stressed = vows[vows.find("`") + 1:].find("`")
    else:
        stressed = vows.find("`")
    if stressed != -1:
        return stressed + 1
    else:
        return 998


def prepare_test_corp(directory="~/Data/shuffled_rnc"):
    """Funtion for preparing the test corpus: The shuffled rnc to csv, fields: token,stress,lemma"""
    fullpath = os.path.expanduser(directory)

    def get_data(fl):
        filepath = os.path.join(fullpath, fl)
        print(fl)
        xml = etree.parse(filepath)
        anas = xml.iter("ana")
        res = [(x.tail.replace("`", ""), x.attrib["lex"], find_stss_syl(x.tail)) for x in anas if x.tail]
        return res

    res = itertools.chain(*map(get_data, sorted(os.listdir(fullpath))))
    return res


def eval_shuffled_rnc(fact=0.5):
    def type_stress(df):
        gr = df.groupby(["type_guess", 'iseq'])["stress"].count().unstack()
        gr_ratio = gr.div(gr.sum(axis=1), axis=0)
        ratio_total = gr.join(gr_ratio, lsuffix="_total", rsuffix="_ratio").fillna(0).sort("True_total",
                                                                                           ascending=False)
        print(gr, ratio_total)
        return ratio_total

    set_stress, pm = setup_stress()
    corpus = list(prepare_test_corp())

    df = pd.DataFrame(corpus[:int(len(corpus) * fact)], columns=['token', "lemma", "stress"])

    stress_map = {k: zip(*set_stress(pm, k)) for k in df["token"].unique()}
    df["stress_guess"] = df["token"].map(lambda x: set(stress_map[x][0]))
    df['type_guess'] = df['token'].map(lambda x: stress_map[x][1])
    # corpus_with_stress = [(itm, (set_stress(pm, itm[0]))) for itm in corpus]
    df['iseq'] = df.apply(
        lambda x: x["stress"] in list(x['stress_guess'])[:1], axis=1)
    # print statistics
    print("Tokens ratio:")
    print(df['iseq'].value_counts().div(len(df)))
    print("Types ratio:")
    types_df = df.drop_duplicates('token')
    print(types_df['iseq'].value_counts().div(len(types_df)))
    # log the words that were guessed wrong
    types_df[types_df['iseq'] == False].to_csv("corp_data/falses.csv", encoding="utf8")
    type_stress(df)


if __name__ == "__main__":
    import sys

    try:
        if len(sys.argv) > 1:
            fact = float(sys.argv[-1])
            if fact > 1:
                raise ValueError
        else:
            fact = 0.5
        df = eval_shuffled_rnc(fact)
    except ValueError:
        print("Factor value is not valid: Choose something between 0.0 and 1.0")
