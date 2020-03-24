Localities OSM application is for handling data from docker-osm database. 
LocalitiesOSM model is based on table from docker osm. Here are the description for every fields on DockerOsm model..

> ##### osm_id 
> The id number of a node (point) or way (polygon) in OSM

> ##### amenity 
> For describing useful and important facilities for visitors and residents.<br>
> amenity=clinic,doctors,hospital,dentist,pharmacy (osm-tag)<br> 
> type (old-hs-attributes)

> ##### healthcare 
> A key to tag all places that provide healthcare (are part of the healthcare sector).<br>
> healthcare=doctor,pharmacy,hospital,clinic,dentist,physiotherapist,alternative,laboratory,optometrist,rehabilitation,blood_donation,birthing_center (osm-tag)<br>

> ##### name 
> The primary tag used for naming an element.<br>
> name (osm-tag)<br> 
> name (old-hs-attributes)

> ##### operator 
> The operator tag is used to name a company, corporation, person or any other entity who is directly in charge of the current operation of a map object..<br>
> operator (osm-tag)

> ##### source 
> Used to indicate the source of information (i.e. meta data) added to OpenStreetMap.<br>
> source (osm-tag)<br> 
> source (old-hs-attributes)

> ##### speciality 
> A key to detail the special services provided by a healthcare facility. To be used in conjuction with the 'healthcare=*' tag. For example 'healthcare=laboratory', and 'healthcare:speciality=blood_check'.<br>
> Speciality and healthcare is coupled, so the value is checked in https://wiki.openstreetmap.org/wiki/Key:healthcare#Subtags
> Multiple speciality can be separated by semicolon
> healthcare:speciality (osm-tag)

> ##### operator_type 
> This tag is used to give more information about the type of operator for a feature<br>
> operator:type=public,private,community,religious,government,ngo (osm-tag)<br>
> ownership (old-hs-attributes)

> ##### contact_number 
> The contact tag is the prefix for several contact:* keys to describe contacts.<br>
> contact:phone (osm-tag)<br>
> contact-number (old-hs-attributes)

> ##### operational_status 
> Used to document an observation of the current functional status of a mapped feature.<br>
> operational_status (osm-tag)

> ##### opening_hours 
> Describes when something is open or closed. There is a specific standard format for this data https://wiki.openstreetmap.org/wiki/Key:opening_hours/specification.<br>
> opening_hours (osm-tag)<br>
> operation (old-hs-attributes)

> ##### beds 
> Indicates the number of beds in a hotel or hospital.<br>
> beds (osm-tag)<br>
> inpatient-service['full time bed'] (old-hs-attributes)

> ##### staff_doctors 
> Indicates the number of doctors in a hospital.<br>
> staff_count:doctors (osm-tag)<br>
> staff ['doctors'] (old-hs-attributes)

> ##### staff_nurses
> Indicates the number of nurses in a hospital.<br>
> staff_count:nurses (osm-tag)<br>
> staff ['nurses'] (old-hs-attributes)

> ##### health_amenity_type
> Indicates what type of speciality medical equipment is available at the healthsite.<br>
> health_amenity:type (osm-tag)

> ##### dispensing (bool)
> Whether a pharmacy dispenses prescription drugs or not. Used to add information to something that is already tagged as amenity=pharmacy.<br>
> dispensing (osm-tag)

> ##### wheelchair (bool)
> Used to mark places or ways that are suitable to be used with a wheelchair and a person with a disability who uses another mobility device (like a walker).<br>
> wheelchair (osm-tag)

> ##### emergency (bool)
> This key describes various emergency services.<br>
> emergency (osm-tag)

> ##### insurance
> This key describes the type of health insurance accepted at the healthsite.<br>
> insurance:health=no,public,private,unknown (osm-tag)

> ##### water_source
> Used to indicate the source of the water for features that provide or use water.<br>
> water_source=well,water_works,manual_pump,powered_pump,groundwater,rain (osm-tag)

> ##### generator_source
> Used to indicate the source of the power generated.<br>
> generator:source=generator,power_grid,solar,no (osm-tag)

> ##### url
> Specifying a url related to a feature, in this case the url if available .<br>
> url (osm-tag)

> ##### addr_housenumber 
> Used for a full-text, often multi-line, housenumber for buildings and facilities.<br>
> addr:housenumber (osm-tag)<br>

> ##### addr_street 
> Used for a full-text, often multi-line, street for buildings and facilities.<br>
> addr:street (osm-tag)<br>

> ##### addr_postcode 
> Used for a full-text, often multi-line, postal code for buildings and facilities.<br>
> addr:postcode (osm-tag)<br>

> ##### addr_city 
> Used for a full-text, often multi-line, city name for buildings and facilities.<br>
> addr:city (osm-tag)<br>

> ##### addr_country 
> Used for a full-text, often multi-line, ISO country code for buildings and facilities.
> See : https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2
> <br>
> addr:country (osm-tag)<br>