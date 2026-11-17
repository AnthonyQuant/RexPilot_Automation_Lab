
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


def load_benchmark_data():

    file_path = Path(__file__).parent / "benchmark_test.csv"

    if not file_path.exists():
        raise FileNotFoundError("Benchmark CSV was not found.")

    df = pd.read_csv(file_path)

    required_columns = {
        "strategy",
        "final_score",
        "session_duration",
        "date"
    }

    if not required_columns.issubset(df.columns):
        raise ValueError("Benchmark CSV is missing required columns.")

    df["final_score"] = pd.to_numeric(
        df["final_score"], errors="coerce"
    )

    df["session_duration"] = pd.to_numeric(
        df["session_duration"], errors="coerce"
    )

    df["date"] = pd.to_datetime(
        df["date"], errors="coerce"
    )

    df = df.dropna(
        subset=["final_score", "session_duration"]
    ).copy()

    if df.empty:
        raise ValueError("No valid benchmark records found.")

    return df


def create_visualizations(df):

    output_directory = Path(__file__).parent / "visualizations"
    output_directory.mkdir(exist_ok=True)

    strategy_order = [
        "Conservative",
        "Balanced",
        "Aggressive"
    ]

    available_strategies = [
        name for name in strategy_order
        if name in df["strategy"].unique()
    ]

    summary = (
        df.groupby("strategy")
        .agg(
            average_score=("final_score", "mean"),
            highest_score=("final_score", "max")
        )
        .reindex(available_strategies)
    )

    # 1. Average score by strategy
    fig, ax = plt.subplots()

    ax.bar(
        summary.index,
        summary["average_score"]
    )

    ax.set_title("Average Score by Strategy (Synthetic Test Data)")
    ax.set_xlabel("Strategy")
    ax.set_ylabel("Average Score")

    fig.tight_layout()
    fig.savefig(output_directory / "average_score.png")
    plt.close(fig)

    # 2. Highest score by strategy
    fig, ax = plt.subplots()

    ax.bar(
        summary.index,
        summary["highest_score"]
    )

    ax.set_title("Highest Score by Strategy (Synthetic Test Data)")
    ax.set_xlabel("Strategy")
    ax.set_ylabel("Highest Score")

    fig.tight_layout()
    fig.savefig(output_directory / "highest_score.png")
    plt.close(fig)

    # Assign trial numbers within each strategy
    df = df.sort_values("date", kind="stable").copy()

    df["trial_number"] = (
        df.groupby("strategy")
        .cumcount() + 1
    )

    # 3. Score progression across trials
    fig, ax = plt.subplots()

    for strategy in available_strategies:

        group = df[df["strategy"] == strategy]

        ax.plot(
            group["trial_number"],
            group["final_score"],
            marker="o",
            label=strategy
        )

    ax.set_title("Score Progression Across Trials (Synthetic Data)")
    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Final Score")
    ax.legend()
    ax.grid(True)

    fig.tight_layout()
    fig.savefig(output_directory / "score_progression.png")
    plt.close(fig)

    # 4. Session duration across trials
    fig, ax = plt.subplots()

    for strategy in available_strategies:

        group = df[df["strategy"] == strategy]

        ax.plot(
            group["trial_number"],
            group["session_duration"],
            marker="o",
            label=strategy
        )

    ax.set_title("Session Duration Across Trials (Synthetic Data)")
    ax.set_xlabel("Trial Number")
    ax.set_ylabel("Duration (seconds)")
    ax.legend()
    ax.grid(True)

    fig.tight_layout()
    fig.savefig(output_directory / "session_duration.png")
    plt.close(fig)

    print("Visualisations generated successfully.")

    print("\nGenerated files:")

    for file in output_directory.iterdir():
        print(file.name)

    print("\nOutput directory:")
    print(output_directory)


def main():

    df = load_benchmark_data()

    create_visualizations(df)


if __name__ == "__main__":
    main()
