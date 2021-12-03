def transition_month(Month):
    for Month in data:
        if data["Month"][Month] == "Jan":
            data["Month"][Month] = 0
        elif data["Month"][Month] == "Feb":
            data["Month"][Month] = 1
        elif data["Month"][Month] == "Mar":                    
            data["Month"][Month] = 2
        elif data["Month"][Month] == "Apr":
            data["Month"][Month] = 3
        elif data["Month"][Month] == "May":
            data["Month"][Month] = 4                
        elif data["Month"][Month] == "Jun":
            data["Month"][Month] = 5
        elif data["Month"][Month] == "Jul":
            data["Month"][Month] = 6
        elif data["Month"][Month] == "Aug":
            data["Month"][Month] = 7
        elif data["Month"][Month] == "Sep":
            data["Month"][Month] = 8
        elif data["Month"][Month] == "Oct":
            data["Month"][Month] = 9
        elif data["Month"][Month] == "Nov":
            data["Month"][Month] = 10
        elif data["Month"][Month] == "Dec":
            data["Month"][Month] = 11
