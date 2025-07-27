#!/usr/bin/bash

for i in $(ls 20[12]?/*.parquet); do
	damast annotate \
		--set-unit \
			COG:deg \
			Draft:m \
			Heading:deg \
			LAT:deg \
			Length:m \
			LON:deg \
			SOG:knots \
			Width:m \
		--set-description \
            BaseDateTime:'Full UTC data and time (see https://coast.noaa.gov/data/marinecadastre/ais/data-dictionary.pdf)' \
			CallSign:'Call sign as assigned by FCC' \
            Cargo:'Cargo type (see NAIS specification and codes)' \
			COG:'Course Over Ground - For data beginning in 2015, COG values that are less than 0 (negative) are known to be incorrect and can be corrected by adding 409.6. Values of 360.0 refer to the COG being unavailable and can be ignored. (see  https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf)' \
			Draft:'Static Draft  - depth of water that a ship needs in order to float. Must be encoded in meters, not feet, and reflect the vessel’s actual or maximum draft (see https://navcen.uscg.gov/sites/default/files/pdf/AIS/AISGuide.pdf)' \
            Heading:'True heading angle' \
			IMO:'International Maritime Organization Vessel number' \
			LAT:Latitude \
            Length:'Length of vessel (see NAIS specifications)' \
			LON:Longitude \
			MMSI:'Maritime Mobile Service Identify number' \
			SOG:'Speed Over Ground - Speed over ground in 1/10 knot steps (0-102.2 knots) 1 023 = not available, 1 022 = 102.2 knots or higher. For data beginning in 2015, SOG values that are less than 0 (negative) are known to be incorrect and can be corrected by adding 102.4. Sentinel values such as 102.3 may indicate that no SOG value was transmitted, and can be translated as not-available' \
			Status:'Navigational status with a range of 0-15 (see https://www.navcen.uscg.gov/ais-class-a-reports)' \
			VesselName:'Name as shown on the station radio license' \
			VesselType:'Vessel types defined in NAIS specifications https://www.navcen.uscg.gov/ais-class-a-reports
	a. Codes 0 through 255 are original vessel type codes defined by AIS standards 
	b. Codes 256 through 999 are an empty set added by MarineCadastre.gov 
	c. Codes 1001 through 1025 are keys to the AVIS vessel type descriptions 
	 (see https://coast.noaa.gov/data/marinecadastre/ais/faq.pdf)' \
            Width:'Width of vessel (see NAIS specifications)' \
		--inplace --apply -f $i
done

