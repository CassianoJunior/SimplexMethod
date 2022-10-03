import re


def createTableau(objectiveFunction, constraintMatrix, bVector, isMaxProblem, needFirstPhase):
  if not needFirstPhase:
    tableau = createTableauToSecondPhase(objectiveFunction, constraintMatrix, bVector, isMaxProblem)
  else: 
    tableau = createTableauToFirstPhase(objectiveFunction, constraintMatrix, bVector, isMaxProblem)

  return tableau
  
def createTableauToSecondPhase(objectiveFunction, constraintMatrix, bVector, isMaxProblem):
  if isMaxProblem: objectiveFunction = [-1 * x for x in objectiveFunction]

  sizeOfConstraints = len(constraintMatrix)

  tableau = [None]*(sizeOfConstraints + 2)
  for i in range(len(tableau)):
    tableau[i] = [None]*(len(constraintMatrix[0]) + 2)

  slackVariablesAmount = objectiveFunction.count(0)

  nextSlackVariableToInsertInBase = len(objectiveFunction) - slackVariablesAmount + 1

  for line in range(len(tableau)):
    for column in range(len(tableau[line])):
      if line == 0 and column == 0: tableau[line][column] = "Base"
      elif line == 0 and column > 0 and column < len(tableau[line]) - 1: tableau[line][column] = "x" + str(column)
      elif line == 0 and column == len(tableau[line]) - 1: tableau[line][column] = "b"
      elif column == 0 and line < sizeOfConstraints+1 and line > 0:
        tableau[line][column] = "x" + str(nextSlackVariableToInsertInBase)
        nextSlackVariableToInsertInBase += 1
      elif column <= len(objectiveFunction) and column != 0 and line > 0:
        if line == len(tableau) - 1:
          tableau[line][column] = objectiveFunction[column - 1]
        else:
          tableau[line][column] = constraintMatrix[line - 1][column - 1]
      elif column == len(tableau[line]) - 1 and line < sizeOfConstraints+1:
        tableau[line][column] = bVector[line-1][0]
      
      if column == 0 and line == sizeOfConstraints+1: tableau[line][column] = 'c'
      if column == len(tableau[line]) - 1 and line == sizeOfConstraints+1: tableau[line][column] = 0
  
  return tableau

def createTableauToFirstPhase():
  pass

def toCanonicForm(tableau):
  constraints = getTableauConstraints(tableau)
  baseVariables = getBaseVariables(tableau, constraints)

  tableauWithIdentitySubmatrix = generatingIdentitySubmatrix(tableau, baseVariables)
  canonicTableau = expressObjectiveFunctionWithNonBasicVariables(tableauWithIdentitySubmatrix, baseVariables)

  return canonicTableau


def getTableauConstraints(tableau):
  constraints = []
  for i in range(len(tableau) - 1):
    constraint = []
    for j in range(len(tableau[i])):
      if j > 0 and j < len(tableau[i]): constraint.append(tableau[i][j])
    constraints.append(constraint)
  
  return constraints

def getBaseVariables(tableau, constraints):
  baseVariables = []
  for i in range(len(constraints)):
    if i < len(tableau) and i > 0: baseVariables.append(int(re.findall(r'[0-9]+', tableau[i][0])[0]))
  
  return baseVariables

def getNonBaseVariables(tableau):
  nonBaseVariables = []
  for column in range(1, len(tableau[0])-1):
    if tableau[len(tableau)-1][column] != 0: nonBaseVariables.append(column)
  return nonBaseVariables

def generatingIdentitySubmatrix(tableau, variables):
  for variable in variables:
    variableLine = variables.index(variable)+1
    if tableau[variableLine][variable] != 1:
      value = tableau[variableLine][variable]
      for column in range(1, len(tableau[0])):
        tableau[variableLine][column] /= value

    for line in range(1, len(tableau)-1):
      if line != variableLine and tableau[line][variable] != 0:
        value = tableau[line][variable]
        for column in range(1, len(tableau[0])):
          tableau[line][column] -= value * tableau[variableLine][column]
         
  return tableau

def expressObjectiveFunctionWithNonBasicVariables(tableau, variables):
  for variable in variables:
    variableLine = variables.index(variable)+1
    objectiveFunctionLine = len(tableau) - 1
    if tableau[objectiveFunctionLine][variable] != 0:
      value = tableau[objectiveFunctionLine][variable]
      for column in range(1, len(tableau[0])):
        tableau[objectiveFunctionLine][column] -= tableau[variableLine][column] * value

  return tableau

def checkOptimality(tableau):
  objectiveFunctionLine = len(tableau) - 1
  for column in range(1, len(tableau[0])-1):
    if tableau[objectiveFunctionLine][column] < 0: return False, column

  return True, None

def getOutputVariable(tableau, inputVariable):
  lowerValue = None
  outputVariable = None
  for line in range(1, len(tableau)-1):
    if tableau[line][inputVariable] > 0:
      bValue = tableau[line][len(tableau[line])-1]
      if lowerValue == None: 
        lowerValue = bValue / tableau[line][inputVariable]
        outputVariable = line
      elif bValue / tableau[line][inputVariable] < lowerValue: 
        lowerValue = bValue / tableau[line][inputVariable]
        outputVariable = line
  
  return outputVariable

def pivoting(tableau, inputVariable, outputVariable):
  tableau[outputVariable][0] = "x" + str(inputVariable)

  tableau = toCanonicForm(tableau)
  
  return tableau

def showTableau(tableau):
  for i in range(len(tableau)):
    for j in range(len(tableau[i])):
      print("%7.1f" %tableau[i][j], end=" ") if type(tableau[i][j]) is not str else print("%7s" %tableau[i][j], end=" ")
    print()
  print()
