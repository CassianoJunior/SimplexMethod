import SimplexMethod
import utils

if __name__ ==  '__main__':
  # Make sure the input is in standard form before calling the SimplexMethod
  tableau, solutionType = SimplexMethod.execute(
    objectiveFunction = [330, 300, 420, 0, 0, 0, 0, 0], # objective function
    constraintMatrix = [ # constraint matrix
      [5.1, 3.6, 6.8, 1, 0, 0, 0, 0], 
      [2, 0, 0, 0, 1, 0, 0, 0], 
      [0, 2, 0, 0, 0, 1, 0, 0],
      [0, 0, 2, 0, 0, 0, 1, 0],
      [1, (3/4), (5/3), 0, 0, 0, 0, 1]
    ], 
    bVector = [ #Vector b
      [220], 
      [40], 
      [30],
      [10],
      [40]
    ], 
    isMaxProblem=True,
    needFirstPhase=False
  )

  # Output:
  if solutionType == SimplexMethod.ILIMITED_SOLUTION:
    print("Ilimited solution")
    utils.showTableau(tableau)
  elif solutionType == SimplexMethod.HAS_SOLUTION or solutionType == SimplexMethod.INFINITE_SOLUTIONS:
    print("Infinite solutions") if solutionType == SimplexMethod.INFINITE_SOLUTIONS else print("Has solution")
    print("Best solution: Z* = ", tableau[len(tableau)-1][len(tableau[0])-1])
    print("Base variables: ")
    baseVariables = utils.getBaseVariables(tableau, utils.getTableauConstraints(tableau))
    nonBaseVariables = utils.getNonBaseVariables(tableau)
    for variable in baseVariables:
      print(f"  x{variable}* = {tableau[baseVariables.index(variable)+1][len(tableau[0])-1]}")
    print("Non-base variables: ")
    for variable in nonBaseVariables:
      print(f"  x{variable}* = 0")

