def analyze_attendees(attendees):
    total = len(attendees)
    checked = sum(bool(a.checked_in) for a in attendees)
    sources = {}
    categories = {}
    for a in attendees:
        sources[a.source] = sources.get(a.source, 0) + 1
        categories[a.category] = categories.get(a.category, 0) + 1
    rate = round((checked / total) * 100, 1) if total else 0
    insights = []
    if total == 0:
        insights.append("No attendee registrations are available yet.")
    else:
        if rate < 70: insights.append(f"Check-in rate is {rate}%; monitor arrival flow and registration queues.")
        else: insights.append(f"Check-in performance is healthy at {rate}%.")
        if categories:
            top = max(categories, key=categories.get)
            insights.append(f"Largest attendee segment: {top} ({categories[top]} registrations).")
        if len(sources) > 1:
            insights.append("Registrations are coming from multiple sources; unified tracking is active.")
    return {"total": total, "checked_in": checked, "pending": total-checked, "check_in_rate": rate, "sources": sources, "categories": categories, "insights": insights}
