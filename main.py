import SimplexMethod

if __name__ ==  '__main__':
  # Make sure the input is in standard form before calling the SimplexMethod
  SimplexMethod.execute(
    objectiveFunction = [-2, -1, 1, 0, 0], # objective function
    constraintMatrix = [ # constraint matrix
      [1, 1, 2, 1, 0], 
      [1, 4, -1, 0, 1]
    ], 
    bVector = [ #Vector b
      [6], 
      [4]
    ], 
    isMaxProblem=False,
    needFirstPhase=False
  )

