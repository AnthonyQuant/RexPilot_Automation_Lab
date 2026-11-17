import pandas as pd
from pathlib import Path


def load_benchmark_data():

    file_path = Path(__file__).parent / "benchmark_test.csv"

    if not file_path.exists():
        raise FileNotFoundError("Benchmark CSV was not found.")

    df = pd.read_csv(file_path)

    required_columns = {"strategy", "final_score", "date"}

    if not required_columns.issubset(df.columns):
        raise ValueError("Benchmark CSV is missing required columns.")

    df["final_score"] = pd.to_numeric(
        df["final_score"],
        errors="coerce"
    )

    # Exclude records without a valid final score
    df = df.dropna(subset=["final_score"]).copy()

    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce"
    )

    if df.empty:
        raise ValueError("No valid benchmark scores were found.")

    return df


def analyse_strategies(df):

    results = []

    for strategy_name, group in df.groupby("strategy"):

        group = group.sort_values("date")

        scores = group["final_score"]

        first_score = scores.iloc[0]
        last_score = scores.iloc[-1]

        if first_score > 0:
            improvement = (
                (last_score - first_score) / first_score
            ) * 100
        else:
            improvement = None

        results.append({
            "Strategy": strategy_name,
            "Trials": len(scores),
            "Average Score": round(scores.mean(), 2),
            "Highest Score": scores.max(),
            "Median Score": round(scores.median(), 2),
            "Improvement (%)": (
                round(improvement, 2)
                if improvement is not None
                else "N/A"
            )
        })

    return pd.DataFrame(results)


def main():

    df = load_benchmark_data()

    results = analyse_strategies(df)

    print("\nREXPILOT STRATEGY BENCHMARK REPORT")
    print("=" * 65)

    print(results.to_string(index=False))

    print("\nTotal valid trials:", len(df))


if __name__ == "__main__":
    main()