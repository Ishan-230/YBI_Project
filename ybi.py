import pandas as pd

# Sample election data
data = {
    'Constituency': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D'],
    'Party': ['Party X', 'Party Y', 'Party X', 'Party Z', 'Party Y', 'Party Z', 'Party X', 'Party Y'],
    'Candidate': ['Alice', 'Bob', 'Charlie', 'David', 'Eve', 'Frank', 'Grace', 'Hank'],
    'Votes': [12000, 11000, 15000, 14000, 13000, 13500, 16000, 14500]
}

df = pd.DataFrame(data)

# Calculate total votes per party
total_votes_per_party = df.groupby('Party')['Votes'].sum()

# Function to get the winning party in each constituency
def get_winning_party(group):
    return group.loc[group['Votes'].idxmax(), 'Party']

df['Winning Party'] = df.groupby('Constituency').apply(get_winning_party).reset_index(level=0, drop=True)

# Determine the overall election winner
overall_winner = total_votes_per_party.idxmax()

total_votes = df['Votes'].sum()

# Calculate vote share percentage
df['Vote Share (%)'] = (df['Votes'] / total_votes) * 100

# Function to identify close contests
def close_contest(group):
    sorted_group = group.sort_values(by='Votes', ascending=False)
    if len(sorted_group) > 1:
        margin = (sorted_group.iloc[0]['Votes'] - sorted_group.iloc[1]['Votes']) / sorted_group.iloc[0]['Votes'] * 100
        return margin < 12  # Checking if margin is less than 12%
    return False  # Return False instead of None for single-candidate constituencies

# Apply function and fill NaN values
df['Close Contest'] = df.groupby('Constituency').apply(close_contest).reset_index(level=0, drop=True).fillna(False)

# Ensure boolean type
df['Close Contest'] = df['Close Contest'].astype(bool)

# Display results
print("Total Votes Per Party:")
print(total_votes_per_party)
print("\nWinning Party in Each Constituency:")
print(df[['Constituency', 'Winning Party']].drop_duplicates())
print("\nOverall Election Winner:", overall_winner)
print("\nVote Share Percentage:")
print(df[['Candidate', 'Party', 'Vote Share (%)']])
print("\nClose Contests:")
print(df[df['Close Contest']][['Constituency', 'Candidate', 'Party', 'Votes']])
