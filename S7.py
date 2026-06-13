# # Two-level groupby
# multi = chess.groupby(['winner', 'victory_status'])['turns'].mean().round(1)

# # Explore the index:
# multi.index                      # MultiIndex([('Black','Mate'), ('Black','Out of Time'),...])
# multi.index.names                # ['winner', 'victory_status']
# multi.index.get_level_values(0)  # Level 0: ['Black','Black','Black','Draw',...]
# multi.index.get_level_values(1)  # Level 1: ['Mate','Out of Time','Resign','Draw',...]




# # Outer level only — returns a Series with inner level as index
# multi.loc['Black']               # Mate:67.3, Out of Time:70.9, Resign:55.5

# # Specific cell — always use a TUPLE for multi-level loc access
# multi.loc[('Draw', 'Draw')]      # 83.8
# multi.loc[('Black', 'Resign')]   # 55.5

# # Cross-section: select across a specific level
# multi.xs('Mate', level='victory_status')   # all Mate rows: Black:67.3, White:63.8
# multi.xs('Draw', level='winner')           # all Draw-winner rows

# # Swap levels
# multi_swapped = multi.swaplevel()
# multi_swapped.sort_index()  # always sort after swaplevel for clean display




# # Method 1: reset_index() — both levels become columns
# flat = multi.reset_index()
# # flat columns: winner | victory_status | turns

# # Method 2: unstack() — moves one index level to become column headers
# pivot = multi.unstack(level='winner')
# # pivot: rows = victory_status, columns = (turns, Black) | (turns, Draw) | (turns, White)

# # Flatten the MultiIndex column header that unstack() creates:
# pivot.columns = pivot.columns.droplevel(0)  # remove 'turns' parent level
# pivot.columns.name = None                    # remove residual name attribute
# # pivot now has columns: Black | Draw | White

# # Method 3: unstack + fill_value
# pivot_filled = multi.unstack(fill_value=0)  # replace NaN with 0



import pandas as pd

# =========================
# Load CSV file
# =========================

csv_path = "data/raw/chess_games.csv"

chess = pd.read_csv(csv_path)

print("\nCSV loaded successfully")
print(chess.head())
print("\nColumns:")
print(chess.columns)


# =========================
# Two-level groupby
# =========================

multi = chess.groupby(["winner", "victory_status"])["turns"].mean().round(1)

print("\n==============================")
print("Two-level groupby result")
print("==============================")
print(multi)


# =========================
# Explore the MultiIndex
# =========================

print("\n==============================")
print("MultiIndex object")
print("==============================")
print(multi.index)

print("\nIndex level names:")
print(multi.index.names)

print("\nLevel 0 values: winner")
print(multi.index.get_level_values(0))

print("\nLevel 1 values: victory_status")
print(multi.index.get_level_values(1))


# =========================
# Outer level only
# =========================

print("\n==============================")
print("multi.loc['Black']")
print("==============================")
print(multi.loc["Black"])


# =========================
# Specific cell access
# =========================

print("\n==============================")
print("Specific cells using tuple")
print("==============================")

print("Draw + Draw:")
print(multi.loc[("Draw", "Draw")])

print("\nBlack + Resign:")
print(multi.loc[("Black", "Resign")])


# =========================
# Cross-section xs()
# =========================

print("\n==============================")
print("Cross-section: all Mate rows")
print("==============================")
print(multi.xs("Mate", level="victory_status"))

print("\n==============================")
print("Cross-section: Draw winner rows")
print("==============================")
print(multi.xs("Draw", level="winner"))


# =========================
# Swap levels
# =========================

multi_swapped = multi.swaplevel()
multi_swapped_sorted = multi_swapped.sort_index()

print("\n==============================")
print("Swapped levels + sorted")
print("==============================")
print(multi_swapped_sorted)


# =========================
# Method 1: reset_index()
# =========================

flat = multi.reset_index()

print("\n==============================")
print("Flat table using reset_index()")
print("==============================")
print(flat)

print("\nFlat columns:")
print(flat.columns)


# =========================
# Method 2: unstack()
# =========================

pivot = multi.unstack(level="winner")

print("\n==============================")
print("Pivot table using unstack(level='winner')")
print("==============================")
print(pivot)

print("\nPivot columns before cleanup:")
print(pivot.columns)


# =========================
# Optional cleanup for columns
# =========================
# In this case, because multi is a Series, columns may NOT have parent level 'turns'.
# So we only drop level if the columns are MultiIndex.

if isinstance(pivot.columns, pd.MultiIndex):
    pivot.columns = pivot.columns.droplevel(0)

pivot.columns.name = None

print("\n==============================")
print("Pivot table after column cleanup")
print("==============================")
print(pivot)

print("\nPivot columns after cleanup:")
print(pivot.columns)


# =========================
# Method 3: unstack + fill_value
# =========================

pivot_filled = multi.unstack(fill_value=0)

print("\n==============================")
print("Pivot table with fill_value=0")
print("==============================")
print(pivot_filled)


# =========================
# Save outputs optionally
# =========================

flat.to_csv("multi_groupby_flat.csv", index=False)
pivot.to_csv("multi_groupby_pivot.csv")
pivot_filled.to_csv("multi_groupby_pivot_filled.csv")

print("\nFiles saved:")
print("multi_groupby_flat.csv")
print("multi_groupby_pivot.csv")
print("multi_groupby_pivot_filled.csv")