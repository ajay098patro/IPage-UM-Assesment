# GIS SaaS Core-Engine – Technical Assessment

## Overview

This project is a minimal GIS SaaS core engine built as part of a technical assessment.
It demonstrates backend spatial data handling with PostGIS, a clean API-driven architecture, and a lightweight frontend to visualize time-based (epoch) geospatial data for a construction site.

The focus is on correct spatial logic, CRS handling, temporal filtering, and multi-tenant awareness, not UI polish.

## Tech Stack

### Backend

- Python
- FastAPI
- PostgreSQL + PostGIS
- psycopg2
- GeoJSON

### Frontend

- HTML
- Plain JavaScript
- OpenLayers
- Features Implemented
- Multi-tenant spatial data storage (tenant_id)
- Time-based data filtering using epochs (epoch_id)
- GeoJSON API output
- Server-side area calculation (square meters)
- CRS transformation (EPSG:4326 → requested CRS)
- Interactive map with epoch toggle (Epoch A / Epoch B)
- Feature click popup showing attributes and calculated area
- Database Setup
- PostgreSQL with PostGIS enabled.

## Table used

- site_features

## Key columns

- tenant_id
- epoch_id
- geom (PostGIS geometry)

Sample geometries include different shapes across epochs to demonstrate temporal change.
Backend Setup & Run
Create and activate environment (micromamba or similar)
Install dependencies

## Configure .env

DB_NAME=your_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

## Commands to run the project

- FastAPI: ```uvicorn main:app --reload```
- API endpoint:```GET /get-features?tenant_id=1&epoch_start=1&epoch_end=1&epsg=4326``` (Returns a GeoJSON FeatureCollection)

## Frontend Usage

### Frontend is served as static files via FastAPI

1. Start backend
2. Open browser
3. ```http://127.0.0.1:8000/```

### Frontend behavior

- Map initializes on load
- Epoch A button loads earlier snapshot
- Epoch B button loads later snapshot
- Clicking a polygon shows:
  - Feature name
  - Owner
  - Calculated area (sqm)
  - Multi-Tenant SaaS Security Design (Concept)

## My Architecture Recommendation for Cloud

The suggested architecture uses FastAPI as a lightweight control plane for authentication, tenant authorization, and request auditing, while PostGIS acts as the authoritative store for vector data and raster metadata with row-level security enforcing tenant isolation. Raster data is stored as Cloud-Optimized GeoTIFFs (COGs) in private Amazon S3, allowing efficient HTTP range-based access without a traditional WCS. FastAPI issues short-lived pre-signed URLs after validating tenant ownership, enabling the frontend to fetch only the required raster tiles directly from S3 (or CloudFront) for high performance and low cost. This design minimizes backend load, scales naturally to large datasets and many users, and enforces strong security through database isolation and cryptographic access control rather than heavy middleware or proxy services.
