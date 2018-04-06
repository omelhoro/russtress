Rustress is an app to set stress marks in russian words.




###Approach
It depends on pymorphy2 since it takes a different approach to the stress-problem:
Some apps use a complete dictionary of word forms to merge them with the occurences in the text.
This leads for the most frequent 20.000 words to 1.7 mio forms.

It can be easier and more effective: If you take some avaible corpus such as www.ruscorpora.ru, you can calculate that about 92% of tokens have the same stress position as their lemma ("normal form"). A big part of the rest 8% one can predict by a list of forms that have different stress than their lemma. Such list has tokens like "хочет,хочешь".

So a given token is first lookep up in the Tokens-Dict, and, if not there, is lemmatized by pymorphy and the lemma is then looked up in List-Dict.

###Evaluation
The results are pretty nice: The evaluation on a free available subset of ruscorpora shows 96% correctness.
In the following table you can see the strenghts and weaknesses of this approach:
If you exclude easy tasks as Jo-words, tokens with no vowels (numerals) and tokens with only one vowel, you can see
that the correctness for words with only one possible lemma-stress is nice, such as for the one possible tokens-stress.
The weaknesses are visible when there are two possibilities of setting the stress - here for the results, the first possibility was taken.This succeeds for lemmas with 72% correctness, for tokens it's only 50%. For the words that are not found in the Database the ratio is 100% False, since I'm still thinking about a backup-algorhithm.

<table border="0" class="dataframe">  <thead>    <tr style="text-align: right;">      <th>iseq</th>      <th>False_total</th>      <th>True_total</th>      <th>False_ratio</th>      <th>True_ratio</th>    </tr>    <tr>      <th>type_guess</th>      <th></th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>(lem-stress,)</th>      <td> 2026</td>      <td> 244732</td>      <td> 0.008210</td>      <td> 0.991790</td>    </tr>    <tr>      <th>(one-vow,)</th>      <td>    0</td>      <td> 137929</td>      <td> 0.000000</td>      <td> 1.000000</td>    </tr>    <tr>      <th>(tok-stress,)</th>      <td> 1106</td>      <td>  65381</td>      <td> 0.016635</td>      <td> 0.983365</td>    </tr>    <tr>      <th>(jo-stress,)</th>      <td>    0</td>      <td>  11323</td>      <td> 0.000000</td>      <td> 1.000000</td>    </tr>    <tr>      <th>(lem-stress, lem-stress)</th>      <td> 4393</td>      <td>  11257</td>      <td> 0.280703</td>      <td> 0.719297</td>    </tr>    <tr>      <th>(tok-stress, tok-stress)</th>      <td> 6600</td>      <td>   6411</td>      <td> 0.507263</td>      <td> 0.492737</td>    </tr>    <tr>      <th>(lem-stress, lem-stress, lem-stress)</th>      <td>    8</td>      <td>     97</td>      <td> 0.076190</td>      <td> 0.923810</td>    </tr>    <tr>      <th>(not-found,)</th>      <td> 5614</td>      <td>      0</td>      <td> 1.000000</td>      <td> 0.000000</td>    </tr>  </tbody></table>

###TODO
- implement an statistical tagger as a backup if the token and lemma are not found
- disambiguate between different words ("тень" - "т'ени", "тенуть" - "тен'и")
- port current Python-Dicts and to something more efficient like DAWG (since pymorphy already uses it)
