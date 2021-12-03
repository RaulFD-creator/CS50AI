#####################
###### README #######
#####################

First run: 
I have tried implementing the filters in the banknotes source code provided in 
the course. Using a convolutional layer, max-pooling layer, flatten unit and dropout
of 0.1, three hidden layers with NUM_CATEGORIES units and the final output layer
with sigmodial activation. Result is loss: 0.5583, accuracy: 0.8300. 

Second run:
To improve the result I amplify the number of units of the hidden layers, making the first comprised of 8 * NUM_CATEGORIES, 4 * NUM_CATEGORIES, and 2 * NUM_CATEGORIES. Result is loss: 0.2781, accuracy: 0.9212.

Third run: 
I introduce another hidden layer with 2* NUM_CATEGORIES units, after the ones already stablished which will have twice the units, result is loss: 0.1781, accuracy: 0.9547.

Fourth run:
The computing time increased to 20s for Epoch in the last run so I will introduce a dropout after the every hidden layer of 0.1. The computing didn't reduce all that much, 19s. Result is loss: 0.3390, accuracy: 0.9098. I will use the algorithm in the third run.