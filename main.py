from createLines import createLineSegments
from visualizer.main import Visualizer 
from Bentley_Ottmann import findIntersections
# from generatePolygon import generatePolygonPoints

def visualizeSegments():
    #
    segments = createLineSegments()
    vis = Visualizer()
    vis.add_line_segment(segments) 
    vis.show() 

    crossed = findIntersections(segments)
    crossed = list( crossed )

    vis = Visualizer()
    vis.add_line_segment(segments)
    vis.add_point(crossed, color = "green", s = 30)
    vis.show()

# end procedure visualizeSegments() 
    
visualizeSegments()

# Example:
# vis = Visualizer()
# points = [((-12.500000000000002, 3.290043290043293), (-9.758064516129036, 6.753246753246756)), ((-7.580645161290324, 6.64502164502165), (-5.806451612903228, 2.3160173160173194)), ((-4.032258064516132, 2.0995670995671034), (-1.612903225806452, 6.536796536796537)), ((0.08064516129032029, 6.536796536796537), (1.774193548387096, 1.8831168831168839)), ((-13.548387096774196, 16.709956709956714), (16.774193548387096, -1.5800865800865793)), ((-14.59677419354839, -11.103896103896103), (12.903225806451609, 5.995670995670999)), ((10.806451612903224, 3.1818181818181834), (12.096774193548384, 3.1818181818181834))]
# for (pointA, pointB) in points:
#     vis.add_point( (pointA, pointB), color = "black")
# vis.add_line_segment(points)
# vis.show()