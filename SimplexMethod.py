import utils


def execute(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase):
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
  

  print("Best solution: Z* = ", -1*tableau[len(tableau)-1][len(tableau[0])-1])
  print("Base variables: ")
  baseVariables = utils.getBaseVariables(tableau, utils.getTableauConstraints(tableau))
  nonBaseVariables = utils.getNonBaseVariables(tableau)
  for variable in baseVariables:
    print(f"\tx{variable}* = {tableau[baseVariables.index(variable)+1][len(tableau[0])-1]}")
  print("Non-base variables: ")
  for variable in nonBaseVariables:
    print(f"\tx{variable}* = 0")

def executePhase2(function, constraints, isMaxProblem):
  tableau = utils.createTableau(function, constraints, isMaxProblem)
