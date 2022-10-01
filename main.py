import SimplexMethod

if __name__ ==  '__main__':
  # Make sure the input is in standard form before calling the SimplexMethod
  SimplexMethod.execute(
    objectiveFunction = [-5, -2, 0, 0, 0], # objective function
    constraintMatrix = [ # constraint matrix
      [1, 0, 1, 0, 0], 
      [0, 1, 0, 1, 0], 
      [1, 2, 0, 0, 1]
    ], 
    bVector = [ #Vector b
      [3], 
      [4], 
      [9]
    ], 
    isMaxProblem=False,
    needFirstPhase=False
  )

