# Simulating-Bumpy-Translucent-Appearance-In-Images

This is the code for coursework of IDIG4003 - Appearance, Perception and Measurement course, in computer science department at NTNU in Gjøvik.


Understanding and replicating material appearance attributes is critical in various fields such as 3D printing, cultural heritage, and computer vision. While attributes like color and gloss have been extensively studied, translucency perception remains relatively understudied, with many unanswered questions. This project investigates the relationship between bumpiness and translucency—two appearance attributes that interact and affect how materials are perceived by the human visual system (HVS). By studying how surface irregularities, like bumps, alter light interaction and translucency perception, this research provides insights that can aid in accurate material rendering and perception modeling.

The primary objective of this study is to explore how surface properties, such as bumpiness, influence translucency perception. To achieve this, we:

1. Create a dataset: Using the method proposed by Manabe et al. [1], we modulate bumpiness levels in images to create a dataset with varying bumpiness levels. In some cases, specular highlights are preserved to enhance translucent appearance using the code provided in [2].
2. Conducted psychophysical experiments: Evaluate Naturalness, Bumpiness, and Translucency of images to study their interactions. The objective scores are provided under objective scores.

# References
1. Manabe, Yusuke & Tanaka, Midori & Horiuchi, Takahiko. (2022). Bumpy Appearance Editing of Object Surfaces in Digital Images. Journal of Imaging Science and Technology. 66. 050403-1. 10.2352/J.ImagingSci.Technol.2022.66.5.050403.
2. https://github.com/fu123456/SHDNet/tree/main
