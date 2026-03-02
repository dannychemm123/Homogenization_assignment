import numpy as np
import matplotlib.pyplot as plt

# Read data
data = np.loadtxt('convergence_data1.txt')
N_vals = data[:, 0]
eps = data[:, 1]
errorL2 = data[:, 2]
errorH1 = data[:, 3]
errorH1corr = data[:, 4]

# Create figure with three subplots
fig = plt.figure(figsize=(18, 5))

# =====================================================
# Plot 1: Log-log plot (epsilon vs error)
# =====================================================
ax1 = fig.add_subplot(131)

ax1.loglog(eps, errorL2, 'o-', label='L2 error (no corrector)', 
           linewidth=2, markersize=8, color='blue')
ax1.loglog(eps, errorH1, 's-', label='H1 error (no corrector)', 
           linewidth=2, markersize=8, color='orange')
ax1.loglog(eps, errorH1corr, '^-', label='H1 error (with corrector)', 
           linewidth=2, markersize=8, color='green')

# Add reference slopes
eps_ref = np.array([eps[0], eps[-1]])
const1 = errorH1[0] / eps[0]  # Adjust constant for O(eps)
const2 = errorH1corr[0] / eps[0]**2  # Adjust constant for O(eps^2)

ax1.loglog(eps_ref, const1*eps_ref, 'k--', alpha=0.5, linewidth=1.5, label='O(eps)')
ax1.loglog(eps_ref, const2*eps_ref**2, 'k:', alpha=0.5, linewidth=1.5, label='O(eps^2)')

ax1.set_xlabel('epsilon = 1/N', fontsize=14)
ax1.set_ylabel('Error', fontsize=14)
ax1.set_title('Convergence in Log-Log Scale', fontsize=16, fontweight='bold')
ax1.legend(fontsize=11)
ax1.grid(True, alpha=0.3, which='both')

# =====================================================
# Plot 2: Semi-log plot (N vs error)
# =====================================================
ax2 = fig.add_subplot(132)

ax2.semilogy(N_vals, errorL2, 'o-', label='L2 error (no corrector)', 
             linewidth=2, markersize=8, color='blue')
ax2.semilogy(N_vals, errorH1, 's-', label='H1 error (no corrector)', 
             linewidth=2, markersize=8, color='orange')
ax2.semilogy(N_vals, errorH1corr, '^-', label='H1 error (with corrector)', 
             linewidth=2, markersize=8, color='green')

ax2.set_xlabel('N (number of cells)', fontsize=14)
ax2.set_ylabel('Error (log scale)', fontsize=14)
ax2.set_title('Convergence vs Number of Cells', fontsize=16, fontweight='bold')
ax2.legend(fontsize=11)
ax2.grid(True, alpha=0.3)

# =====================================================
# Plot 3: Convergence rates
# =====================================================
ax3 = fig.add_subplot(133)

rates_L2 = []
rates_H1 = []
rates_H1corr = []
N_mid = []

for i in range(1, len(eps)):
    rateL2 = np.log(errorL2[i]/errorL2[i-1]) / np.log(eps[i]/eps[i-1])
    rateH1 = np.log(errorH1[i]/errorH1[i-1]) / np.log(eps[i]/eps[i-1])
    rateH1corr = np.log(errorH1corr[i]/errorH1corr[i-1]) / np.log(eps[i]/eps[i-1])
    
    rates_L2.append(rateL2)
    rates_H1.append(rateH1)
    rates_H1corr.append(rateH1corr)
    N_mid.append((N_vals[i-1] + N_vals[i])/2)

ax3.plot(N_mid, rates_L2, 'o-', label='L2 convergence rate', 
         linewidth=2, markersize=8, color='blue')
ax3.plot(N_mid, rates_H1, 's-', label='H1 convergence rate', 
         linewidth=2, markersize=8, color='orange')
ax3.plot(N_mid, rates_H1corr, '^-', label='H1 corrector rate', 
         linewidth=2, markersize=8, color='green')

ax3.axhline(y=1, color='k', linestyle='--', alpha=0.5, linewidth=1.5, label='Expected rate = 1')
ax3.axhline(y=2, color='k', linestyle=':', alpha=0.5, linewidth=1.5, label='Expected rate = 2')

ax3.set_xlabel('N (number of cells)', fontsize=14)
ax3.set_ylabel('Convergence Rate', fontsize=14)
ax3.set_title('Convergence Rates', fontsize=16, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_ylim([0, 3])

plt.tight_layout()
plt.savefig('convergence_plot.png', dpi=300, bbox_inches='tight')
plt.show()

print("Plot saved as convergence_plot.png")

# =====================================================
# Print numerical results table
# =====================================================
print("\n" + "="*80)
print("CONVERGENCE TABLE")
print("="*80)
print(f"{'N':>4} {'epsilon':>10} {'L2 error':>12} {'H1 error':>12} {'H1 corr':>12}")
print("-"*80)
for i in range(len(N_vals)):
    print(f"{int(N_vals[i]):>4} {eps[i]:>10.4f} {errorL2[i]:>12.6e} {errorH1[i]:>12.6e} {errorH1corr[i]:>12.6e}")

print("\n" + "="*80)
print("CONVERGENCE RATES")
print("="*80)
for i in range(len(N_mid)):
    print(f"From N={int(N_vals[i])} to N={int(N_vals[i+1])}:")
    print(f"  L2 rate:      {rates_L2[i]:6.3f} (expected ~1.0)")
    print(f"  H1 rate:      {rates_H1[i]:6.3f} (expected ~1.0)")
    print(f"  H1 corr rate: {rates_H1corr[i]:6.3f} (expected ~2.0)")
    print()