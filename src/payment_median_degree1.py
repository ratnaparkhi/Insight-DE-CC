#!/c/Python34/python
# Date: July 15, 2016
# Author: Prashant Ratnaparkhi
# Summary: This file contains the source code for the solution for
# Insight DE coding challenge. The rolling median of payments
# transactions within a 60 seconds moving windos is calculate and
# stored in a file.
# This implementation contains the implementation of Participant, PaymentGraph
# and Trnsaction classes. These are used to model the Venmo payments graph. 
# Hence it does not depend upon networkx package.
# Usage: payment_median_degree1.py -i <inputFile> -o <outputFile>
# For more information regarding the solution, please refer to the URL below
# https://github.com/ratnaparkhi/Insight-DE-CC.git
# For more information regarding the challegnge,
# please refer to the URL below
# https://github.com/InsightDataScience/coding-challenge
#
import sys
import getopt
import json
import statistics
import time
from calendar import timegm

class Participant:
   'Represents a node in PaymentGraph, it could be a Payor (From) of Payee(To)'
   def __init__(self, node):
      self._name = node
      self._nbrs = list() # Maintain Payee (to) list or payor (fm) list

   def add_nbr(self, node):
      self._nbrs.append(node)

   def is_nbr(self, node):
      nbrExists = False
      for nbr in self._nbrs:
         if node == nbr:
            nbrExists = True
            break
      return nbrExists
 
   def remove_nbr(self, node):
      nbrIndex = self._nbrs.index(node)
      del self._nbrs[nbrIndex]

   def get_nbrs(self):
      return self._nbrs

   def get_name(self):
      return self._name

   def get_degree(self):
      return len(self._nbrs)
   
class Transaction:
   'Represents an edge i.e. one payment activity <from-to> and creation time.'
   def __init__(self, fm, to, crTime):
      self._payor = fm
      self._payee = to
      self._ts = crTime

   def get_payor(self):
      return self._payor

   def get_payee(self):
      return self._payee

   def get_ts(self):
      return self._ts

   def set_ts(self, crTime):
      self._ts = crTime

class PaymentGraph:
   'Graph representation of Venmo payment transactions'
   
   def __init__ (self):
      self._participants = list() 
      self._payments = list() 
      #self._numParticipants = 0
      #self._numPayments = 0 # Transactions or edges

   def clear(self):
      self._participants = list() 
      self._payments = list() 
      #self._numParticipants = 0
      #self._numPayments = 0 # Transactions or edges.

   def add_participant(self, node,):
      if self.get_participant(node) == None:
         #self._numParticipants = self._numParticipants + 1
         newParticipant = Participant(node)
         self._participants.append(newParticipant)
      return newParticipant

   def get_participant(self, node):
      pExists = False
      for p in self._participants:
         if node == p.get_name():
            pExists = True
            break
      if pExists == True:
         return p
      else:
         return None

   def get_participant_index(self, node):
      if self.get_participant(node) == None:
         return None
      else:
         return self._participants.index(self.get_participant(node))

   def get_transaction_index(self, fm, to):
      if self.get_edge(fm, to) == None:
         return None
      else:
         return self._payments.index(self.get_edge(fm, to))

   def get_edge(self, fm, to):
      eExists = False
      for e in self._payments:
         if fm == e.get_payor() and to == e.get_payee():
            eExists = True
            break
      if eExists == True:
         return e
      else:
         return None

   def add_edge(self, fm, to, crTime):
      payor = self.get_participant(fm) 
      if payor == None:
         payor = self.add_participant(fm)
      payee = self.get_participant(to)
      if payee == None:
         payee = self.add_participant(to)

      # Transaction timestamp is maintained from Payor to Payee only.
      # We don't add duplicate transaction from same Payor-Payee combination
      # If the a payment from payor to payee exists, update only the ts. 
      txnIndex = self.get_transaction_index(fm, to) 
      if txnIndex == None: 
         newTransaction = Transaction(fm, to, crTime)
         self._payments.append(newTransaction)
	 # append the new neighbor in payor nbr lists. 
         payor.add_nbr(to)
      else:
         self._payments[txnIndex].set_ts(crTime)

      # Check if payor already exists as a nbr in payee nbr list
      # This is could be due to other already existing reverse payment.
      # Add payor (fm) as nbr of payee (to), if it is not a already a neighbor
      if payee.is_nbr(fm) == False:
         payee.add_nbr(fm)

   def get_participants(self):
      return self._participants

   def nodes(self):
      #create a list of participant names and return it
      pNameList = list()
      for p in self._participants:
         pNameList.append(p.get_name())
      return pNameList
   
   def degree(self, participant):
      deg = 0
      p = self.get_participant(participant)
      if p != None:
         deg = p.get_degree()        
      return deg

   # Return a list of edge tuples (fm, to, timestamp)
   def edges(self, data):
      edgeList = list()
      for txn in self._payments:
         edge = (txn.get_payor(), txn.get_payee(), txn.get_ts())
         edgeList.append(edge)
      return edgeList

   def remove_edge(self, fm, to):
      # Only removes the transaction. Node is not removed even if 0 neighbors.
      # Get index from the list of payments and use it to delete.
      txnIndex = self.get_transaction_index(fm, to) 
      del self._payments[txnIndex]
      # Remove payee (to) from the nbr list of payor (fm) 
      payor = self.get_participant(fm)
      payor.remove_nbr(to)
      # Also remove payor (fm) from nbr list of payeee (to), if it is a nbr
      payee = self.get_participant(to)
      if payee != None:
         if payee.is_nbr(fm) == True:
            payee.remove_nbr(fm)
      
   def remove_node(self, n1):
      # Only removes if there are no neighbors i.e no connections. 
      p = self.get_participant(n1)
      if p != None:
         if p.get_degree() == 0:
            pIndex = self.get_participant_index(n1)
            del self._participants[pIndex]

def main(argv):
   inFile = ''
   outFile = ''
   try:
      opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
   except getopt.GetoptError:
      print ("Usage: payment_median_degree1.py -i <inputFile> -o <outputFile>") 
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ("Usage: payment_median_degree1.py -i <inputFile> -o <outputFile>") 
         sys.exit()
      elif opt in ("-i", "--ifile") :
         inFile = arg
      elif opt in ("-o", "--ofile") :
         outFile = arg

   if inFile == '':
      print ("Usage: payment_median_degree1.py -i <inputFile> -o <outputFile>") 
      sys.exit()
   if outFile == '':
      print ("Usage: payment_median_degree1.py -i <inputFile> -o <outputFile>") 
      sys.exit()

   txnGraph = PaymentGraph()
   maxTimestamp = 0 ## Maximum processed timestamp
   existingMedian = "0.0" ## set & use if timestamp older than 60 seconds.
   staleTxn = False
   timeWindow = 60 ## Sixty seconds processing window

   medianOutput = open(outFile, 'w') 
   with open(inFile, 'r') as payment_txns:
      for payment in payment_txns:
         payment_data = json.loads(payment)
         #Get the nodes and create edge in the graph
         ## Assumed that format of all fields is correct. 
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
            txnGraph.add_edge(payment_actor, payment_target, txnEpochTime)	
         if timeDiff > 0 and timeDiff <= 60: # (T1) within 60 seconds
            maxTimestamp = txnEpochTime # Advance timestamp
            # Iterate & remove edges which have fallen out of the sixty seconds
	    # window. Also remove nodes without any connections
            for n1, n2, ts in txnGraph.edges(data=True):
               if ts < txnEpochTime - timeWindow:
                  txnGraph.remove_edge(n1, n2)
               if txnGraph.degree(n1) == 0:
                  txnGraph.remove_node(n1)
               if txnGraph.degree(n2) == 0:
                  txnGraph.remove_node(n2)
            txnGraph.add_edge(payment_actor, payment_target, txnEpochTime)
  
         if timeDiff >= -60 and timeDiff <= 0: #(T0,T3)Between 0 & -60 seconds. 
            # No need to change maxTimestamp &  to adjust graph. Add the edge.
            txnGraph.add_edge(payment_actor, payment_target, txnEpochTime)	
              
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
