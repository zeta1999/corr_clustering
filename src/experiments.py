# ---------------------------------------------------------------------
# This is the script to run experiments for different models. 
# ---------------------------------------------------------------------
import os
import random
import networkx as nx
import numpy as np
import leader_model

seed = 222
random.seed(seed)
np.random.seed(seed)


# ---------------------------------------------------------------------
def run_leader_model_once():
# ---------------------------------------------------------------------
# Generate data, run pivot, run density_pivot and save output to file.
# This is a sample one-time run. Only once, for trial purposes.
	if not os.path.isdir('../data/'):
		os.makedirs('../data/')

	k = 5			# Number of cluster
	ni = 50      	# Number of nodes per cluster
	p = 0.2			# Intra-non-leader flipping probability
	epsilon = 0.0 	# Leader-neighbor flipping probability
	dataDir = '../data/data_leaderModel.txt'
	solutionDir = '../data/solution_leaderModel.txt'

	gf = leader_model.gen_data(k,ni,p,epsilon,dataDir)
	gf1 = gf.copy()
	gf2 = gf.copy()
	gf3 = gf.copy()
	leader_model.pivot_algorithm(gf1)
	leader_model.density_pivot_algorithm(gf2)
	leader_model.vote_algorithm(gf3,'vote')
	fid = open(solutionDir, 'w')
	fid.write('# Note:  GroundTruthClusterID ObtainedClusterIDs dont correspond, they just denote grouping of nodes.\n')
	fid.write('# Node GroundTruthClusterID ObtainedClusterID_pivot ObtainedClusterID_density ObtainedClusterID_vote')
	for v in gf.nodes_iter():
		fid.write('\n{} {} {} {} {}'.format(v,int(v/ni),gf1.node[v]['clusterId'],gf2.node[v]['clusterId'],gf3.node[v]['clusterId']))
	fid.close()

	return gf





# ---------------------------------------------------------------------
def grid_experiment_leader_model():
# ---------------------------------------------------------------------
# This function is to run the full code for different parameters and
# to save the files in an experiment directory
	if not os.path.isdir('../data/'):
		os.makedirs('../data/')
	if not os.path.isdir('../data/experiments/'):
		os.makedirs('../data/experiments/')

	k = 5													# Number of cluster
	niList = [50] 											# Number of nodes per cluster
	pList = [0.2] #[x/100.0 for x in range(5,50,5)]			# Intra-non-leader flipping probability
	epsilonList = [0.0] 									# Leader-neighbor flipping probability
	
	for n in niList:
		for p in pList:
			for epsilon in epsilonList:
				dataDir = '../data/experiments/data_leaderModel_k{}_ni{}_p{}_epsilon{}.txt'.format(k,ni,int(p*100),int(epsilon*100))
				solutionDir = '../data/experiments/solution_leaderModel_k{}_ni{}_p{}_epsilon{}.txt'.format(k,ni,int(p*100),int(epsilon*100))

				gf = leader_model.gen_data(k,ni,p,epsilon,dataDir)
				gf1 = gf.copy()
				gf2 = gf.copy()
				gf3 = gf.copy()
				leader_model.pivot_algorithm(gf1)
				leader_model.density_pivot_algorithm(gf2)
				leader_model.vote_algorithm(gf3,'best')
				fid = open(solutionDir, 'w')
				fid.write('# Note:  GroundTruthClusterID ObtainedClusterIDs dont correspond, they just denote grouping of nodes.\n')
				fid.write('# Node GroundTruthClusterID ObtainedClusterID_pivot ObtainedClusterID_density ObtainedClusterID_vote')
				for v in gf.nodes_iter():
					fid.write('\n{} {} {} {} {}'.format(v,int(v/ni),gf1.node[v]['clusterId'],gf2.node[v]['clusterId'],gf3.node[v]['clusterId']))
				fid.close()



# ---------------------------------------------------------------------
def read_mnist_data():
# ---------------------------------------------------------------------
# Read MNIST Data to apply greedy heuristic algorithms
	dataDir = '../data/data_mnist.txt'
	fid = open(dataDir, 'r')

	# Readout comments
	fid.readline() ; fid.readline() ; 

	# Read top line
	line = fid.readline()
	n = int(line.split()[0])

	# Read Graph from Adjacency Matrix
	g = nx.Graph();
	groundTruth = {}
	for line in fid:
		line = line.split()
		if len(line) < 2:
			continue

		node = int(line[1])
		groundTruth[node] = int(line[0])
		
		for i in range(2,len(line)):
			g.add_edge(node,int(line[i]))

	return (n,groundTruth,g)




# ---------------------------------------------------------------------
def run_mnist():
# ---------------------------------------------------------------------
# Read MNIST data and apply greedy algorithms	
	(nmnist, gtMnist, graphMnist) = read_mnist_data()
	gf1 = graphMnist.copy()
	gf2 = graphMnist.copy()
	gf3 = graphMnist.copy()
	leader_model.pivot_algorithm(gf1)
	leader_model.density_pivot_algorithm(gf2)
	leader_model.vote_algorithm(gf3,'vote')
	solutionDir = '../data/solution_mnist.txt'
	fid = open(solutionDir, 'w')
	fid.write('# Note:  GroundTruthClusterID ObtainedClusterIDs dont correspond, they just denote grouping of nodes.\n')
	fid.write('# Node GroundTruthClusterID ObtainedClusterID_pivot ObtainedClusterID_density ObtainedClusterID_vote')
	for v in graphMnist.nodes_iter():
		fid.write('\n{} {} {} {} {}'.format(v,gtMnist[v],gf1.node[v]['clusterId'],gf2.node[v]['clusterId'],gf3.node[v]['clusterId']))
	fid.close()

	return graphMnist


# ---------------------------------------------------------------------
# Running Experiments
# ---------------------------------------------------------------------
gf = run_leader_model_once()
# grid_experiment()
# graphMnist = run_mnist()




