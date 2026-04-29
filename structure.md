Here is the slide titles and basic contents, image names and general structure of the presentation to create: I want you to make it more official if neccesary. Use bulletpoints instead of sentences. In paranthes sentences are points you need to be careful while creating.

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
    (Cursor check pdfs under related-works part:
    
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
5. Data Flow Diagram
6. Methodology
7. Validation & Testing
8. Demo
9. Conclusion / Future Work

