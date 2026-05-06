# Quantitative Files To Add Locally

Place these files in this local folder:

`/Users/torialiu/Downloads/tangled-title-site/data/quant/`

The website already knows how to use them when present.

## Required for the full tract-level table and interactive tract map

| Local filename | GitHub path |
| --- | --- |
| `tract_intersectional_group_merged.csv` | `analysis/20260427uzzi_category_match/outputs/tract_intersectional_group_merged.csv` |
| `baltimore_tracts.geojson` | `streamlit/data/map_assets/baltimore_tracts.geojson` |

## Helpful supporting files

| Local filename | GitHub path |
| --- | --- |
| `tangled_and_at_risk_by_census_tract_baltimore_202603.csv` | `Data/tangled_and_at_risk_by_census_tract_baltimore_202603.csv` |
| `acs_acs5_2019_tract_baltimore_city_md_ice_input_derived.csv` | `Data/acs_acs5_2019_tract_baltimore_city_md_ice_input_derived.csv` |
| `tract_intersectional_group_lookup.csv` | `analysis/20260427uzzi_category_match/outputs/tract_intersectional_group_lookup.csv` |

## Non-fatal shooting rate

The current `p5_publication_style_table.csv` has `Non-fatal shooting rate` as `NA`.
The data inventory says the raw source is:

`Data/Part1_Crime_Beta_9S(shooting).geojson`

That file contains point incidents. It would need to be filtered/aggregated to census tracts and divided by ACS tract population before the website can show a tract-level or group-level non-fatal shooting rate.
