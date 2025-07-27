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

Update the metadata, here adding unit 'deg' to LAT and LON columns:
``` 
    damast annotate --set-unit LAT:deg LON:deg --inplace --apply -f AIS_2024_01_01.parquet
``` 

Note:
The data pipeline `str-to-timestamp.damast.ppl` has been added, to convert the
BaseTimeColumn to datetime format.
While this conversion could be automatically done at the initial time of converting CSV to parquet it requires the `try_parse_date` option, which turned out to significantly slow the conversion process. Hence, we first convert CSV and parquet, then add the 'timestamp' column.

Either use the convert.sh script or

```
damast process --pipeline str-to-timestamp.damast.ppl --input-data input.parquet --output-file output.parquet
```

### Meta Data

The scripts folder contains 'apply-metadata.sh' which allows to write metadata to 
each of the parquet files.

The following sources of information have been used:

- Format: https://coast.noaa.gov/data/marinecadastre/ais/data-dictionary.pdf
- VesselType Codes: https://coast.noaa.gov/data/marinecadastre/ais/VesselTypeCodes2018.pdf
- FAQ: https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf
