const center = ol.proj.fromLonLat([78.4, 17.4]);

const source = new ol.source.Vector();
const layer = new ol.layer.Vector({ source });

const map = new ol.Map({
  target: "map",
  layers: [
    new ol.layer.Tile({ source: new ol.source.OSM() }),
    layer
  ],
  view: new ol.View({ center, zoom: 17 })
});

async function loadEpoch(a,b){
  source.clear();
  const res = await fetch(`/get-features?tenant_id=1&epoch_start=${a}&epoch_end=${b}`);
  const data = await res.json();
  const feats = new ol.format.GeoJSON().readFeatures(data,{featureProjection:"EPSG:3857"});
  source.addFeatures(feats);
}
