import numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.optimize import minimize
import statsmodels.api as sm
import warnings
warnings.filterwarnings('ignore')

plt.style.use('seaborn-white')
plt.rc('font', size=10)
plt.rc('figure', titlesize=18)
plt.rc('axes', labelsize=15)
plt.rc('axes', titlesize=18)
np.random.seed(1)


n, k = 100, 50  # number of observations and neighbors
true_fn = lambda x: np.sin(x*np.pi*5/4)   # true underlying sinusoidla function
X = np.array(sorted(np.random.random(size=n)))   # predictor values
Y = true_fn(X) + np.random.random(n)-0.5     # noisy non-linearly related response values
x0 = 0.45     # test observations at which local regressions are computed

# Visualize (X,Y) observations and x0 test point
def Bell(X, x0, tau=.005):
    return np.exp(-(X - x0)**2 / 2 / tau)

df = pd.DataFrame(dict(X=X, Y=Y))

# Grey points
ax = df.plot.scatter('X','Y', title='Local regression', s=80, c='white',
                     figsize=(7,5), edgecolors='gray', ylim=[-1.2,1.7]);

# Blue line
ax.plot(X, true_fn(X), color='C0')

# Vertical line
ax.plot([x0,x0], [-1, true_fn(x0)], color='orange')

# Orange fit for all
lowess = sm.nonparametric.lowess
locreg = lowess(Y, X, frac = 0.5, it=3)[:, 1]
ax.plot(X, locreg, c='orange')

# The x0
y0 = locreg[49]
ax.scatter(x0, y0, c='darkorange', s=100, zorder=3)

d = np.abs(X - x0)
d = np.sort(np.argsort(d)[:50])
XN, YN = X[d], Y[d]

# Yellow bell
ax.fill(XN, Bell(XN, x0), c='khaki', zorder=1)

# Nearest points
ax.scatter(XN, YN, facecolors='none', edgecolor='darkorange', s=80, zorder=3)

# Regression line
mod = sm.WLS(YN, sm.add_constant(XN)).fit()
ax.plot(XN, mod.predict(sm.add_constant(XN)) + 0.04, color='darkorange', linewidth=2);


# # Problem 3


df = pd.read_csv('http://web.stanford.edu/~oleg2/hse/wage/wage.csv')
df.head()


X = np.array(df.age)
y = np.array(df.wage)


plt.figure(figsize=(8, 5))
plt.title('Local Linear Regression')
plt.xlabel('Age')
plt.ylabel('Wage')
plt.ylim((-5, 350))

# Grey points
plt.scatter(X, y, marker='o', facecolor='none', edgecolor='lightgrey', s=10)

# Red line
locreg = lowess(y, X, frac = 0.2, it=3)[:, 1]
plt.plot(sorted(X), locreg, c='red', label='Span is 0.2 (16.4 Degrees of Freedom)')

# Blue line
locreg = lowess(y, X, frac = 0.7, it=3)[:, 1]
plt.plot(sorted(X), locreg, c='blue', label='Span is 0.7 (5.3 Degrees of Freedom)')

plt.legend(loc='upper right');



# # Problem 4


df = df[['year', 'age', 'education', 'wage']]


from pygam import LinearGAM, LogisticGAM, s, f, l

eds = df['education'].unique()
for i, ed in enumerate(eds):
    df['education'] = np.where(df['education'] == ed, i, df['education'])
    
X = np.array(df[['year', 'age', 'education']])
y = np.array(df.wage)

fig, axs = plt.subplots(1, 3, figsize=(10, 5))
fig.tight_layout()

gam = LinearGAM(s(0) + s(1) + f(2)).gridsearch(X, y)

# Plot
titles = ['year', 'age', 'education']
for i, ax in enumerate(axs):
    ax.set(xlabel=titles[i], ylabel=f'$f_{i}({titles[i]})$')
    grid = gam.generate_X_grid(term=i)
    ax.plot(grid[:, i], gam.partial_dependence(term=i, X=grid), c='r')
    ax.plot(grid[:, i], gam.partial_dependence(term=i, X=grid, width=.95)[1], c='grey', ls='dotted')
    if i == 0:
        ax.set_ylim(-30,30)
        
    if i == 1:
        #ax.scatter(X[:, i].ravel(), y)
        pass
    
    if i == 2:
        ax.set_title('<HS Coll <Coll HS >Coll');


fig, axs = plt.subplots(1, 3, figsize=(10, 5))

y = np.where(y>250, 1, 0)
gam = LogisticGAM(l(0) + s(1) + f(2)).gridsearch(X, y)

for i, ax in enumerate(axs):
    XX = gam.generate_X_grid(term=i)
    pdep, confi = gam.partial_dependence(term=i, width=.95)

    ax.plot(XX[:, i], pdep)
    ax.plot(XX[:, i], confi, c='r', ls='--')
    ax.set_title(titles[i])
    
#     if i == 0:
#         ax.set(ylim=[-4.1, 4.1], xlim=[2003, 2009])