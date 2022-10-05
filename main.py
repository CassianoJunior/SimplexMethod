import SimplexMethod
import utils

if __name__ ==  '__main__':
  # Make sure the input is in standard form before calling the SimplexMethod
  # tableau, solutionType = SimplexMethod.execute(
  #   objectiveFunction = [-6, 1, 0, 0], # objective function
  #   constraintMatrix = [ # constraint matrix
  #     [4, 1, 1, 0], 
  #     [2, 3, 0, -1], 
  #     [-1, 1, 0, 0],
  #   ], 
  #   bVector = [ #Vector b
  #     [21], 
  #     [13], 
  #     [1]
  #   ],
  #   artificialVariablesAmount=2,
  #   isMaxProblem=False,
  #   needFirstPhase=True
  # )

  # tableau, solutionType = SimplexMethod.execute(
  #     objectiveFunction = [-5, -2, 0, 0, 0], # objective function
  #     constraintMatrix = [ # constraint matrix
  #       [1, 2, -1, 0, 0], 
  #       [1, 0, 0, 1, 0], 
  #       [0, 1, 0, 0, 1]
  #     ], 
  #     bVector = [ #Vector b
  #       [9], 
  #       [3], 
  #       [4]
  #     ],
  #     artificialVariablesAmount=1,
  #     isMaxProblem=False,
  #     needFirstPhase=True
  #   )

  # tableau, solutionType = SimplexMethod.execute(
  #     objectiveFunction = [-3, 4, 0, 0], # objective function
  #     constraintMatrix = [ # constraint matrix
  #       [1, 1, 1, 0], 
  #       [2, 3, 0, -1]
  #     ], 
  #     bVector = [ #Vector b
  #       [4], 
  #       [18]
  #     ],
  #     artificialVariablesAmount=1,
  #     isMaxProblem=False,
  #     needFirstPhase=True
  #   )

  # tableau, solutionType = SimplexMethod.execute(
  #     objectiveFunction = [6, -1, 0, 0], # objective function
  #     constraintMatrix = [ # constraint matrix
  #       [4, 1, 1, 0],
  #       [2, 3, 0, -1],
  #       [-1, 1, 0, 0]
  #     ], 
  #     bVector = [ #Vector b
  #       [21],
  #       [13],
  #       [1]
  #     ],
  #     artificialVariablesAmount=2,
  #     isMaxProblem=True,
  #     needFirstPhase=True
  #   )

  tableau, solutionType = SimplexMethod.execute(
      objectiveFunction = [1, 1, 0], # objective function
      constraintMatrix = [ # constraint matrix
        [1, 4, -1], 
        [3, 1, 0]
      ], 
      bVector = [ #Vector b
        [4], 
        [1]
      ],
      artificialVariablesAmount=2,
      isMaxProblem=True,
      needFirstPhase=True
    )


  # Output:
  if solutionType == SimplexMethod.ILIMITED_SOLUTION:
    print("Ilimited solution")
    utils.showTableau(tableau)
  elif solutionType == SimplexMethod.HAS_SOLUTION or solutionType == SimplexMethod.INFINITE_SOLUTIONS:
    print("Infinite solutions") if solutionType == SimplexMethod.INFINITE_SOLUTIONS else print("Has solution")
    print("Best solution: Z* = ", tableau[len(tableau)-1][len(tableau[0])-1])
    print("Base variables: ")
    baseVariables = utils.getBaseVariables(tableau, utils.getTableauConstraints(tableau), 0, False)
    nonBaseVariables = utils.getNonBaseVariables(tableau)
    for variable in baseVariables:
      print(f"  x{variable}* = {tableau[baseVariables.index(variable)+1][len(tableau[0])-1]}")
    print("Non-base variables: ")
    for variable in nonBaseVariables:
      print(f"  x{variable}* = 0")
  elif solutionType == SimplexMethod.NO_SOLUTION:
    print("No solution")

