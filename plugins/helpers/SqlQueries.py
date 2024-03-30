class SqlQueries: 
    staging_era5_create = ("""
    CREATE TABLE IF NOT EXISTS public.era5 (
        id SERIAL PRIMARY KEY,
        latitude DOUBLE PRECISION,
        longitude DOUBLE PRECISION,
        value VARCHAR(255),
        data_date INTEGER,
        data_time INTEGER,
        level INTEGER
    );
    """)

    staging_radar_create = ("""
    CREATE TABLE IF NOT EXIST public.radar (
    longitude VARCHAR,
    latitude VARCHAR,
    altitude VARCHAR,
    reflectivity VARCHAR,
    total_power VARCHAR,
    velocity VARCHAR,
    spectrum_width VARCHAR,
    time VARCHAR
    );
    """)

    # TODO: insert query
    