from engine import PokerEngine


def main():
    print("Interactive poker simulation")
    rounds = input("Please enter the number of hands to simulate (default is 3): ").strip()
    if not rounds:
        rounds = 3
    else:
        try:
            rounds = int(rounds)
        except ValueError:
            print("Invalid input. Using default of 3 hands.")
            rounds = 3
    print("Enter player names separated by commas, or press Enter for the default names.")
    raw_names = input("Players: ").strip()
    if raw_names:
        player_names = [name.strip() for name in raw_names.split(",") if name.strip()]
    else:
        player_names = ["Alice", "Bob"]

    engine = PokerEngine(player_names, starting_chips=1000, ante=10)

    for hand_number in range(1, rounds+1):
        print(f"\n=== Hand {hand_number} ===")
        result = engine.play_hand()

        print("Community cards:")
        for card in result["community_cards"]:
            print(f"  - {card}")

        print("Pot:", result["pot"])
        print("Winners:", [player.name for player in result["winners"]])
        print("Chip counts:")
        for player in result["players"]:
            print(f"  - {player.name}: {player.chips}")

        if hand_number < 3:
            try:
                input("Press Enter to start the next hand...")
            except EOFError:
                print("No input received; continuing to the next hand.")

    print("\nSimulation complete.")


if __name__ == "__main__":
    main()

