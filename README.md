# MARINE CADASTRE

## Download data from

https://hub.marinecadastre.gov/pages/vesseltraffic

### Year 2024

All files:
 - https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2024/index.html

```
  wget https://coast.noaa.gov/htdata/CMSP/AISDataHandler/2024/AIS_2024_01_01.zip
```

Convert the contained csv into a parquet file:
```
    damast convert -f AIS_2024_01_01.zip  --output-dir parquet/
```

Inspect and filter the data for a particular region:
```
    damast inspect -f parquet/* --filter 'LAT > 18' --filter 'LAT < 20' --filter 'LON < -90' --filter 'LON > -95'
```

Note:
The data pipeline `str-to-timestamp.damast.ppl` has been added, to convert the
BaseTimeColumn to datetime format.
While this conversion could be automatically done at the initial time of converting CSV to parquet it requires the `try_parse_date` option, which turned out to significantly slow the conversion process. Hence, we first convert CSV and parquet, then add the 'timestamp' column.

Either use the convert.sh script or

```
damast process --pipeline str-to-timestamp.damast.ppl --input-data input.parquet --output-file output.parquet
```

#### Vessel Types

https://coast.noaa.gov/data/marinecadastre/ais/VesselTypeCodes2018.pdf
