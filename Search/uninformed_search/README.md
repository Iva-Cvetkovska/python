# Explorer
The goal is to get our explorer to his house safely, without coliding with existing obstacles that are moving vertically.</br>

# Stars
By using both knight and bishop, we mimic the same movements as in chess and try to collect the randomly placed stars in the most optimal way.</br></br>

*in both cases breadth first graph search is used as the most safe bet for an optimal solution*

# Snake
In this problem, there is an additional layer of complexity: we need to keep track of the **direction** in which the snake is facing. Possible directions are: north (N), south (S), east (E), west (W). The objective is to **eat all green apples** and avoid the red ones as they are poisonous. The only **allowed actions** are moveForward, turnLeft and turnRight. 