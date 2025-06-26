def check_event_access(attendee):
    if attendee is None:
        return "Registration not found"

    elif attendee is not None and attendee.has_valid_ticket():
        return "Full event access granted"

    elif attendee is not None and (attendee.category == "VIP" or attendee.category == "Speaker"):
        return "Limited event access granted"

    else:
        return "Access denied"
