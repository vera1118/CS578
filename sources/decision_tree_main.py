from data_clean import *
from decision_tree import *


def main():
	X_train, X_test, y_train, y_test = prank_data_split('../dataset/ratings.csv', 0.2)

	#cross validation#
	depth_array = np.array([1,2,3,4,5,6,7,8,9,10,11])
	depth = kfoldcv(X_train.as_matrix(), y_train.as_matrix(), 5, depth_array, '../dataset/movies.csv')

	#prediction#
	print('predict using decision tree with max depth', depth, ':')
	X_train, X_test, y_train, y_test = generate_matrix(X_train, X_test, y_train, y_test, '../dataset/movies.csv')
	regr = decision_tree(X_train, y_train, depth)
	y_predicted = predict(regr, X_test)

	rmse = get_RMSE(y_test, y_predicted)
	print('rmse:',rmse)
	mae = get_MAE(y_test, y_predicted)
	print('mae:', mae)

	#specificity, sensitivity, precision, accuracy
	spec, sens, prec, accu = get_spec_sens_prec_accu(y_test, y_predicted)
	print('spec:', spec)
	print('sens:', sens)
	print('prec:', prec)
	print('accu:', accu)

main()
