import utils

HAS_SOLUTION = 0
ILIMITED_SOLUTION = 1
INFINITE_SOLUTIONS = 2

def execute(objectiveFunction, constraintMatrix, bVector, isMaxProblem = False, needFirstPhase = False):
  if not needFirstPhase:
    return executePhase2(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase)

def executePhase2(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase):
  solutionType = HAS_SOLUTION
  tableau = utils.createTableau(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase)
  utils.showTableau(tableau)
  tableau = utils.toCanonicForm(tableau)
  utils.showTableau(tableau)

  bestSolution, inputVariable = utils.checkOptimality(tableau)

  while not bestSolution:
    isUnbounded = utils.checkUnboundedness(tableau, inputVariable)
    
    if isUnbounded:
      solutionType = ILIMITED_SOLUTION
      break

    outputVariable = utils.getOutputVariable(tableau, inputVariable)
    tableau = utils.pivoting(tableau, inputVariable, outputVariable)

    utils.showTableau(tableau)

    bestSolution, inputVariable = utils.checkOptimality(tableau)
  
  multiplyer = 1 if isMaxProblem else -1

  tableau[len(tableau)-1][len(tableau[0])-1] *= multiplyer

  isEndless = utils.checkEndless(tableau)
  if solutionType == HAS_SOLUTION and isEndless: solutionType = INFINITE_SOLUTIONS

  return tableau, solutionType
