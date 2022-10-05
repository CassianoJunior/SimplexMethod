import utils

HAS_SOLUTION = 0
ILIMITED_SOLUTION = 1
INFINITE_SOLUTIONS = 2
NO_SOLUTION = 3

def execute(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount, isMaxProblem = False, needFirstPhase = False):
  if not needFirstPhase:
    return executePhase2(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase)
  else:
    return executePhase1(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount, isMaxProblem, needFirstPhase)

def executePhase1(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount, isMaxProblem, needFirstPhase):
  solutionType = HAS_SOLUTION
  tableau = utils.createTableau(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount, isMaxProblem, needFirstPhase)
  utils.showTableau(tableau)
  tableau = utils.toCanonicForm(tableau, artificialVariablesAmount, needFirstPhase)
  utils.showTableau(tableau)

  isBestSolution, inputVariable = utils.checkOptimality(tableau)
  utils.showTableau(tableau)

  while not isBestSolution:
    outputVariable = utils.getOutputVariable(tableau, inputVariable)
    tableau = utils.pivoting(tableau, inputVariable, outputVariable, artificialVariablesAmount, needFirstPhase)
    isBestSolution, inputVariable = utils.checkOptimality(tableau)
    utils.showTableau(tableau)
  
  if tableau[len(tableau)-1][len(tableau[0])-1] != 0:
    solutionType = NO_SOLUTION
    return tableau, solutionType

  updatedConstraints, updatedBVector, baseVariables = utils.turnTableauToPhase2(tableau, artificialVariablesAmount)
  
  return executePhase2(objectiveFunction, updatedConstraints, updatedBVector, isMaxProblem, False, baseVariables)

  

def executePhase2(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase, baseVariables = []):
  solutionType = HAS_SOLUTION
  tableau = utils.createTableau(objectiveFunction, constraintMatrix, bVector, 0, isMaxProblem, needFirstPhase, baseVariables)
  utils.showTableau(tableau)
  tableau = utils.toCanonicForm(tableau, 0, needFirstPhase)
  utils.showTableau(tableau)

  isBestSolution, inputVariable = utils.checkOptimality(tableau)

  while not isBestSolution:
    isUnbounded = utils.checkUnboundedness(tableau, inputVariable)
    
    if isUnbounded:
      solutionType = ILIMITED_SOLUTION
      break

    outputVariable = utils.getOutputVariable(tableau, inputVariable)
    tableau = utils.pivoting(tableau, inputVariable, outputVariable, 0, needFirstPhase)

    utils.showTableau(tableau)

    isBestSolution, inputVariable = utils.checkOptimality(tableau)
  
  multiplyer = 1 if isMaxProblem else -1

  tableau[len(tableau)-1][len(tableau[0])-1] *= multiplyer

  isEndless = utils.checkEndless(tableau)
  if solutionType == HAS_SOLUTION and isEndless: solutionType = INFINITE_SOLUTIONS

  return tableau, solutionType
