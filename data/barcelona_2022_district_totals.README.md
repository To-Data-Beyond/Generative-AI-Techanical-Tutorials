# Barcelona 2022 district totals

These ten aggregate values are transcribed from the original author's complete
district-join table in “Leveraging Geospatial Data in Python with GeoPandas”
(archive ID `9dc188787e88`, substantive figure 10). The original local
`2022_padro_sexe.csv` was not supplied and its linked municipal resource now
returns 404. This CSV recovers only the visible district totals, **not** sex-level
records or the original missing file. No population values are synthesized.

Source table: https://cdn-images-1.medium.com/max/800/1*ZmxFQm3sb-qN_CJRGXfKwg.png

The ten counts sum to 1,639,981. District codes are the standard 1–10 geographic
join keys, matched to the names visible in that same source table. The notebook
checks the code/name mapping before joining and refuses missing or duplicate keys.
The table is a reproducible teaching input, not a newly measured population series.
