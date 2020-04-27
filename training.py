#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI


class ComputerAI(BaseAI):

	#variable that keeps track of the most optimal cell the ComputerAI can populate
	def _init_(self):
		self.makemove = (-1,-1)

	#Allocates new tile as either number 2 (probability 0.9) or 4 (probability 0.1)
	def getNewTileValue(self):
		if randint(0,99) < 100 * 0.9: 
			return 2 
		else: 
			return 4	

	#Input for heuristic: Gets the top four tiles and returns to eval function.
	def getMaxTiles(self, grid):
		maxTile = 0
		dist = 0
		maxTiles = [0, 0, 0, 0]
		for x in xrange(grid.size):
			for y in xrange(grid.size):
				dist = dist+(x-y)*grid.map[x][y]*3.0
				maxTile = grid.map[x][y]
				if maxTile > maxTiles[0]:
					maxTiles[0]=maxTile
					maxTiles.sort(cmp=None, key=None, reverse=False)
		maxTiles.append(dist)
		return maxTiles

	def getMinTiles(self, grid):
		minTile = 0
		minTiles = [0, 0, 0, 0]
		for x in xrange(grid.size):
			for y in xrange(grid.size):
				minTile = grid.map[x][y]
				if minTile < minTiles[0]:
					minTiles[0]=minTile
					minTiles.sort(cmp=None, key=None, reverse=True)
		return minTiles


	#Heuristic: Calculates the utility at leaf node based on - number of populated cells available, top 4 min/maxTiles values
	#and weighted distance of tiles from bottom left corner.
	def evalfn(self,grid):
		cell = grid.getAvailableCells()
		maxTiles = self.getMaxTiles(grid)
		minTiles = self.getMinTiles(grid)
		maxSum = sum(maxTiles)-maxTiles[4]
		minSum = sum(minTiles)	
		evalScore = (16-len(cell))*3000+1.5*(minSum-maxSum)-2*(maxTiles[4])
		return(evalScore)
		
		
	#Minimax algorithm implementation with alpha-beta pruning	
	def alphabeta(self, grid, depth, alpha, beta, maximizingPlayer):
		if depth == 0:
			return self.evalfn(grid)
		if maximizingPlayer:
			cells = grid.getAvailableCells()
			if cells == []:
				return -1
			for x in cells:
				newgrid = grid.clone()
				newgrid.map[x[0]][x[1]] = self.getNewTileValue()				
				result = self.alphabeta(grid, depth-1, alpha, beta, False)
				if result > alpha:
					self.makemove = x
				if result == -float('inf'):
					self.makemove = x
				if beta <= alpha:
					print "I'm in break stmt"
					break
			return alpha					
	
		else:
			moves = grid.getAvailableMoves()
			if moves:
				direction = moves[randint(0, len(moves) - 1)]
				grid.move(direction)
				result = self.alphabeta(grid, depth-1, alpha, beta, True)
				beta = min(beta, result)
			return beta	
	
	
	#Returns the optimal move per the algorithm to the GameManager function.
	def getMove(self, grid):
		cells = grid.getAvailableCells()
		print cells
		
		#return cells[randint(0, len(cells) - 1)] if cells else None
		
		result = self.alphabeta(grid, 5, -float('inf'), float('inf'), True)
		print "Expected Score:", result
		return self.makemove
		
