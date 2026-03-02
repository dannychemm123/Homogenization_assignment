import numpy as np
import matplotlib.pyplot as plt

# Read data
data = np.loadtxt('convergence_data1.txt')
eps = data[:, 0]
errorL2 = data[:, 1]
errorH1 = data[:, 2]
errorH1corr = data[:, 3]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Log-log plot
ax1.loglog(eps, errorL2, 'o-', label='L2 error (no corrector)', linewidth=2, markersize=8)
ax1.loglog(eps, errorH1, 's-', label='H1 error (no corrector)', linewidth=2, markersize=8)
ax1.loglog(eps, errorH1corr, '^-', label='H1 error (with corrector)', linewidth=2, markersize=8)

# Add reference slopes
eps_ref = np.array([eps[0], eps[-1]])
ax1.loglog(eps_ref, 0.5*eps_ref, 'k--', alpha=0.5, linewidth=1.5, label=r'Slope 1')
ax1.loglog(eps_ref, 0.05*eps_ref**2, 'k:', alpha=0.5, linewidth=1.5, label=r'Slope 2')

ax1.set_xlabel(r'$\varepsilon = 1/N$', fontsize=14)
ax1.set_ylabel('Error', fontsize=14)
ax1.set_title('Convergence in Log-Log Scale', fontsize=16, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3)

# Plot 2: Semi-log plot
ax2.semilogy(1/eps, errorL2, 'o-', label='L2 error (no corrector)', linewidth=2, markersize=8)
ax2.semilogy(1/eps, errorH1, 's-', label='H1 error (no corrector)', linewidth=2, markersize=8)
ax2.semilogy(1/eps, errorH1corr, '^-', label='H1 error (with corrector)', linewidth=2, markersize=8)

ax2.set_xlabel('N (number of cells)', fontsize=14)
ax2.set_ylabel('Error (log scale)', fontsize=14)
ax2.set_title('Convergence vs Number of Cells', fontsize=16, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('convergence_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("Plot saved as convergence_plot.png")

# Create a separate plot for convergence rates
fig2, ax = plt.subplots(figsize=(10, 6))

rates_L2 = []
rates_H1 = []
rates_H1corr = []
N_vals = []

for i in range(1, len(eps)):
    rateL2 = np.log(errorL2[i]/errorL2[i-1]) / np.log(eps[i]/eps[i-1])
    rateH1 = np.log(errorH1[i]/errorH1[i-1]) / np.log(eps[i]/eps[i-1])
    rateH1corr = np.log(errorH1corr[i]/errorH1corr[i-1]) / np.log(eps[i]/eps[i-1])
    
    rates_L2.append(rateL2)
    rates_H1.append(rateH1)
    rates_H1corr.append(rateH1corr)
    N_vals.append((1/eps[i-1] + 1/eps[i])/2)  # midpoint

ax.plot(N_vals, rates_L2, 'o-', label='L2 convergence rate', linewidth=2, markersize=8)
ax.plot(N_vals, rates_H1, 's-', label='H1 convergence rate', linewidth=2, markersize=8)
ax.plot(N_vals, rates_H1corr, '^-', label='H1 corrector rate', linewidth=2, markersize=8)
ax.axhline(y=1, color='k', linestyle='--', alpha=0.5, label='Expected rate = 1')
ax.axhline(y=2, color='k', linestyle=':', alpha=0.5, label='Expected rate = 2')

ax.set_xlabel('N (number of cells)', fontsize=14)
ax.set_ylabel('Convergence Rate', fontsize=14)
ax.set_title('Convergence Rates', fontsize=16, fontweight='bold')
ax.legend(fontsize=11)
ax.grid(True, alpha=0.3)
ax.set_ylim([0, 3])

plt.tight_layout()
plt.savefig('convergence_rates.png', dpi=300, bbox_inches='tight')
plt.show()

print("Convergence rates plot saved as convergence_rates.png")

# Print numerical results
print("\n" + "="*60)
print("CONVERGENCE RATES")
print("="*60)
for i in range(1, len(eps)):
    rateL2 = np.log(errorL2[i]/errorL2[i-1]) / np.log(eps[i]/eps[i-1])
    rateH1 = np.log(errorH1[i]/errorH1[i-1]) / np.log(eps[i]/eps[i-1])
    rateH1corr = np.log(errorH1corr[i]/errorH1corr[i-1]) / np.log(eps[i]/eps[i-1])
    
    print(f"From N={int(1/eps[i-1])} to N={int(1/eps[i])}:")
    print(f"  L2 rate: {rateL2:.3f} (expected ~1.0)")
    print(f"  H1 rate: {rateH1:.3f} (expected ~1.0)")
    print(f"  H1 corrector rate: {rateH1corr:.3f} (expected ~2.0)")
    print()