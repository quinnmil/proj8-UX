"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#Table for speeds and max times
#TABLE = [brevet,(min_speed, max_speed),(max_hr,max_min)]
TABLE = [[200,(15,34),(13,30)], [300,(15,32),(20,00)], [400,(15,32),(27,00)], [600,(15,30),(40,00)], [1000,(11.428,28),(75,00)]]


def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
       brevet_dist_km: number, the nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """

    #Control distance of 0
    if control_dist_km == 0:
      return arrow.get(brevet_start_time).isoformat()

    

    #Control distance is more than brevet distance but less than
    #120% of brevet distance
    if control_dist_km > brevet_dist_km and control_dist_km <= (brevet_dist_km*1.2):
      control_dist_km = brevet_dist_km

    #Reset variables for each calculation
    time = 0
    index = 0

    #Find the proper brevet distance
    for i, dist in enumerate(TABLE):
      if dist[0] == brevet_dist_km:
        index = i

    #Calculate opening time
    while index >= 0:
      calc = 0
      if index == 0:
        time += control_dist_km/TABLE[0][1][1]
        index -= 1
      elif control_dist_km < TABLE[index-1][0]:
        index -= 1
      else:
        calc = control_dist_km - TABLE[index-1][0]
        time += calc/TABLE[index][1][1]
        control_dist_km -= calc
        index -= 1

    #Format hr and min
    min = time%1
    hr = round(time - min)
    min = round(min*60)

    opening = arrow.get(brevet_start_time).replace(hours =+ hr, minutes =+ min)

    return opening.isoformat()


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, the control distance in kilometers
          brevet_dist_km: number, the nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An ISO 8601 format date-time string indicating
           the official start time of the brevet
    Returns:
       An ISO 8601 format date string indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """

    #Control distance of 0
    if control_dist_km == 0:
      return arrow.get(brevet_start_time).replace(hours =+ 1).isoformat()

    #Reset variables
    time = 0
    index = 0

    #Find the proper brevet distance
    for i, dist in enumerate(TABLE):
      if dist[0] == brevet_dist_km:
        index = i

    #Control distance is more than brevet distance but less than
    #120% of brevet distance, get MAX time
    if control_dist_km >= brevet_dist_km and control_dist_km <= (brevet_dist_km*1.2):
      hr = TABLE[index][2][0]
      min = TABLE[index][2][1]
      return arrow.get(brevet_start_time).replace(hours=+hr, minutes=+min).isoformat()

    #Calculate closing time
    while index >= 0:
      calc = 0
      if index == 0:
        time += control_dist_km/TABLE[0][1][0]
        index -= 1
      elif control_dist_km < TABLE[index-1][0]:
        index -= 1
      else:
        calc = control_dist_km - TABLE[index-1][0]
        time += calc/TABLE[index][1][0]
        control_dist_km -= calc
        index -= 1

    #Format hr and min
    min = time%1
    hr = round(time - min)
    min = round(min*60)

    closing = arrow.get(brevet_start_time).replace(hours=+hr, minutes=+min)

    return closing.isoformat()