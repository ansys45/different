import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

import statsmodels.api as sm

plt.style.use('seaborn-white')
plt.rc('font', size=10)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)

df = pd.read_csv('http://web.stanford.edu/~oleg2/hse/wage/wage.csv')
df.head()


fig, axs = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle('Figure 7.2')

df = df.sort_values('age')
x, y = df['age'], df['wage']
X = np.array([np.power(x, i) for i in range(5)]).T

# plot 1
x = np.array(x)
C0 = np.where((x > 0) & (x < 33.75), 1, 0).reshape(-1, 1)
C1 = np.where((x > 33.75) & (x < 64.5), 1, 0).reshape(-1, 1)
C2 = np.where(x > 64.5, 1, 0).reshape(-1, 1)
C = np.concatenate((C0, C1, C2),axis=1)
C = sm.add_constant(C)

mod = sm.OLS(y, C).fit()
y_step = mod.predict(C)
ci = mod.get_prediction(C).summary_frame()[['mean_ci_lower', 'mean_ci_upper']]

axs[0].set(xlabel='Age', ylabel='Wage')
axs[0].scatter(x, y, facecolors='none', edgecolors='silver', s=8)
axs[0].plot(x, y_step, c='g', linewidth=2)
axs[0].plot(x, ci['mean_ci_lower'], c='g', linewidth=1.5, linestyle='dashed')
axs[0].plot(x, ci['mean_ci_upper'], c='g', linewidth=1.5, linestyle='dashed')

# plot 2 
C0 = np.where((x > 0) & (x < 33.5), 1, 0).reshape(-1, 1)
C1 = np.where((x > 33.5) & (x < 49), 1, 0).reshape(-1, 1)
C2 = np.where((x > 49) & (x < 64.5), 1, 0).reshape(-1, 1)
C2 = np.where(x > 64.5, 1, 0).reshape(-1, 1)
C = np.concatenate((C0, C1, C2),axis=1)
C = sm.add_constant(C)

y = np.where(df['wage'] > 250, 1, 0)
mod2 = sm.GLM(y, C, family=sm.families.Binomial(sm.families.links.logit)).fit()
y_step2 = mod2.predict(C)
ci = mod2.get_prediction(C).summary_frame()[['mean_ci_lower', 'mean_ci_upper']]

axs[1].set(xlabel='Age', ylabel=r'$Pr(Wage > 250 | Age)$')
axs[1].scatter(x, y * 0.2, marker='|', color='silver')
axs[1].plot(x, y_step2, c='g', linewidth=2)
axs[1].plot(x, ci['mean_ci_lower'], c='g', linewidth=1.5, linestyle='dashed')
axs[1].plot(x, ci['mean_ci_upper'], c='g', linewidth=1.5, linestyle='dashed');


from scipy.interpolate import CubicSpline
from sklearn.preprocessing import PolynomialFeatures as pf
import seaborn as sns

df = df.sort_values('age')
x, y = df['age'], df['wage']

pers = [np.percentile(x, i) for i in [25, 50, 75]]

fig, axs = plt.subplots(1, 2, figsize=(10, 5))
fig.suptitle('Figure 7.5')

# plot 1
axs[0].set(xlabel='Age', ylabel='Wage', ylim=[0, 320])
axs[0].scatter(x, y, facecolors='none', edgecolors='silver', s=8)
sns.regplot(df['age'], df['wage'], order=4, truncate=True, scatter=False, color='red', ax=axs[0])
axs[0].stem(pers, [350]*3, markerfmt=' ', basefmt=' ', linefmt='k--')

# plot 2
y = np.where(df['wage'] > 250, 1, 0)
pff = pf(4).fit_transform
xt = pff(df['age'][:,None])
mod = sm.GLM(y, xt, family=sm.families.Binomial(sm.families.links.logit)).fit()
y_pred = mod.predict(xt)
ci = mod.get_prediction(xt).summary_frame()[['mean_ci_lower', 'mean_ci_upper']]

axs[1].set(xlabel='Age', ylabel=r'$Pr(Wage > 250 | Age)$', ylim=[-0.01, 0.21])
axs[1].scatter(x, y * 0.2, marker='|', color='silver')
axs[1].stem(pers, [0.5]*3, markerfmt=' ', basefmt=' ', linefmt='k--')
axs[1].plot(x, y_pred, c='r', linewidth=2)
axs[1].plot(x, ci['mean_ci_lower'], c='r', linewidth=1.5, linestyle='dashed')
axs[1].plot(x, ci['mean_ci_upper'], c='r', linewidth=1.5, linestyle='dashed');



from rpy2 import robjects

fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle('Figure 7.7')

ax.scatter(df['age'], df['wage'], facecolors='none', edgecolors='silver', s=8)
sns.regplot(df['age'], df['wage'], order=15, scatter=False, ax=ax, label='Polynomial')
rx = robjects.FloatVector(df['age'])
ry = robjects.FloatVector(df['wage'])
spline = robjects.r['smooth.spline'](x=rx, y=ry, df=15)
plt.plot(np.arange(18, 80).reshape(-1, 1)[:-1], spline[1], color='red', label='Natural Cubic Spline')

ax.set(xlim=[18, 81], ylim=[0, 320], xlabel='Age', ylabel='Wage')
plt.legend();


fig, ax = plt.subplots(figsize=(7,5))
fig.suptitle('Figure 7.8 / Smoothing spline')

ax.set(xlim=[18, 81], ylim=[0, 320], xlabel='Age', ylabel='Wage')
ax.scatter(df['age'], df['wage'], facecolors='none', edgecolors='silver', s=8)

x = np.arange(18, 80).reshape(-1, 1)[:-1]
spline = robjects.r['smooth.spline'](x=rx, y=ry, df=16)
plt.plot(x, spline[1], color='red', label='16 Degrees of Freedom')
spline = robjects.r['smooth.spline'](x=rx, y=ry, cv=True)
plt.plot(x, spline[1], c='b', label='6.8 Degrees of Freedom (LOOCV)')

plt.legend(loc='upper right');


from sklearn import svm
from sklearn.datasets import make_blobs


# we create 40 separable points
X, y = make_blobs(n_samples=40, centers=2, random_state=6)

# fit the model, don't regularize for illustration purposes
clf = svm.SVC(kernel='linear', C=1000)
clf.fit(X, y)

plt.scatter(X[:, 0], X[:, 1], c=y, s=30, cmap=plt.cm.Paired)

# plot the decision function
ax = plt.gca()
xlim = ax.get_xlim()
ylim = ax.get_ylim()

# create grid to evaluate model
xx = np.linspace(xlim[0], xlim[1], 30)
yy = np.linspace(ylim[0], ylim[1], 30)
YY, XX = np.meshgrid(yy, xx)
xy = np.vstack([XX.ravel(), YY.ravel()]).T
Z = clf.decision_function(xy).reshape(XX.shape)

# plot decision boundary and margins
ax.contour(XX, YY, Z, colors='k', levels=[-1, 0, 1], alpha=0.5,
           linestyles=['--', '-', '--'])
# # plot support vectors
# ax.scatter(clf.support_vectors_[:, 0], clf.support_vectors_[:, 1], s=100,
#            linewidth=1, facecolors='none', edgecolors='k')
plt.show()



