import numpy as np
import plotly.graph_objs as go
from scipy.spatial import ConvexHull

def getRandomPoints(num_points=4):
    """
    get random points on the surface of a sphere.

    @param num_points: num of points to generate (we want to generate a tetrahedron so 4)
    """
    points = np.random.randn(num_points, 3)
    points /= np.linalg.norm(points, axis=1)[:, np.newaxis]
    return points

def getHull(points):
    """
    Compute the convex hull of a set of points.
    """
    return ConvexHull(points)

def spherePlotly():
    """
    Create a plotly trace for the sphere.

    @return: Plotly surface trace representing the sphere.

    0:2*np.pi:100j generates 100 points between 0 and 2 𝜋 2π for u.
    0:np.pi:50j generates 50 points between 0 and 𝜋 π for v
    """
    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:50j]

    # parametric equation generate x, y, z coordinates of points on the sphere
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    return go.Surface(x=x, y=y, z=z, opacity=0.3, colorscale='Viridis')

def plotTracer(points):
    """
    Create a plotly trace for the points.

    @param points: array of shape (n, 3) representing 3D points.
    @return: RETURNS FINAL PLOTLY GRAPH
    """
    return go.Scatter3d(x=points[:, 0], y=points[:, 1], z=points[:, 2],
                        mode='markers', marker=dict(size=5, color='red'))

def traceTetra(points, hull):
    """
    Create a plotly trace for the tetrahedron.

    @param points: array of shape (n, 3) representing 3D points.
    @param hull: convex hull of the points.
    @return: gives a mesh trace of it all
    """
    return go.Mesh3d(
        x=points[hull.vertices, 0],
        y=points[hull.vertices, 1],
        z=points[hull.vertices, 2],
        i=hull.simplices[:, 0],
        j=hull.simplices[:, 1],
        k=hull.simplices[:, 2],
        opacity=0.3,
        color='blue'
    )

def makeCenterOfSphere():
    """
    REad the name of the function
    """
    return go.Scatter3d(x=[0], y=[0], z=[0], mode='markers',
                        marker=dict(size=5, color='green'))

def traceEdges(points, hull):
    """
    create plotly traces for the edges of the tetrahedron.

    @return: List of plotly scatter traces representing the edges of the tetrahedron.
    """
    edges_trace = []
    for simplex in hull.simplices:
        for i in range(3):
            edge = np.array([points[simplex[i], :], points[simplex[(i + 1) % 3], :]])
            edge_trace = go.Scatter3d(x=edge[:, 0], y=edge[:, 1], z=edge[:, 2],
                                      mode='lines', line=dict(color='black', width=3))
            edges_trace.append(edge_trace)
    return edges_trace

def plotToMakeTetra():
    """
    plot random points on a sphere and the resulting tetrahedron.
    """
    points = getRandomPoints()
    hull = getHull(points)

    sphere_trace = spherePlotly()
    points_trace = plotTracer(points)
    tetrahedron_trace = traceTetra(points, hull)
    center_trace = makeCenterOfSphere()
    edges_trace = traceEdges(points, hull)

    layout = go.Layout(scene=dict(aspectmode='data'), title='Points:')
    fig = go.Figure(data=[sphere_trace, points_trace, tetrahedron_trace, center_trace] + edges_trace, layout=layout)

    fig.show()

if __name__ == "__main__":
    plotToMakeTetra()
