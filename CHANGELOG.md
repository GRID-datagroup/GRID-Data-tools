# 0.1.1
# Change
* `get_edges` move to `binned`
## Add
* add bin_by_max_count in `unbinned`
## Fix
* `Evt` convert to `phaii`

# 0.1.0
## Fix
* add module `binned` and `data` to `setup`

# 0.1.0a1
## Rename
* change `gdt` to `grid`
* move `coords` and `logger` to root directory

## Add
* class `Detector`, `TimeGRIDSec`, `MetGRID`
* module `binned`
* module `data` (class `Evt`, `PosAtt`)
* `flux` method in `class:HIA`
* icon class `GRIDIcon`

## Remove
* `get_sun_pos` and `get_geocenter_pos` in `coords`

## Change
* move `in_hia` from `class:EarthPlotGRID` to `class:HIA`
* change plot class

# 0.1.0a0
## Add
* CheckGRID
* EatrhPlotGRID
* LightCurveGRID
* SkyPlotGRID
* SigmaClip
* coordinates functions
* HIA region
* Logger