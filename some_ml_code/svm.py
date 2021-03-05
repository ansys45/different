import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-white')
plt.rc('font', size=10)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)




from sklearn.datasets import make_moons
from sklearn.svm import LinearSVC
from sklearn.svm import SVC

X, y = make_moons(n_samples=100, random_state=35)

fig, axs = plt.subplots(1, 2, figsize=(11, 5))
fig.suptitle('Task 9.7.4')

clf = LinearSVC(C=1).fit(X, y)

axs[0].scatter(X[y==0, 0], X[y==0, 1], c='cornflowerblue')
axs[0].scatter(X[y==1, 0], X[y==1, 1], c='palevioletred')

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max),
                     np.arange(y_min, y_max))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

axs[0].contour(xx, yy, Z, colors='k', levels=[-0.1, 0, 0.5], linestyles=['--', '-', '--'])
axs[0].set(xlabel=r'$X_1$', ylabel=r'$X_2$');

clf = SVC(kernel='rbf', gamma=0.7, C=0.3)
clf.fit(X, y)

xlim = axs[0].get_xlim()
ylim = axs[0].get_ylim()
xx = np.linspace(xlim[0], xlim[1], 10)
yy = np.linspace(ylim[0], ylim[1], 10)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

axs[1].scatter(X[y==0, 0], X[y==0, 1], c='cornflowerblue')
axs[1].scatter(X[y==1, 0], X[y==1, 1], c='palevioletred')

axs[1].contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], linestyles=['--', '-', '--'])
axs[1].set(xlim=[-3, 3], ylim=[-3, 3], xlabel=r'$X_1$', ylabel=r'$X_2$');


# 1. It can be seen that the radial kernel performs much better than Linear one on data with non-linear boundaries
# 2. Radial kernel achievs good results on the Moons graphs, probably because Moons are half-elipses
# 3. There is an unexpected angle in the Linear SVC on Moons 



from sklearn.datasets import make_blobs

X, y = make_blobs(n_samples=75, centers=[[-3, -3], [0, 0], [3, 3]], cluster_std=0.8, random_state=50)
y = np.where(y==2, 0, y)

fig, axs = plt.subplots(1, 2, figsize=(11, 5))
fig.suptitle('Figure 9.8')

# Plot 1
axs[0].scatter(X[y==0, 0], X[y==0, 1], c='cornflowerblue')
axs[0].scatter(X[y==1, 0], X[y==1, 1], c='palevioletred')

axs[0].set(xlim=[-5, 5], ylim=[-5, 5], xlabel=r'$X_1$', ylabel=r'$X_2$')

# Plot 2
clf = LinearSVC(C=10)
clf.fit(X, y)

xlim = axs[0].get_xlim()
ylim = axs[0].get_ylim()
xx = np.linspace(xlim[0], xlim[1], 10)
yy = np.linspace(ylim[0], ylim[1], 10)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

axs[1].scatter(X[y==0, 0], X[y==0, 1], c='cornflowerblue')
axs[1].scatter(X[y==1, 0], X[y==1, 1], c='palevioletred')

axs[1].contour(XX, YY, Z, colors='k', levels=[-0.4, 0, 0.4], linestyles=['--', '-', '--'])
axs[1].set(xlim=[-5, 5], ylim=[-5, 5], xlabel=r'$X_1$', ylabel=r'$X_2$');


# 1. The hyperplane chages its angle as random-state of blobs changes
# 2. As C or the cluster standard error decreases the width of the counter interval also decreases.
# 3. The hyperplane in this case goes through the centers of the blobs



fig, axs = plt.subplots(1, 2, figsize=(11, 5))
fig.suptitle('Figure 9.9')

# Plot 1
clf = SVC(kernel='poly', degree=2, C=0.01, class_weight='balanced')
clf.fit(X, y)

x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

axs[0].scatter(X[y==0, 0], X[y==0, 1], c='cornflowerblue')
axs[0].scatter(X[y==1, 0], X[y==1, 1], c='palevioletred')

axs[0].contour(xx, yy, Z, colors='k', levels=[-1, -0.5, -0.1, 0.1, 0.5, 1], linestyles=['--', '-', '--', '--', '-', '--'])
axs[0].set(xlim=[-5, 5], ylim=[-5, 5], xlabel=r'$X_1$', ylabel=r'$X_2$');

# Plot 2
clf = SVC(kernel='rbf', gamma=0.7, C=0.3)
clf.fit(X, y)

xlim = axs[0].get_xlim()
ylim = axs[0].get_ylim()
xx = np.linspace(xlim[0], xlim[1], 10)
yy = np.linspace(ylim[0], ylim[1], 10)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

axs[1].scatter(X[y==0, 0], X[y==0, 1], c='cornflowerblue')
axs[1].scatter(X[y==1, 0], X[y==1, 1], c='palevioletred')

axs[1].contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], linestyles=['--', '-', '--'])
axs[1].set(xlim=[-5, 5], ylim=[-5, 5], xlabel=r'$X_1$', ylabel=r'$X_2$');


# 1. The margin is tiny on the second graph which is probably because of a long distance between the centers of blobs
# 2. Margins are very wide with polinomial kernel
# 3. Both, polynomial and radial kernels outperform linear on this data
