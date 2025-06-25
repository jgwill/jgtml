Add initial documentation files for MLF, MX, and TTF data columns and purposes with TODO notes for future elaboration on patterns and relationships.


#42


@stcgoal I scaffolded what I want this documentation to contain for creating clarity for the steps of making models that will learn from all that.
@ STCIssue Redundant repetition of my Intent with LLM when prompting and also no centralized place where to talk about columns patterns


* In development, data is in ./data/full/ttf ./data/full/mlf ./data/targets/mx

## Patterns configuration

The file `$HOME/.jgt/settings.json` defines a `"patterns"` section mapping
pattern names to the columns generated for each dataset.

| Pattern | Columns |
| ------- | ------- |
| `mz` | `mfi_str`, `zcol` |
| `mfi` | `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake` |
| `mfizone` | `mfi_sq`, `mfi_green`, `mfi_fade`, `mfi_fake`, `zone_sig` |
| `zonesq` | `zone_sig`, `mfi_sq` |
| `aoabz` | `aoaz`, `aobz` |
| `aoac` | `ao`, `ac` |
| `ttf` | `mfi_sig`, `zone_sig` |

These patterns drive which columns appear in the feature CSVs found under the
`./data/full/ttf` and `./data/full/mlf` directories.

## Dataset layout

- `./data/full/ttf` – transformed trading features using the `ttf` pattern.
- `./data/full/mlf` – meta lag features derived from TTF for each pattern.
- `./data/targets/mx` or `./data/full/mx/targets` – target datasets combining
  signals such as `fdbb` and `fdbs` with the resulting profit or loss in the
  `target` column.

The raw CDS files used to build these datasets are kept in
`./data/current/cds`.


------
SEE:
-------

[TTF_purpose.md](TTF_purpose.md)  
[TTF_data_columns.md](TTF_data_columns.md)  


[MLF_purpose.md](MLF_purpose.md)  
[MLF_data_columns.md](MLF_data_columns.md)  


[MX_purpose.md](MX_purpose.md)  
[MX_data_columns.md](MX_data_columns.md)  

