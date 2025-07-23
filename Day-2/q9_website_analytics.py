monday_visitors = {"user1", "user2", "user3", "user4", "user5"}
tuesday_visitors = {"user2", "user4", "user6", "user7", "user8"}
wednesday_visitors = {"user1", "user3", "user6", "user9", "user10"}

# Total number of unique visitors
unique= len(monday_visitors.union(tuesday_visitors, wednesday_visitors))
print('Unique visitors:',unique)

# Visitors who visited on monday and tuesday
monday_tuesday_overlap = monday_visitors.intersection(tuesday_visitors)
print('Visitors who visited on monday and tuesday: ',monday_tuesday_overlap)

# New visitors on each day
monday_new = monday_visitors
tuesday_new = tuesday_visitors - monday_visitors - wednesday_visitors
wednesday_new = wednesday_visitors - monday_visitors - tuesday_visitors
print('New visitors on Monday:', monday_new)
print('New visitors on Tuesday:', tuesday_new)
print('New visitors on Wednesday:', wednesday_new)

# Visitors who visited on all days
all_days_visitors = monday_visitors.intersection(tuesday_visitors, wednesday_visitors)
print('Visitors who visited on all days:', all_days_visitors)

# Overlap analysis
overlap_analysis = {
    "Monday-Tuesday": monday_visitors.intersection(tuesday_visitors),
    "Monday-Wednesday": monday_visitors.intersection(wednesday_visitors),
    "Tuesday-Wednesday": tuesday_visitors.intersection(wednesday_visitors)
}
print('Overlap analysis:', overlap_analysis)