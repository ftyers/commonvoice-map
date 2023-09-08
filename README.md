# commonvoice-map

![](img/size_map_example.png)

A simple map generation script to produce an approximate distribution and dataset size of languages in Common Voice.

## To generate a new map

* Download the latest stats: `wget -q -O - "https://commonvoice.mozilla.org/api/v1/stats/languages" | json_pp > languages.json`
* If there are two letter codes, update `iso2to3.py` with the mappings to three letter codes.
* Update `mapdata.tsv` by adding the mapping from code to latitude/longitude (you can get this from [Glottolog](https://glottolog.org/)).
* Run `plot.py`

## Todo

* Point pinpoints where languages are, get them from Glottolog.
