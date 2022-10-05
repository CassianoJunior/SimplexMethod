import re


def createTableau(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount, isMaxProblem, needFirstPhase, baseVariables=[]):
  if isMaxProblem: objectiveFunction = [-1 * x for x in objectiveFunction]

  if not needFirstPhase:
    tableau = createTableauToSecondPhase(objectiveFunction, constraintMatrix, bVector, baseVariables)
  else: 
    tableau = createTableauToFirstPhase(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount)

  return tableau
  
def createTableauToSecondPhase(objectiveFunction, constraintMatrix, bVector, baseVariables = []):
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
        if len(baseVariables) > 0:
          tableau[line][column] = "x" + str(baseVariables[line-1])
        else:
          tableau[line][column] = "x" + str(nextSlackVariableToInsertInBase)
          nextSlackVariableToInsertInBase += 1
      elif column <= len(objectiveFunction) and column != 0 and line > 0:
        if line == len(tableau) - 1:
          tableau[line][column] = objectiveFunction[column - 1]
        else:
          tableau[line][column] = constraintMatrix[line - 1][column - 1]
      elif column == len(tableau[line]) - 1 and line < sizeOfConstraints+1:
        tableau[line][column] = bVector[line-1][0]
      
      if column == 0 and line == sizeOfConstraints+1: tableau[line][column] = 'Z'
      if column == len(tableau[line]) - 1 and line == sizeOfConstraints+1: tableau[line][column] = 0
  
  return tableau

def createTableauToFirstPhase(objectiveFunction, constraintMatrix, bVector, artificialVariablesAmount):
  sizeOfConstraints = len(constraintMatrix)

  tableau = [None]*(sizeOfConstraints + 2)
  for i in range(len(tableau)):
    tableau[i] = [None]*(len(constraintMatrix[0]) + artificialVariablesAmount + 2)
  
  slackVariablesAmount = objectiveFunction.count(0)
  variablesAmount = len(objectiveFunction) - slackVariablesAmount
  for column in range(len(objectiveFunction)):
    if objectiveFunction[column] == 0:
      for line in range(len(constraintMatrix)):
        if constraintMatrix[line][column] == -1: slackVariablesAmount-=1

  nextSlackVariableToInsertInBase = len(objectiveFunction) - slackVariablesAmount
  nextArtificialVariableToInsertInBase = 1
  nextArtificialVariableId = 1

  lineWithArtificialVariables = getLinesWithArtificialVariables(constraintMatrix, variablesAmount)
  print(lineWithArtificialVariables)
  nextArtificialColumn = len(objectiveFunction) + 1

  for line in range(len(tableau)):
    for column in range(len(tableau[line])):
      if line == 0 and column == 0: tableau[line][column] = "Base"
      elif line == 0 and column > 0 and column < len(tableau[line]) - artificialVariablesAmount - 1: tableau[line][column] = "x" + str(column)
      elif line == 0 and column >= len(tableau[line]) - artificialVariablesAmount - 1 and column < len(tableau[line]) - 1:
        tableau[line][column] = "a" + str(nextArtificialVariableId)
        nextArtificialVariableId += 1
      elif line == 0 and column == len(tableau[line]) - 1: tableau[line][column] = "b"
      elif column == 0 and line < sizeOfConstraints+1 and line > 0 and nextSlackVariableToInsertInBase <= len(objectiveFunction):
        if line - 1 in lineWithArtificialVariables:
          tableau[line][column] = "a" + str(nextArtificialVariableToInsertInBase)
          nextArtificialVariableToInsertInBase += 1
          print(tableau[line][column])
        else:
          tableau[line][column] = "x" + str(nextSlackVariableToInsertInBase)
          nextSlackVariableToInsertInBase += 1
      elif column <= len(objectiveFunction) and column != 0 and line > 0 and line != len(tableau) - 1:
        tableau[line][column] = constraintMatrix[line - 1][column - 1]
      elif column >= len(tableau[line]) - artificialVariablesAmount - 1 and line > 0 and line < len(tableau) - 1 and column < len(tableau[line]) - 1:
        if line - 1 in lineWithArtificialVariables and column == nextArtificialColumn:
          tableau[line][nextArtificialColumn] = 1
          lineWithArtificialVariables.remove(line - 1)
          nextArtificialColumn += 1
        else:
          tableau[line][column] = 0
      elif line == len(tableau) - 1:
        tableau[line][column] = 1 if column > len(objectiveFunction) and column < len(tableau[line]) - 1 else 0
      elif column == len(tableau[line]) - 1 and line < sizeOfConstraints+1:
        tableau[line][column] = bVector[line-1][0]
      
      if column == 0 and line == sizeOfConstraints+1: tableau[line][column] = 'W'
      if column == len(tableau[line]) - 1 and line == sizeOfConstraints+1: tableau[line][column] = 0

  for line in range(1, len(tableau)-1):
    for column in range(len(tableau[line])):
      if tableau[line][column] == 1:
        isBaseVariable = True
        for lineBaseColumn in range(1, len(tableau)-1):
          if tableau[lineBaseColumn][column] != 0 and lineBaseColumn != line: isBaseVariable = False
        if isBaseVariable: tableau[line][0] = tableau[0][column]
  showTableau(tableau)

  return tableau

def toCanonicForm(tableau, artificialVariablesAmount, hasArtificialVariables = False):
  constraints = getTableauConstraints(tableau)
  baseVariables = getBaseVariables(tableau, constraints, artificialVariablesAmount, hasArtificialVariables)

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

def getBaseVariables(tableau, constraints, artificialVariablesAmount, hasArtificialVariables):
  baseVariables = []
  if hasArtificialVariables:
    for i in range(len(constraints)):
      if i > 0:
        if tableau[i][0][0] == 'x':
          baseVariables.append(int(re.findall(r'[0-9]+', tableau[i][0])[0]))
        elif tableau[i][0][0] == 'a':
          baseVariables.append((len(constraints[0]) - artificialVariablesAmount - 1) + int(re.findall(r'[0-9]+', tableau[i][0])[0]))
  else:
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

def pivoting(tableau, inputVariable, outputVariable, artificialVariablesAmount, hasArtificialVariables):
  if hasArtificialVariables and tableau[outputVariable][0][0] == 'a':
    letter = 'a' if tableau[0][inputVariable][0] == 'a' else 'x'
    inputVariable = inputVariable if inputVariable < len(tableau[0]) - artificialVariablesAmount - 2 else abs(inputVariable - (len(tableau[0]) - artificialVariablesAmount - 2))
    tableau[outputVariable][0] = letter + str(inputVariable)
  else:
    tableau[outputVariable][0] = "x" + str(inputVariable)
    
  tableau = toCanonicForm(tableau, artificialVariablesAmount, hasArtificialVariables)
  
  return tableau

def checkUnboundedness(tableau, inputVariable):
  for line in range(1, len(tableau)-1):
    if tableau[line][inputVariable] > 0: return False

  return True

def checkEndless(tableau):
  nonBaseVariables = getNonBaseVariables(tableau)
  objectiveFunctionLine = len(tableau) - 1
  hasZero = False
  for variable in nonBaseVariables:
    if tableau[objectiveFunctionLine][variable] == 0: hasZero = True
  
  return hasZero

def getLinesWithArtificialVariables(constraintMatrix, variablesAmount):
  lineWithArtificialVariables = []
  showTableau(constraintMatrix)
  
  for line in range(len(constraintMatrix)):
    isLineWithEqualsConstraint = True
    for column in range(len(constraintMatrix[line])):
      if constraintMatrix[line][column] == -1:
        lineHasArtificialVariable = True
        for lineBaseColumn in range(len(constraintMatrix)):
          if constraintMatrix[lineBaseColumn][column] != 0 and lineBaseColumn != line: lineHasArtificialVariable = False
    
        if lineHasArtificialVariable: lineWithArtificialVariables.append(line)
      
      if column >= variablesAmount and constraintMatrix[line][column] != 0: isLineWithEqualsConstraint = False
    if isLineWithEqualsConstraint: lineWithArtificialVariables.append(line)

  return lineWithArtificialVariables

def turnTableauToPhase2(tableau, artificialVariablesAmount):
  updatedConstraints = []
  updatedBVector = []

  for line in range(1, len(tableau)-1):
    constraint = []
    for column in range(1, len(tableau[line])):
      if column < len(tableau[line]) - artificialVariablesAmount-1: constraint.append(tableau[line][column])
      if column == len(tableau[line])-1: updatedBVector.append([tableau[line][column]])
    updatedConstraints.append(constraint)

  baseVariables = getBaseVariables(tableau, getTableauConstraints(tableau), artificialVariablesAmount, True)

  return updatedConstraints, updatedBVector, baseVariables

def getBVector(tableau):
  bVector = []
  for line in range(1, len(tableau)-1):
    bVector.append([tableau[line][len(tableau[line])-1]])

  return bVector

def showTableau(tableau):
  for i in range(len(tableau)):
    for j in range(len(tableau[i])):
      print("%7.1f" %tableau[i][j], end=" ") if type(tableau[i][j]) is not str else print("%7s" %tableau[i][j], end=" ")
    print()
  print()
