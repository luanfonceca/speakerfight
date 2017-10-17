from deck.exceptions import EmptyActivitiesArrangementException


def initialize_event_schedule(event):
    track = event.get_main_track()

    if not track.has_activities():
        proposals_to_schedule = event.filter_not_scheduled_by_slots()

        for order, proposal in enumerate(proposals_to_schedule):
            track.add_proposal_to_slot(proposal, order)

    return True

def rearrange_event_schedule(event, new_activities_arrangement):
    if not new_activities_arrangement:
        raise EmptyActivitiesArrangementException

    track = event.get_main_track()
    track.refresh_track()

    for order, activity in enumerate(new_activities_arrangement):
        track.add_activity_to_slot(activity, order)

    return new_activities_arrangement
