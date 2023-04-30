# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 14:10:56 2023

@author: Ajay
"""

import numpy as np
import matplotlib.pyplot as plt

# reading data from the datafile, located at same dir as the .Py code
# and storing it in an array
url = 'https://raw.githubusercontent.com/AjayRahulRaja/Fundamentals_of_Data_Science/main/coding_project/data1.csv'
arr = np.genfromtxt(url, delimiter = ',')
type(arr)

# creating another array, representing the distribution of newborn weights in a given dataset
counts, bins = np.histogram(arr, bins = 40, range = [2.0, 5.0])
print("The counts are", counts.size)
print("Bin range are", bins.size)

# arr.max() = 4.63233
# arr.min() = 2.23214

#calculating bincenter and binwidth from the histogram distribution
bincenter = 0.5 * (bins[1:] + bins[:-1])
binwidth = bins[1:] - bins[:-1]

#normalising the counts before plotting the histogram
counts_norm = counts / np.sum(counts)
print("bincenter is ", bincenter.size)
print("Normalised count is ",counts_norm.size)

# calculating the average weight of newborn babies in the given region
W = np.mean(bincenter)

# using the distribution to calculate another value, X
# The value of X is such that 33% of newborns from the distribution are born with a weight above X
X = np.percentile(bincenter, 100 - 33)
print("Mean value is: ", W)
print("X value is: ", X)

cum_sum = np.cumsum(counts_norm)
print("The cummulative sum is :", cum_sum)

x_bar = counts_norm * (bincenter <= X)

plt.figure(figsize = (6, 4))
# plotting the array as a histogram
plt.style.use("ggplot")
plt.gca().set_facecolor('lightgrey')

plt.bar(bincenter, counts_norm, width = 0.88 * binwidth, color = "blue", label = "New born babies distribution")

#mean value
plt.plot([W, W], [0, np.max(counts_norm) + 0.002], 'k--')
plt.text(3.5, 0.081, "Mean value is 3.5", c = "black", fontsize = 10)

#X value
plt.bar(bincenter, x_bar, width = 0.88 * binwidth, alpha = 0.5, color = "white", label = "33% of newborns are born with a weight above X")
plt.plot([X, X], [0, 0.032], 'k--')
plt.text(4.0, 0.032, "X value is 3.9973", c = "black", fontsize = 10)

plt.title("Distribution of new born babies in certain regions of Europe", fontsize = 10)
plt.xlabel("Weights of newborn babies (Distribution)", fontsize = 10)
plt.ylabel("Normalised Counts", fontsize = 10)
plt.xlim(2.0, 5.0, 0.5)
plt.ylim(0.00, 0.09, 0.01)

leg = plt.legend(bbox_to_anchor = (1.01, 0.99), fontsize = 10)
leg.get_frame().set_facecolor('lightgrey')
# plt.savefig('C:/Users/Lenovo/Desktop/UK/Hertfordshire/SEM 01/Fundamentals of Data Science/coding project/plot.png', dpi = 300, bbox_inches = 'tight')
plt.show()
