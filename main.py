import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

exercise = sns.load_dataset("exercise")
running = exercise[exercise["kind"] == "running"]

one_minute = running[running["time"] == "1 min"][["id", "pulse"]]
one_minute = one_minute.rename(columns={"pulse": "pulse_1_min"})

thirty_minutes = running[running["time"] == "30 min"][["id", "pulse"]]
thirty_minutes = thirty_minutes.rename(columns={"pulse": "pulse_30_min"})

comparison = pd.merge(one_minute, thirty_minutes, on="id")
comparison["pulse_change"] = comparison["pulse_30_min"] - comparison["pulse_1_min"]
comparison = comparison.sort_values("pulse_change").reset_index(drop=True)

plot_data = comparison.melt(
    id_vars="id",
    value_vars=["pulse_1_min", "pulse_30_min"],
    var_name="time",
    value_name="pulse",
)
plot_data["time"] = plot_data["time"].map(
    {"pulse_1_min": "1 minute", "pulse_30_min": "30 minutes"}
)

ax = sns.barplot(data=plot_data, x="id", y="pulse", hue="time")
for bars in ax.containers:
    ax.bar_label(bars, fmt="%.0f", padding=2)

ax.set(title="Running Pulse: 1 vs 30 Minutes", xlabel="Participant", ylabel="Pulse")
plt.tight_layout()
plt.show()