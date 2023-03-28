# 0.2.0
## Refactor
* move `coords` and `time` into `utils`
## Feat
* some coordinate conversion functions in `utils.coords`
* some time conversion functions in `utils.time`

# 0.1.1
## Feat
* add bin_by_max_count in `unbinned`

## Fix
* `Evt` convert to `phaii`

## Others
* `get_edges` move to `binned`

# 0.1.0
## Fix
* add module `binned` and `data` to `setup`

# 0.1.0a1
## Feat
* class `Detector`, `TimeGRIDSec`, `MetGRID`
* module `binned`
* module `data` (class `Evt`, `PosAtt`)
* `flux` method in `class:HIA`
* icon class `GRIDIcon`

## Remove
* `get_sun_pos` and `get_geocenter_pos` in `coords`

## Others
* change `gdt` to `grid`
* move `coords` and `logger` to root directory
* move `in_hia` from `class:EarthPlotGRID` to `class:HIA`
* change plot class

# 0.1.0a0
## Feat
* CheckGRID
* EatrhPlotGRID
* LightCurveGRID
* SkyPlotGRID
* SigmaClip
* coordinates functions
* HIA region
* Logger