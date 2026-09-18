from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_DIR = Path("D:/ecommerce-user-behavior-project/real_data_project")
PROCESSED_DATA_DIR = PROJECT_DIR / "data" / "processed"
FIGURE_DIR = PROJECT_DIR / "docs" / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)


behavior_distribution = pd.read_csv(PROCESSED_DATA_DIR / "behavior_distribution.csv")
daily_metrics = pd.read_csv(PROCESSED_DATA_DIR / "daily_metrics.csv")
window_rates = pd.read_csv(PROCESSED_DATA_DIR / "delayed_purchase_window_rates.csv")
behavior_rates = pd.read_csv(PROCESSED_DATA_DIR / "delayed_purchase_behavior_rates.csv")
delay_distribution = pd.read_csv(PROCESSED_DATA_DIR / "purchase_delay_distribution.csv")

def plot_behavior_distribution():
    plt.figure(figsize=(8, 5))

    plt.bar(
        behavior_distribution["behavior_type"],
        behavior_distribution["behavior_count"],
        color=["#4C78A8", "#F58518", "#54A24B", "#E45756"],
    )

    plt.title("Behavior Type Distribution")
    plt.xlabel("Behavior Type")
    plt.ylabel("Behavior Count")

    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "behavior_distribution.png", dpi=200)
    plt.close()


plot_behavior_distribution()


def plot_daily_user_trend():
    daily_metrics["date"] = pd.to_datetime(daily_metrics["date"])

    plt.figure(figsize=(10, 5))

    plt.plot(
        daily_metrics["date"],
        daily_metrics["dau"],
        marker="o",
        label="DAU",
    )

    plt.plot(
        daily_metrics["date"],
        daily_metrics["buy_users"],
        marker="o",
        label="Buy Users",
    )

    plt.title("Daily Active Users and Buying Users")
    plt.xlabel("Date")
    plt.ylabel("User Count")
    plt.legend()
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "daily_user_trend.png", dpi=200)
    plt.close()


plot_daily_user_trend()

def plot_purchase_rate_by_window():
    plt.figure(figsize=(8, 5))

    plt.bar(
        window_rates["window"],
        window_rates["buy_rate"] * 100,
        color="#59A14F",
    )

    plt.title("Purchase Rate by Future Window")
    plt.xlabel("Future Purchase Window")
    plt.ylabel("Purchase Rate (%)")

    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "purchase_rate_by_window.png", dpi=200)
    plt.close()


plot_purchase_rate_by_window()

def plot_purchase_rate_by_first_behavior():
    plt.figure(figsize=(8, 5))

    plt.bar(
        behavior_rates["first_behavior_type"],
        behavior_rates["buy_rate"] * 100,
        color=["#F58518", "#54A24B", "#4C78A8"],
    )

    plt.title("3-Day Purchase Rate by First Behavior")
    plt.xlabel("First Behavior Type")
    plt.ylabel("Purchase Rate (%)")

    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "purchase_rate_by_first_behavior.png", dpi=200)
    plt.close()


plot_purchase_rate_by_first_behavior()

def plot_purchase_delay_distribution():
    plt.figure(figsize=(8, 5))

    plt.bar(
        delay_distribution["delay_bucket"],
        delay_distribution["buy_count"],
        color="#E45756",
    )

    plt.title("Purchase Delay Distribution")
    plt.xlabel("Delay After First Interest")
    plt.ylabel("Purchase Count")

    plt.tight_layout()
    plt.savefig(FIGURE_DIR / "purchase_delay_distribution.png", dpi=200)
    plt.close()


plot_purchase_delay_distribution()
