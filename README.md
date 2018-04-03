# Decision-Tree
This simple Decision Tree Algorithm can learn from NUMERICAL inputs to make a tree and save it in a HTML file. 
Then it can make decisions for unseen-data based on the constructed tree.

To run the codes you can follow these steps:

Three data set are provided with the question as follow with the following names:
Human Activity Recognition: X_train.txt, y_train.txt, X_test.txt, y_test.txt
Iris: X_iris.txt y_iris.txt
Banknote: X_banknote.txt, y_banknote.txt

To run the training program you should provide some arguments after these keys:
-m    : should be followed by model name as "gini" or "information gain" 
	: for running test model this key can be followed by "test" or "train" to give the accuracy 	   	   for each of them
-itr1  : should be followed by name of a file containing attribute values
-itr2   : should be followed by name of a file containing class values
optional
-its1  : should be followed by name of a file containing attribute values
-its2   : should be followed by name of a file containing class values


sample running orders:

python tree_training_model.py -itr1 X_iris.txt -itr2 y_iris.txt -m "gini"

python tree_testing_model.py -itr1 X_iris.txt -itr2 y_iris.txt -m test


python tree_training_model.py -itr1 X_train.txt -itr2 y_train.txt -its1 X_test.txt -its2 y_test.txt -m "information gain"

python tree_testing_model.py -itr1 X_train.txt -itr2 y_train.txt -its1 X_test.txt -its2 y_test.txt -m train


