from unittest import TestCase, main

import SimplexMethod
import utils


def executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector):
  self.assertEqual(solutionType, expectedSolution)
  if expectedSolution == SimplexMethod.NO_SOLUTION: return
  self.assertEqual(tableau[len(tableau)-1][len(tableau[0])-1], zValue)

  bVector = utils.getBVector(tableau)
  for value in bVector:
    self.assertTrue(value[0] in expectedBVector)

  baseVariables = utils.getBaseVariables(tableau, utils.getTableauConstraints(tableau), 0, False)
  for variable in baseVariables:
    self.assertTrue(variable in expectedBaseVariables)
    variableLine = baseVariables.index(variable) + 1
    self.assertEqual(tableau[variableLine][len(tableau[0])-1], bVector[variableLine-1][0])
  nonBaseVariables = utils.getNonBaseVariables(tableau)
  for variable in nonBaseVariables:
    self.assertTrue(variable in expectedNonBaseVariables)

class TestSimplexMethod(TestCase):
  def test_firstMinimizationProblemWithPhase2OnlyHasSolution(self):
    tableau, solutionType = SimplexMethod.execute(
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
      artificialVariablesAmount=0,
      isMaxProblem=False,
      needFirstPhase=False
    )

    zValue = -21
    expectedSolution = SimplexMethod.HAS_SOLUTION
    expectedBaseVariables = [1, 2, 4]
    expectedNonBaseVariables = [3, 5]
    expectedBVector = [3, 1, 3]

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)
    
  def test_secondMinimizationProblemWithPhase2OnlyHasSolution(self):
    tableau, solutionType = SimplexMethod.execute(
      objectiveFunction = [-20, -24, 0, 0], # objective function
      constraintMatrix = [ # constraint matrix
        [3, 6, 1, 0], 
        [4, 2, 0, 1]
      ], 
      bVector = [ #Vector b
        [60], 
        [32]
      ],
      artificialVariablesAmount=0,
      isMaxProblem=False,
      needFirstPhase=False
    )

    zValue = -272
    expectedSolution = SimplexMethod.HAS_SOLUTION
    expectedBaseVariables = [1, 2]
    expectedNonBaseVariables = [3, 4]
    expectedBVector = [8, 4]

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)

  def test_firstMinimizationProblemWithPhase1AndPhase2HasSolution(self):
    tableau, solutionType = SimplexMethod.execute(
      objectiveFunction = [-6, 1, 0, 0], # objective function
      constraintMatrix = [ # constraint matrix
        [4, 1, 1, 0], 
        [2, 3, 0, -1], 
        [-1, 1, 0, 0]
      ], 
      bVector = [ #Vector b
        [21], 
        [13], 
        [1]
      ],
      artificialVariablesAmount=2,
      isMaxProblem=False,
      needFirstPhase=True
    )

    zValue = -19
    expectedSolution = SimplexMethod.HAS_SOLUTION
    expectedBaseVariables = [1, 2, 4]
    expectedNonBaseVariables = [3]
    expectedBVector = [10, 4, 5]

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)

  def test_secondMinimizationProblemWithPhase1AndPhase2HasSolution(self):
    tableau, solutionType = SimplexMethod.execute(
      objectiveFunction = [-5, -2, 0, 0, 0], # objective function
      constraintMatrix = [ # constraint matrix
        [1, 2, -1, 0, 0], 
        [1, 0, 0, 1, 0], 
        [0, 1, 0, 0, 1]
      ], 
      bVector = [ #Vector b
        [9], 
        [3], 
        [4]
      ],
      artificialVariablesAmount=1,
      isMaxProblem=False,
      needFirstPhase=True
    )

    zValue = -23
    expectedSolution = SimplexMethod.HAS_SOLUTION
    expectedBaseVariables = [1, 2, 3]
    expectedNonBaseVariables = [4, 5]
    expectedBVector = [3, 2, 4]

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)

  def test_firstMaxmizationProblemWithPhase1AndPhase2HasSolution(self):
    tableau, solutionType = SimplexMethod.execute(
      objectiveFunction = [6, -1, 0, 0], # objective function
      constraintMatrix = [ # constraint matrix
        [4, 1, 1, 0],
        [2, 3, 0, -1],
        [-1, 1, 0, 0]
      ], 
      bVector = [ #Vector b
        [21],
        [13],
        [1]
      ],
      artificialVariablesAmount=2,
      isMaxProblem=True,
      needFirstPhase=True
    )

    zValue = 19
    expectedSolution = SimplexMethod.HAS_SOLUTION
    expectedBaseVariables = [1, 2, 4]
    expectedNonBaseVariables = [3]
    expectedBVector = [10, 4, 5]

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)


  def test_minimizationProblemWithPhase1AndPhase2NoSolution(self):
    tableau, solutionType = SimplexMethod.execute(
      objectiveFunction = [-3, 4, 0, 0], # objective function
      constraintMatrix = [ # constraint matrix
        [1, 1, 1, 0], 
        [2, 3, 0, -1]
      ], 
      bVector = [ #Vector b
        [4], 
        [18]
      ],
      artificialVariablesAmount=1,
      isMaxProblem=False,
      needFirstPhase=True
    )

    zValue = None
    expectedSolution = SimplexMethod.NO_SOLUTION
    expectedBaseVariables = []
    expectedNonBaseVariables = []
    expectedBVector = []

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)

  def test_secondMaximizationProblemWithPhase1AndPhase2HasSolution(self):
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

    zValue = 1
    expectedSolution = SimplexMethod.HAS_SOLUTION
    expectedBaseVariables = [3, 2]
    expectedNonBaseVariables = [1]
    expectedBVector = [0, 1]

    executeAsserts(self, tableau, solutionType, zValue, expectedSolution, expectedBaseVariables, expectedNonBaseVariables, expectedBVector)

if __name__ == '__main__':
  main()
