CREATE DATABASE gis_saas_db;

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE site_features (
  id SERIAL PRIMARY KEY,
  name TEXT,
  owner TEXT,
  tenant_id INTEGER,
  epoch_id INTEGER,
  geom GEOMETRY(POLYGON, 4326)
);

INSERT INTO site_features
(name, owner, tenant_id, epoch_id, geom)
VALUES (
  'Block A',
  'Ajay',
  1,
  1,
  ST_GeomFromText(
    'POLYGON((
      78.4 17.4,
      78.401 17.4,
      78.401 17.401,
      78.4 17.401,
      78.4 17.4
    ))',
    4326
  )
),
(
  'Block B',
  'Ajay',
  1,
  2,
  ST_GeomFromText(
    'POLYGON((
      78.402 17.400,
      78.403 17.401,
      78.4025 17.402,
      78.4015 17.402,
      78.401 17.401,
      78.4015 17.400,
      78.402 17.400
    ))',
    4326
  )
);

SELECT id, name, epoch_id, ST_AsText(geom) FROM site_features;
