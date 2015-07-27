from rest_framework import generics

from api.serializers import ProposalSerializer
from deck.models import Proposal


class ListProposalView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    queryset = Proposal.objects.filter(is_approved=True)

    def get_queryset(self):
        slug = self.kwargs['slug']
        return self.queryset.filter(event__slug=slug)
