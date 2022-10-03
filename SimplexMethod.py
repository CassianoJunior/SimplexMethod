import utils


def execute(objectiveFunction, constraintMatrix, bVector, isMaxProblem = False, needFirstPhase = False):
  if not needFirstPhase:
    return executePhase2(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase)

def executePhase2(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase):
  tableau = utils.createTableau(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase)
  utils.showTableau(tableau)
  tableau = utils.toCanonicForm(tableau)
  utils.showTableau(tableau)

  bestSolution, inputVariable = utils.checkOptimality(tableau)

  while not bestSolution:
    outputVariable = utils.getOutputVariable(tableau, inputVariable)
    tableau = utils.pivoting(tableau, inputVariable, outputVariable)

    utils.showTableau(tableau)

    bestSolution, inputVariable = utils.checkOptimality(tableau)
  
  multiplyer = 1 if isMaxProblem else -1

  tableau[len(tableau)-1][len(tableau[0])-1] *= multiplyer

  return tableau
