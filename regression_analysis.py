
import pandas as pd

from pathlib import Path
from sklearn.linear_model import LinearRegression


def load_benchmark_data():

    file_path = Path(__file__).parent / "benchmark_test.csv"

    if not file_path.exists():
        raise FileNotFoundError("Benchmark CSV was not found.")

    df = pd.read_csv(file_path)

    required_columns = {
        "jump_duration",
        "duck_duration",
        "final_score"
    }

    if not required_columns.issubset(df.columns):
        raise ValueError("Required regression columns are missing.")

    for column in required_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    df = df.dropna(
        subset=list(required_columns)
    ).copy()

    if len(df) < 3:
        raise ValueError("At least three valid records are required.")

    return df


def perform_regression(df, feature):

    X = df[[feature]]
    y = df["final_score"]

    if X[feature].nunique() < 2:
        print(f"\nInsufficient variation in {feature}.")
        return

    model = LinearRegression()

    model.fit(X, y)

    predictions = model.predict(X)

    r_squared = model.score(X, y)

    print(f"\nRegression: {feature} versus final score")
    print("-" * 50)

    print("Observations:", len(df))
    print("Coefficient:", round(model.coef_[0], 4))
    print("Intercept:", round(model.intercept_, 4))
    print("R-squared:", round(r_squared, 4))

    print("\nActual versus predicted scores:")

    for actual, predicted in zip(y, predictions):
        print(
            f"Actual: {actual:.2f} | "
            f"Predicted: {predicted:.2f}"
        )


def main():

    df = load_benchmark_data()

    print("REXPILOT REGRESSION ANALYSIS")
    print("=" * 50)

    perform_regression(df, "jump_duration")

    perform_regression(df, "duck_duration")

    print("\nRegression analysis completed.")


if __name__ == "__main__":
    main()
