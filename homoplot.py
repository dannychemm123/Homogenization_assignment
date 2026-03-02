import numpy as np
import matplotlib.pyplot as plt

# Read data
data = np.loadtxt('convergence_data.txt')
eps = data[:, 0]
errorL2 = data[:, 1]
errorH1 = data[:, 2]
errorH1corr = data[:, 3]

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Log-log plot
ax1.loglog(eps, errorL2, 'o-', label=r'$||u_\varepsilon - u_0||_{L^2}$', linewidth=2, markersize=8)
ax1.loglog(eps, errorH1, 's-', label=r'$||u_\varepsilon - u_0||_{H^1}$', linewidth=2, markersize=8)
ax1.loglog(eps, errorH1corr, '^-', label=r'$||u_\varepsilon - u_{corr}||_{H^1}$', linewidth=2, markersize=8)

# Add reference slopes
eps_ref = np.array([eps[0], eps[-1]])
ax1.loglog(eps_ref, 0.5*eps_ref, 'k--', alpha=0.5, label=r'$O(\varepsilon)$')
ax1.loglog(eps_ref, 0.05*eps_ref**2, 'k:', alpha=0.5, label=r'$O(\varepsilon^2)$')

ax1.set_xlabel(r'$\varepsilon = 1/N$', fontsize=14)
ax1.set_ylabel('Error', fontsize=14)
ax1.set_title('Convergence in Log-Log Scale', fontsize=16)
ax1.legend(fontsize=12)
ax1.grid(True, alpha=0.3)

# Plot 2: Semi-log plot
ax2.semilogy(1/eps, errorL2, 'o-', label=r'$||u_\varepsilon - u_0||_{L^2}$', linewidth=2, markersize=8)
ax2.semilogy(1/eps, errorH1, 's-', label=r'$||u_\varepsilon - u_0||_{H^1}$', linewidth=2, markersize=8)
ax2.semilogy(1/eps, errorH1corr, '^-', label=r'$||u_\varepsilon - u_{corr}||_{H^1}$', linewidth=2, markersize=8)

ax2.set_xlabel(r'$N$ (number of cells)', fontsize=14)
ax2.set_ylabel('Error (log scale)', fontsize=14)
ax2.set_title('Convergence vs Number of Cells', fontsize=16)
ax2.legend(fontsize=12)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('convergence_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("Plot saved as convergence_plot.png")

# Compute and display convergence rates
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