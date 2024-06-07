import multiprocessing
import json
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import os


def pointGenerator(num_points=4):
    """
    Generate random points on the surface of a sphere.

    @param num_points Number of points to generate (default is 4).
    """
    points = np.random.randn(num_points, 3)
    points /= np.linalg.norm(points, axis=1)[:, np.newaxis]
    # Normalize the points to lie on the unit sphere
    return points


def isInCenter(points):
    """
    Check if the center of the sphere lies inside the tetrahedron formed by the points.

    @param points Numpy array of shape (4, 3) representing points on the sphere.
    @return Boolean indicating if the center is inside the tetrahedron.
    """
    hull = ConvexHull(points)
    center = np.array([0, 0, 0])
    equations = hull.equations
    signs = np.sign(np.dot(equations[:, :-1], center) + equations[:, -1])
    return bool(np.all(signs <= 0) or np.all(signs >= 0))


def makePlot(points, index, inside, probability):
    """
    Create a 3D plot of the tetrahedron and the sphere, with annotations.

    Only saves the image for every 1000th iteration to save space.

    @param points Numpy array of shape (4, 3) representing points on the sphere.
    @param index val of the current iteration.
    @param inside Boolean indicating if the center is inside the tetrahedron.
    @param probability Current probability of the center being inside the tetrahedron.
    """
    if index % 100000 != 0:
        return

    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')
    hull = ConvexHull(points)

    # wireframe with parametric coordinates of the sphere
    u, v = np.mgrid[0:2 * np.pi:100j, 0:np.pi:50j]
    x = np.cos(u) * np.sin(v)
    y = np.sin(u) * np.sin(v)
    z = np.cos(v)
    ax.plot_wireframe(x, y, z, color='gray', alpha=0.3)

    # convex hull of the 4 points to make a tetrahedron
    for simplex in hull.simplices:
        triangle = Poly3DCollection([points[simplex]])
        triangle.set_color('cyan')
        triangle.set_edgecolor('black')
        ax.add_collection3d(triangle)

    # plotting the points
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], color='red')
    ax.scatter(0, 0, 0, color='green')  # Center of the sphere

    # bounds of the graph
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_zlim([-1, 1])

    # CENTER for center
    ax.text(0, 0, 0, f'(0, 0, 0)', color='black')

    if inside:
        status = "Inside"
    else:
        status = "Outside"
    ax.text2D(0.05, 0.95, f"Index: {index}\nProbability: {probability:.5f}\nCenter: {status}", transform=ax.transAxes)

    # Point table on image
    table_data = [["Point", "Coordinates"]]
    for i, (x, y, z) in enumerate(points):
        table_data.append([f"Point {i + 1}", f"({x:.2f}, {y:.2f}, {z:.2f})"])

    ax.table(cellText=table_data, loc='upper right', colWidths=[0.2, 0.2], cellLoc='center', fontsize=10)

    if not os.path.exists('simulation_images'):
        os.makedirs('simulation_images')
    plt.savefig(f'simulation_images/tetrahedron_{index}.png')
    plt.close()


def saveData(points, index, inside, probability):
    """
    Save the current data to a JSON file.

    @param points Numpy array of shape (4, 3) representing points on the sphere.
    @param index val of the current iteration.
    @param inside Boolean indicating if the center is inside the tetrahedron.
    @param probability Current probability of the center being inside the tetrahedron.
    """
    data = {
        'index': index,
        'probability': probability,
        'inside': inside,
        'points': points.tolist()
    }
    with open('currentData.json', 'w') as f:
        json.dump(data, f, indent=4)


def simulate_single(max_size_bytes):
    """
    Simulate the generation of points and check if the center is inside the tetrahedron.

    @param max_size_bytes Maximum size in bytes for the generated images.
    @return Probability of the center being inside the tetrahedron.
    """
    inside_count = 0
    total_size = 0
    probability = 0
    i = 0

    while total_size <= max_size_bytes:
        points = pointGenerator()
        inside = isInCenter(points)
        if inside:
            inside_count += 1
        probability = inside_count / (i + 1)
        makePlot(points, i, inside, probability)
        saveData(points, i, inside, probability)  #SAVE TO JSON

        if i % 100000 == 0:
            total_size = sum(os.path.getsize(os.path.join('simulation_images', f))
                             for f in os.listdir('simulation_images') if
                             os.path.isfile(os.path.join('simulation_images', f)))

        i += 1

    return probability


def compileSize(max_size_bytes=1000000000):
    """
    Run the simulation until the total size of generated images reaches a specified limit.
    1 GB
    """
    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)
    results = pool.map(simulate_single, [max_size_bytes] * num_cores)
    pool.close()
    pool.join()

    probability = sum(results) / len(results)

    print(f'Final Result {probability:.6f}')


if __name__ == "__main__":
    compileSize()
