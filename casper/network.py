"""The network module .... """
from casper.view import View
from casper.plot_tool as PlotTool


class Network:
    """Simulates a network that allows for message passing between validators."""
    def __init__(self, validator_set):
        self.validator_set = validator_set
        self.global_view = View()
        self.plot_tool = PlotTool()

    def propagate_message_to_validator(self, message, validator):
        """Propagate a message to a validator."""
        assert message in self.global_view.messages, ("...expected only to propagate messages "
                                                      "from the global view")
        assert validator in self.validator_set, "...expected a known validator"

        validator.receive_messages(set([message]))

    def get_message_from_validator(self, validator):
        """Get a message from a validator."""
        assert validator in self.validator_set, "...expected a known validator"

        new_message = validator.make_new_message()
        self.global_view.add_messages(set([new_message]))

        return new_message

    def view_initialization(self, view):
        """
        Initalizes all validators with all messages in some view.
        NOTE: This method is not currently tested or called anywhere in repo
        """
        assert isinstance(view, View)
        self.global_view = view.messages

        latest = view.latest_messages

        for validator in latest:
            validator.receive_messages(set([latest[validator]]))

    def random_initialization(self):
        """Generates starting messages for all validators with None as an estiamte."""
        for validator in self.validator_set:
            new_bet = self.get_message_from_validator(validator)
            self.global_view.add_messages(set([new_bet]))

    def report(self, message_colors=None, message_lables=None, edges=None):
        """Displays a view graph."""
        if message_colors is None:
            message_colors = {}
        if message_lables is None:
            message_lables = {}
        if edges is None:
            edges = []


        self.plot_tool.display_viewgraph(
            self.global_view,
            self.validator_set,
            message_colors=message_colors,
            message_lables=message_lables,
            edges=edges
        )
