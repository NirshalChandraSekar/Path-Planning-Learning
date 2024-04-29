import cv2
import numpy as np
import random

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


if __name__ == "__main__":
    map_obj = environment()
    map = map_obj.environment()
    
    cv2.imshow("frame", map)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

        

        