import cv2
import numpy as np
import random
import math

class environment:
    def environment(self):
        map_height, map_width = 500, 1200
        map = np.zeros((map_height, map_width, 3), dtype=np.uint8)  # Empty image for map
        # Create the obstacles (all obstacles are red in color)
        num_obstacles = random.randint(5, 10)  # Random number of obstacles between 5 and 10
        for _ in range(num_obstacles):
            # Random coordinates for the top-left corner of the obstacle
            x1 = random.randint(0, map_width)
            y1 = random.randint(0, map_height)
            # Random coordinates for the bottom-right corner of the obstacle
            x2 = x1 + random.randint(50, 150)
            y2 = y1 + random.randint(100, 200)
            # Ensure the obstacle is within the map boundaries
            x2 = min(x2, map_width)
            y2 = min(y2, map_height)
            # Draw the obstacle on the map
            map[y1:y2, x1:x2, :] = [0, 0, 255]
        return map
    
class RRT_Connect:
    def __init__(self, map, start, goal):

        self.map = map

        cv2.circle(self.map, (start[0], start[1]), 3, [0,255,0], -1)
        cv2.circle(self.map, (goal[0], goal[1]), 3, [0,255,0], -1)


        self.start = np.array(start)
        self.goal = np.array(goal)
        self.step_length = 10

        self.T_a = self.init_tree(self.start)
        self.T_b = self.init_tree(self.goal)
        
        self.iterate_rrt_connect()

    def init_tree(self,q):
        tree = {
                "vertices": [ { "vertex":q, "edges":[] } ],
                "newest": 0
                }
        return tree

    def iterate_rrt_connect(self):
        # Create a random configuration
        while(True):
            x_cord = random.randrange(0,1200)
            y_cord = random.randrange(0,500)
            q_rand = np.array([x_cord, y_cord])
            if(self.check_collision(q_rand) == False):
                break

        extension_1 = self.extendTowardsPoint(self.T_a, q_rand)

        if(extension_1 != "obstacle"):
            q_latest_index = len(self.T_a["vertices"])-1
            q_latest = self.T_a["vertices"][q_latest_index]["vertex"]
            extension_2 = self.extendTowardsPoint(self.T_b, q_latest)
            if(extension_2 == "connected"):
                print("trees connected")
                cv2.imshow("frame", self.map)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


        
    def extendTowardsPoint(self, tree, point):
        min_dist = math.inf
        nearest_index = 0
        for i in range(len(tree['vertices'])):
            dist = self.euclideanDistance(tree['vertices'][i]['vertex'], point)
            if(dist<min_dist):
                min_dist = dist
                nearest_index = i
        
        nearest = tree['vertices'][nearest_index]['vertex']

        if (self.euclideanDistance(nearest, point) <= self.step_length):
            q_new = point
            collision = self.check_collision(q_new)
            goal_reached = True
        
        else:
            x_new = int(nearest[0] + (((point[0]-nearest[0])*self.step_length)/self.euclideanDistance(nearest, point)))
            y_new = int(nearest[1] + (((point[1]-nearest[1])*self.step_length)/self.euclideanDistance(nearest, point)))
            q_new = np.array([x_new, y_new])
            collision = self.check_collision(q_new)
            goal_reached = False

        if(collision == False):
            self.insertTreeVertex(tree, q_new)
            self.insertTreeEdge(tree, nearest_index, tree["newest"])
            if(goal_reached == True):
                return "connected"
        else:
            return "obstacle"
        
    def insertTreeVertex(self,tree, q):
        new_vertex = { "vertex": q, "edges": []}
        tree["vertices"].append(new_vertex)
        tree["newest"] = len(tree["vertices"])-1
        
        self.draw_point(q)

    def insertTreeEdge(self, tree, q1_idx, q2_idx):
        tree["vertices"][q1_idx]["edges"].append(tree["vertices"][q2_idx])
        tree["vertices"][q2_idx]["edges"].append(tree["vertices"][q1_idx])


        
    def draw_point(self, q):
        cv2.circle(self.map, (q[0],q[1]), 1, [255,0,0], -1)

    def euclideanDistance(self, point1, point2):
        dist = math.sqrt(math.pow((point1[0]-point2[0]),2) + math.pow((point1[1]-point2[1]),2))
        return dist

    def check_collision(self, configuration):
        if(list(self.map[configuration[1],configuration[0]]) == [0,0,255]):
            return True
        else:
            return False       


if __name__ == "__main__":
    map_obj = environment()
    map = map_obj.environment()
    
    start = RRT_Connect(map, [20,30], [700,650])
    # cv2.imshow("frame", map)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

        

        