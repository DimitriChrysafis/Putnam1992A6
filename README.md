## Problem Statement
**_Definitive Putnam Problem_**

Four points are chosen independently and at random on the surface of a sphere (using the uniform distribution). What is the probability that the center of the sphere lies inside the resulting tetrahedron?


**Solution to Putnam 1992 A6**  
The documented code provided in ``PythonFiles/simulation.py``` randomly choose four points on sphere millions of times. ```PythonFiles/visualize_tetrahedron.py``` generates the plotly interactive graph to be able to have a playground for testing. ```PythonFiles/renderer.py``` is for generating the images with the sphere wireframe and display probabilities or easy user access.  

The c++ code is done similarly where ```RewriteInC++/main.cpp``` uses the convex hull header file to do the same. All data and explanation of code can be found below.

[read the PDF here https://github.com/DimitriChrysafis/Putnam1992A6/blob/main/ExplanationPaper.pdf](https://github.com/DimitriChrysafis/Putnam1992A6/blob/main/ExplanationPaper.pdf).

![](input.gif)

Left: Example of the center being INSIDE the tetrahedron.\n
Right: Example of the center being OUTSIDE the tetrahedron.
<div style="display: flex; justify-content: center;">
    <img src="inside.gif" width="300">
    <img src="outside.gif" width="300">
</div>
