"""Draws figure 1 (I(t) for the coherent and incoherent completions). Requires numpy, matplotlib."""
import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
t = np.linspace(1e-6, 1 - 1e-9, 2000); r = np.sqrt(t*t - t + 1); a = (r - t)/4; b = (r + t)/4
I = t/2*np.log(2*t) + a*np.log(a) - b*np.log(b)
fig, ax = plt.subplots(figsize=(6.4, 3.6))
ax.axhline(0, color="0.6", lw=0.8)
ax.plot(t, I, color="#1f4e79", lw=2, label=r"coherent completion $\mathcal{E}_t$")
ax.plot(t, t*np.log(2), color="#b35900", lw=1.6, ls="--", label=r"incoherent completion / restriction: $t\log 2$")
tau = 0.296535165408627; ts = 0.112197392433428
ax.axvspan(0, tau, color="#1f4e79", alpha=0.08)
ax.plot([5/21], [np.log(2573571875/8707129344)/42], "o", color="k", ms=4)
ax.annotate(r"$t=5/21$ (exact certificate)", (5/21, -0.029), xytext=(0.33, -0.09), fontsize=8, arrowprops=dict(arrowstyle="-", lw=0.6))
ax.plot([ts], [-0.0590859989], "v", color="#1f4e79", ms=5)
ax.annotate(r"$t_*$", (ts, -0.059), xytext=(ts-0.01, -0.12), fontsize=9)
ax.annotate(r"$\tau$", (tau, 0), xytext=(tau+0.01, 0.05), fontsize=9)
ax.set_xlim(0, 1); ax.set_ylim(-0.16, 0.72)
ax.set_xlabel(r"channel parameter $t$"); ax.set_ylabel(r"mutual information in time (nats)")
ax.legend(fontsize=8, loc="upper left", frameon=False)
fig.tight_layout(); fig.savefig("../qutrit_information.pdf"); fig.savefig("../qutrit_information.png", dpi=200)
