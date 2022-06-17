## Assignment 4
1. I'm not really sure the name but have seen this before. If I were to guess, it would be called Flyweight Design Pattern
2. It is a structural design pattern. It helps to decrease object count thus improving application required objects structure reducing the memory load. In the diagram, a list of Students are present to be reuse, so if it were to create a new object, it will first check whether such an object is already exists and can be reused, otherwise the object is created and added to the pool for future reuse.


3 & 4. I've created a simplified class without using Hash like map that could have been better and more efficient.  
  

###  Requirement:
  NodeJs > v16.15.0


###  Perform the following steps:

  ``npm install``

  ``npx ts-node flyweightPattern.ts``