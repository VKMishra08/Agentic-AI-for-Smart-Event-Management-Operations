def recommend_venues(venues, attendees, equipment=None):
    equipment = [x.strip().lower() for x in (equipment or [])]
    results=[]
    for v in venues:
        if v.status == "Booked" or v.capacity < attendees: continue
        have=[x.strip().lower() for x in (v.equipment or "").split(",")]
        matched=sum(x in have for x in equipment)
        fit=round(attendees/v.capacity*100,1)
        score=matched*100-fit-v.utilization*0.25
        results.append({"venue": v.name,"capacity":v.capacity,"location":v.location,"matched_equipment":matched,"capacity_fit":fit,"score":round(score,1)})
    return sorted(results,key=lambda x:x["score"],reverse=True)
