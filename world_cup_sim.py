import random


def make_group_stage_fixtures(teams: list[str]):
    
    if len(teams) != 3:
        raise ValueError("Three teams are expected")
    fixture = {
        "Game 1": [teams[0], teams[1]],
        "Game 2": [teams[1], teams[2]],
        "Game 3": [teams[2], teams[0]]
    }
    return fixture


# Team performance attributes-
team_stats = {
    "morale": 50,
    "injuries": 0,
    "strength": 50
}
# Pre-tournament preparation phase
def tournament_preparation():
    print("\n=== PRE-TOURNAMENT STAGE ===")
    
    is_preparation_complete = False
    while not is_preparation_complete:
        print(f"\nCurrent Team Status:")
        print(f"Morale: {team_stats['morale']}, Injuries: {team_stats['injuries']}, Strength: {team_stats['strength']}")
        
        print("\nPreparation Options:")
        print("1. Training Session")
        print("2. Friendly Match")
        print("3. Recovery Session")
        print("4. Finish Preparation")
        
        choice = ""
        while choice not in ("1","2","3","4"):
            choice = input("Choose a valid option (1-4): ")
        
        if choice == "1":
            # Training increases strength
            strength_increase = random.randint(5, 10)
            morale_increase = random.randint(3,6)
            team_stats["strength"] += strength_increase
            team_stats["morale"] += morale_increase
            print(f"Training completed! Strength +{strength_increase}, Morale +{morale_increase}")
            
            # Check for injuries after training
            new_injuries = int(input("Any injuries from training? (0-2): "))
            team_stats["injuries"] += new_injuries
            
            # Ask for recoveries if injuries > 0
            if team_stats["injuries"] > 0:
                recoveries = int(input(f"Any recoveries? (0-{team_stats['injuries']}): "))
                team_stats["injuries"] = max(0, team_stats["injuries"] - recoveries)
                print(f"Recovered {recoveries} injuries. Current injuries: {team_stats['injuries']}")
                
            if team_stats["injuries"] > 5:
                print("Too many injuries! Team won't make it. Therefore Eliminated..")
                break
        elif choice == "2":
            # Friendly match affects morale and injuries
            result = input("Did you win the friendly? (y/n): ").lower()
            if result == "y":
                morale_increase = random.randint(5, 10)
                team_stats["morale"] += morale_increase
                print(f"Friendly win! Morale +{morale_increase}")
            else:
                morale_decr = random.randint(2, 7)
                team_stats["morale"] -= morale_decr
                print(f"Friendly loss! Morale -{morale_decr}")
                
            # Check for injuries after friendly
            new_injuries = int(input("Any injuries from friendly?: "))
            team_stats["injuries"] += new_injuries
            
            # Ask for recoveries if injuries > 0
            if team_stats["injuries"] > 0:
                recoveries = int(input(f"Any recoveries? (0-{team_stats['injuries']}): "))
                team_stats["injuries"] = max(0, team_stats["injuries"] - recoveries)
                print(f"Recovered {recoveries} injuries. Current injuries: {team_stats['injuries']}")
                
            if team_stats["injuries"] > 5:
                print("Too many injuries! Team eliminated.")
                break
        elif choice == "3":
            # Recovery reduces injuries
            team_stats["injuries"] = max(0, team_stats["injuries"] - 2)
            rand_incr = random.randint(2,5)
            team_stats["morale"] += rand_incr
            print(f"Recovery completed! Injuries reduced, Morale +{rand_incr}")
        elif choice == "4":
            is_preparation_complete = True
            print("Preparation phase complete!")


# Group stage simulation
def group_stage_simulation(teams: list[str], team_name: str):
    print("\n=== GROUP STAGES ===")
    
    points = {team: 0 for team in teams}
    fixture = make_group_stage_fixtures(teams)
    
    for match_key, (home_team, away_team) in fixture.items():
        print(f"\n{match_key}: {home_team} vs {away_team}")
        
        home_goals = int(input(f"Goals scored by {home_team}: "))
        away_goals = int(input(f"Goals scored by {away_team}: "))
        
        if home_team == team_name:
            if team_stats["strength"] >= 60:
                home_goals += 1
            if team_stats["morale"] < 30:
                home_goals = max(0, home_goals - 1)
        elif away_team == team_name:
            if team_stats["strength"] >= 60:
                away_goals += 1
            if team_stats["morale"] < 30:
                away_goals = max(0, away_goals - 1)
        
        if home_goals > away_goals:
            points[home_team] += 3
            print(f"{home_team} wins!")
        elif away_goals > home_goals:
            points[away_team] += 3
            print(f"{away_team} wins!")
        else:
            points[home_team] += 1
            points[away_team] += 1
            print("It's a tie!")
        
        if team_name in (home_team, away_team):
            if team_stats["injuries"] >= 5:
                print(f"{team_name}: Critical injuries! Match forfeited.")
                break
        
        if team_name in (home_team, away_team):
            new_injuries = int(input(f"Any injuries for {team_name} in this match?: "))
            team_stats["injuries"] += new_injuries
            if team_stats["injuries"] > 0:
                recoveries = int(input(f"Any recoveries for {team_name}? (0-{team_stats['injuries']}): "))
                team_stats["injuries"] = max(0, team_stats["injuries"] - recoveries)
                print(f"Recovered {recoveries} injuries. Current injuries: {team_stats['injuries']}")
    return points


def knockout_stages(team_name):
    print(f"\n=== KNOCKOUT STAGES ({team_name}) ===")
    
    stages = ["Round-of-16", "Quarter-final", "Semi-final", "Final"]
    current_stage = 0
    tournament_won = False
    
    morale_increase, strength_increase = 0, 0
    while current_stage < len(stages):
        cur_stage = " ".join(stages[current_stage].split('-'))
        print(f"\n--- {cur_stage} ---")
        
        # Check if team can progress
        if team_stats["morale"] < 20:
            print(f"{team_name}: Morale too low! Team eliminated.")
            break
        result = input(f"Result for {team_name} in {cur_stage}? (w/l): ").lower()
        if result == "w":
            morale_increase = random.randint(10,15)
            strength_increase = random.randint(3,6)
            team_stats["morale"] += morale_increase
            team_stats["strength"] += strength_increase
            print(f"{team_name} wins! Morale +{morale_increase}, Strength +{strength_increase}")
        elif result == "l":
            print(f"{team_name} loses! Team eliminated.")
            break
        else:
            print("Invalid result, match replayed.")
            continue
        
        # Check for injuries after knockout match
        new_injuries = int(input("Any injuries from this match?: "))
        team_stats["injuries"] += new_injuries
        
        # Ask for recoveries if injuries > 0
        if team_stats["injuries"] > 0:
            recoveries = int(input(f"Any recoveries for {team_name}? (0-{team_stats['injuries']}): "))
            team_stats["injuries"] = max(0, team_stats["injuries"] - recoveries)
            print(f"Recovered {recoveries} injuries. Current injuries: {team_stats['injuries']}")
        
        if team_stats["injuries"] > 5:
            print("Too many injuries! Team eliminated from tournament.")
            break
        
        # Advance to next stage
        current_stage += 1
        if current_stage == len(stages):
            tournament_won = True
            break
    return tournament_won


# Main tournament simulation
def run_tournament_simulation():
    print("=== 2026 FIFA WORLD CUP SIMULATION ===")
    
    # Pre-tournament (friendlies and training)
    tournament_preparation()
    
    # Enter group stage teams after preparation
    print("\n=== ENTER GROUP STAGE TEAMS ===")
    teams = [
        input("Team 1: ").strip(),
        input("Team 2: ").strip(),
        input("Team 3: ").strip()
    ]
    team_name = input("Which team are you managing? ").strip()
    if team_name not in teams:
        raise ValueError("Selected team must be one of the 3 entered teams")
    
    # Group stage
    points = group_stage_simulation(teams, team_name)
    sorted_standings = sorted(points.items(), key=lambda x: x[1], reverse=True)
    
    print(f"\nGroup Standings:")
    rk = 0
    for rank, (team, pts) in enumerate(sorted_standings, 1):
        if team == team_name:
            rk = rank - 1
        print(f"  {rank}. {team}: {pts} pts")
    
    # Check qualification if team is the last
    if rk == len(teams) - 1: 
        print(f"{team_name} failed to qualify for knockout stages!")
        return
    
    # Knockout stages
    if knockout_stages(team_name):
        print(f"\nCONGRATS! {team_name.upper()} HAS WON THE WORLD CUP!")
    else:
        print(f"\n{team_name} eliminated from tournament.")


if __name__ == "__main__":
    run_tournament_simulation()