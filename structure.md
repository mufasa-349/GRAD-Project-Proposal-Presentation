Here is the slide titles and basic contents, image names and general structure of the presentation to create: I want you to make it more official if neccesary. Use bulletpoints instead of sentences. In paranthes sentences are points you need to be careful while creating. You can find images under images folder in project directory

Slides
1. Title:
    Project #543
    Visualizing Spatio-Temporal Uncertainty in High-Density Data

    Mustafa Bozyel
    Senih Kırmaç
    Ömer Mert Özel

2. Problem & Motivation
    Software based systems generally provides certain data, although the real data is contains reasonable amount of uncertainty, especially in spatio-temporal data. Our motivation is to visualize this uncertainty for better decision making processes. (A brief example can be made, Cursor you can create this yoruself, but include it in italic so that i can understand its your idea and check whether it is okey or not for our scenario)

3. Related Works
    (To Cursor:
    
    Related Works section should be maximum 2 slides. Do not explain too many papers. Focus only on 3–4 key works that directly support our project title: “Visualizing Spatio-Temporal Uncertainty in High-Density Data.”

Slide 1: Uncertainty Visualization Design Space

Use image: padilla1.png

Main source:
Padilla, Kay, and Hullman (2022) – Uncertainty Visualization

Brief explanation:
This work provides a broad overview of uncertainty visualization techniques. It categorizes methods such as error bars, box plots, violin plots, gradient plots, quantile dot plots, hypothetical outcome plots, ensemble plots, and visual encodings such as fuzziness, location, size, and transparency. For our project, this source is useful because it shows that uncertainty can be represented either through distributional graphics or through visual encodings directly applied to the data.

Key takeaway for our project:
Since our data is spatio-temporal and high-density, simple methods like error bars are not enough. We need visual encodings such as transparency, blur, gradient intensity, or ensemble-like representations that can show uncertainty without overcrowding the visualization.

Also mention:
MacEachren et al. (2012) – Visual Semiotics & Uncertainty Visualization

Brief explanation:
MacEachren et al. study how visual variables such as blur, transparency, fuzziness, size, and arrangement communicate uncertainty. This supports our design idea of using visual effects like opacity or fading to make uncertainty intuitive for the user.

Slide 2: Spatial Uncertainty and Decision-Oriented Visualization

Use image: from-report1.png

Main source:
McKenzie et al. / spatial uncertainty visualization examples

Brief explanation:
This type of work shows how uncertainty can be visualized in map-based or mobile spatial interfaces. The circle around a location is a common method for showing positional uncertainty, while color and landmarks can add extra contextual information. This is relevant to our project because we also need to represent uncertainty over space and time, not only as numerical confidence values.

Key takeaway for our project:
Spatial uncertainty should be visible but not misleading. A hard boundary such as a circle may make users think that everything inside is possible and everything outside is impossible. Therefore, our visualization should avoid overly rigid borders when uncertainty is continuous.

Additional related source:
Liu et al. (2016) – Uncertainty Visualization by Representative Sampling from Prediction Ensembles

Brief explanation:
Liu et al. use ensemble-based visualization to show multiple possible outcomes instead of a single deterministic prediction. This is useful for our project because spatio-temporal uncertainty often involves many possible future states or trajectories. Ensemble-style visualizations can help communicate this uncertainty more naturally.

Final message of related works:
Prior research shows that uncertainty visualization is not only about adding extra information to a chart. It must be designed carefully to avoid visual overload and misinterpretation. Our project builds on these works by combining uncertainty encodings such as transparency, blur, gradients, and possible ensemble-based representations for high-density spatio-temporal data.
)



4. System Overview

Create a “System Overview” slide with a left-to-right pipeline:
Raw Spatio-Temporal Data → Preprocessing & Cleaning → Uncertainty Estimation → Visual Encoding Layer → Interactive Dashboard → Decision Support.

Use short labels under each step:
- Raw Data: location + time + observed values
- Preprocessing: cleaning, aggregation, temporal alignment
- Uncertainty Estimation: confidence, variance, missingness, prediction error
- Visual Encoding: opacity, blur, gradients, density-aware views
- Dashboard: map, timeline, filters, interaction
- Decision Support: identify reliable and uncertain regions

Also include two screenshots from our prototype:
- dense1.png
- heatmap1.png

Use dense1.png to illustrate dense point-based raw data and heatmap1.png to illustrate processed uncertainty-aware visualization. Add short captions under them.

Keep the slide clean, visual, and minimal.

5. Data Flow Diagram

we have two different diagrams. 1 is data insertion diagram, you can paste it in slide 1 from data-workflow1.png

and in slide 2 , you can paste:
operation-workflow.png


6. Methodology

Create ONE slide titled “Methodology” for my project “GNSS Fix Visualization (Leaflet + D3)”. Keep it concise (5–7 bullets), presentation-ready, in English.

Context:
- Data: Android GNSS Logger logs. We use only lines starting with “Fix,” → *_FixOnly.txt (CSV-like).
- Optional reference: OSM GPX track → *_latlon_by_time.txt (TSV: ISO_TIME, LAT, LON).
- Web app: gnss_tuzla_map_interactive.html loads data via fetch(), parses Fix fields (lat, lon, alt, speed, accuracy, bearing, UnixTimeMillis, VerticalAccuracyMeters).
- Derived metrics: Haversine distance from first fix; Δlat/Δlon; Δalt.
- Visualizations: (1) Original points colored by distance, size by accuracy (2) Heatmaps (grid / soft density, stationary vs moving route threshold 30m, hover preview window i±7) (3) Uncertainty rings (radius=AccuracyMeters, color green→red, center dot scales with VerticalAccuracyMeters).
- Compare mode: loads OSM reference + raw GNSS, computes nearest-neighbor deviation (Haversine) and signed cross-track deviation (using route tangent/normal), shows on map + chart.
- Output: interactive Leaflet map + D3 chart (Lon vs Alt; or Lon vs signed deviation in compare mode).

Deliverable:
- Slide bullets only (no paragraphs), include one short “Tools/Tech” bullet and one “Outputs” bullet.


7. Validation & Testing


Create ONE slide titled “Validation & Testing” for my project “GNSS Fix Visualization (Leaflet + D3)”. Keep it concise (5–7 bullets), presentation-ready, in English.

Context:
- Inputs: Android GNSS Logger logs; we parse only lines starting with “Fix,” into *_FixOnly.txt. Optional OSM GPX reference exported to *_latlon_by_time.txt (TSV: ISO_TIME, LAT, LON).
- Loading: data is fetched via relative URLs (./data/...) and should work on GitHub Pages or via local HTTP server; manual file upload fallback exists.
- Parsing validation: skip malformed Fix lines (length < 13) and rows with non-finite lat/lon/alt; treat missing speed/accuracy/bearing/time/vertical accuracy as null.
- Metric validation: Haversine distance checks (sanity ranges), derived deltas (Δlat/Δlon/Δalt) computed relative to first fix.
- Visualization testing: verify all modes render without errors (Original / Heatmap mono & BGR / Uncertainty); moving-route threshold at 30 m; hover preview uses i±7 window and updates preview radius.
- Compare-mode validation: load OSM reference + raw GNSS; compute nearest-neighbor deviation (Haversine) and signed cross-track deviation; verify map hover connector and chart update (Lon vs deviation, clipped ±3 m).
- Outputs to check: stats panel ranges (count, distance range, accuracy range), popups/hover selection fields, and D3 chart consistency with selected point.

Deliverable:
- Slide bullets only (no paragraphs). Include one bullet describing “Test data / scenarios” and one bullet describing “Acceptance criteria”.


8. Demo

we will use multiple slides for demo. 
slide1:
First of all we will include a screenshot of dashboard. In thıs screenshot, we are comparing real reference data and raw gps data: dashboard1.png Also the chart in iamge is showing distance deviation in meters. 

slide2

This figure shows the devaitions in raw gps data while stable: dashboard2.png

slide3: 

How to visualize uncertainty in stable data: 2 methods. Density: dashboard3.png and Heatmap: dashboard4.png

slide4:

How does these visualizations work on walking data: dashboard5.png


9. Conclusion / Future Work

Conclusion (Slide)
Built an interactive GNSS fix analysis tool (Leaflet map + D3 chart) for visual exploration.
Parsed & cleaned Android GNSS Logger Fix, records and computed derived metrics (distance-from-first, deltas).
Provided multiple visual perspectives: point view, density/heatmaps, and uncertainty rings.
Enabled reference-based evaluation via OSM track comparison (nearest-neighbor + cross-track deviation).
Improved interpretability of accuracy, drift, and route-level behavior through interactive hover/click.
Future Work (Slide)
Large-scale validation on dense, high-frequency, long-duration datasets (city-scale / many tracks).
Performance risks: browser memory pressure, slower parsing/rendering, UI lag (many markers / heavy heat computations).
Visualization scaling issues: overplotting, misleading density at low zoom, loss of local detail without clustering/tiling.
Data quality challenges: time misalignment between reference and GNSS, outliers/multipath, missing accuracy fields.
Next steps: spatial indexing (e.g., grid/k-d tree), marker clustering / vector tiling, incremental/streamed loading, and robust outlier filtering.

10. Add a thanks slide saying thanks. 

