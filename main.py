from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import psycopg2, os, json
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

@app.get("/get-features")
def get_features(tenant_id: int, epoch_start: int, epoch_end: int, epsg: int = 4326):
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
    )
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, owner, tenant_id, epoch_id,
               ST_AsGeoJSON(ST_Transform(geom, %s)),
               ST_Area(ST_Transform(geom, 3857))
        FROM site_features
        WHERE tenant_id = %s
          AND epoch_id BETWEEN %s AND %s;
    """, (epsg, tenant_id, epoch_start, epoch_end))

    features = []
    for r in cur.fetchall():
        features.append({
            "type": "Feature",
            "geometry": json.loads(r[5]),
            "properties": {
                "id": r[0],
                "name": r[1],
                "owner": r[2],
                "tenant_id": r[3],
                "epoch_id": r[4],
                "area_sqm": r[6]
            }
        })

    cur.close()
    conn.close()
    return {"type": "FeatureCollection", "features": features}

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
