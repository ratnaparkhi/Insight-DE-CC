#!/c/Python34/python
# Date: July 15, 2016
# Author: Prashant Ratnaparkhi
# Summary: This file contains the source code for the solution for
# Insight DE coding challenge. The rolling median of payments
# transactions within a 60 seconds moving windos is calculate and
# stored in a file.
# This implementation uses Graph class from networks package. 
# Usage: payment_median_degree.py -i <inputFile> -o <outputFile>
# For more information regarding the solution, please refer to the URL below
# https://github.com/ratnaparkhi/Insight-DE-CC.git
# For more information regarding the challegnge,
# please refer to the URL below
# https://github.com/InsightDataScience/coding-challenge
#
import sys
import getopt
import json
import networkx as graph
import statistics
import time
from calendar import timegm
#
def main(argv):
   inFile = ''
   outFile = ''
   try:
      opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
   except getopt.GetoptError:
      print ("Usage: payment_median_degree.py -i <inputFile> -o <outputFile>") 
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ("Usage: payment_median_degree.py -i <inputFile> -o <outputFile>") 
         sys.exit()
      elif opt in ("-i", "--ifile") :
         inFile = arg
      elif opt in ("-o", "--ofile") :
         outFile = arg

   if inFile == '':
      print ("Usage: payment_median_degree.py -i <inputFile> -o <outputFile>") 
      sys.exit()
   if outFile == '':
      print ("Usage: payment_median_degree.py -i <inputFile> -o <outputFile>") 
      sys.exit()

   txnGraph = graph.Graph()
   maxTimestamp = 0 ## Maximum processed timestamp
   existingMedian = "0.0" ## set & use if timestamp older than 60 seconds.
   staleTxn = False
   timeWindow = 60 ## Sixty seconds processing window

   medianOutput = open(outFile, 'w') 
   with open(inFile, 'r') as payment_txns:
      for payment in payment_txns:
         payment_data = json.loads(payment)
         #Get the nodes and create edge in the graph
         payment_actor = payment_data['actor']
         payment_target = payment_data['target']
         payment_timestamp = payment_data['created_time']
         # It is assumed that format of the fields is correct.
         # Check if actor and target are the same, which indicates
         # invalid transaction. In such case, write 'INVALID_TXN'
         # and continue to process the next payment.
         if payment_actor == payment_target:
            medianOutput.write(str('INVALID-TXN\n'))
            continue

         # convert payment_timestamp to epoch_time
         utcTimestamp = time.strptime(payment_timestamp, "%Y-%m-%dT%H:%M:%SZ")
         txnEpochTime = timegm(utcTimestamp)
         # Prune the graph to process payments in the 60 seconds window.
         timeDiff = txnEpochTime - maxTimestamp
         if timeDiff < -60: # Payment older than 60 seconds, ignore
            staleTxn = True # (T4) no need to do anything   
         if timeDiff > 60: # (T2) Remove all nodes/edges and then add
            txnGraph.clear()
            maxTimestamp = txnEpochTime # Advance timestamp
            # If node does not exist, add_edge creates it.
            txnGraph.add_edge(payment_actor, payment_target, timestamp=txnEpochTime)	
         if timeDiff > 0 and timeDiff <= 60: # (T1) within 60 seconds
            maxTimestamp = txnEpochTime # Advance timestamp
            # Iterate & remove edges which have fallen out of the sixty seconds
	    # window. Also remove nodes without any connections
            for n1, n2, ts in txnGraph.edges(data=True):
               if ts['timestamp'] < txnEpochTime - timeWindow:
                  txnGraph.remove_edge(n1, n2)
               if txnGraph.degree(n1) == 0:
                  txnGraph.remove_node(n1)
               if txnGraph.degree(n2) == 0:
                  txnGraph.remove_node(n2)
            txnGraph.add_edge(payment_actor, payment_target, timestamp=txnEpochTime)	
         if timeDiff >= -60 and timeDiff <= 0: #(T0,T3)Between 0 & -60 seconds. 
            # No need to change maxTimestamp &  to adjust graph. Add the edge.
            txnGraph.add_edge(payment_actor, payment_target, timestamp=txnEpochTime)	
         # If txn is not stale, iterate over list of nodes in the graph; get 
	 # degree of each node, and find the median of degrees for the graph. 
         if staleTxn == False: 
            degreeList = list() # create an empty list of degrees of nodes.
            for node in txnGraph.nodes():
               degreeList.append(txnGraph.degree(node))
            txnGraphMedian = "{:.2f}".format(statistics.median(degreeList))
            existingMedian = txnGraphMedian
         else: # It is a stale transaction completed before 60 seconds.
            txnGraphMedian = existingMedian 
            staleTxn = False # Reset 
         medianOutput.write(str(txnGraphMedian)+'\n')

if __name__ == "__main__":
   main(sys.argv[1:])
