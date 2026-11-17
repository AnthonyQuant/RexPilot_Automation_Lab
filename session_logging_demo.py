from rexpilot.session_manager import SessionManager
from rexpilot.balanced_strategy import BalancedStrategy
from rexpilot.performance_logger import PerformanceLogger

def collect_final_score():

    while True:

        score_input = input(
            "\nEnter the final Chrome Dino score "
            "(or press Enter to skip): "
        ).strip()

        if not score_input:
            return None

        try:
            score = int(score_input)

        except ValueError:
            print("Invalid input. Enter a whole number.")
            continue

        if score < 0:
            print("Score cannot be negative.")
            continue

        return score

def main():

    manager = SessionManager()
    logger = PerformanceLogger()

    strategy = BalancedStrategy()

    # Start the session
    session = manager.start_session(strategy)

    print("\nTest session is running.")

    input("Press Enter to simulate the end of gameplay...")

    # Record the actual session end time first
    completed_session = manager.stop_session()

    print("\nSession ended.")
    print(
        f"Recorded gameplay duration: "
        f"{completed_session.get_duration():.2f} seconds"
    )

    # Collect the score after the session has ended
    final_score = collect_final_score()

    completed_session.set_final_score(final_score)

    # Save the completed session
    logger.log_session(completed_session)

    print("\nFinal session summary:")
    print("Strategy:", completed_session.strategy.name)
    print("Final score:", completed_session.final_score)
    print("Session ID:", completed_session.session_id)

if __name__ == "__main__":
    main()
