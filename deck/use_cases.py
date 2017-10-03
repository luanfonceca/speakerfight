def initialize_event_schedule(event):
    track = event.get_main_track()

    if not track.has_activities():
        proposals_to_schedule = event.filter_not_scheduled_by_slots()

        for order, proposal in enumerate(proposals_to_schedule):
            track.add_proposal_to_slot(proposal, order)

    return True

def rearrange_event_schedule(event, new_activities_arrange):
    raise NotImplementedError
