from nose.tools import raises
from tests.base_unittest import BaseUnitTest
from pypokerengine.api.emulator import Emulator, restore_game_state
from pypokerengine.engine.card import Card
from examples.players.fold_man import PokerPlayer as FoldMan

class EmulatorTest(BaseUnitTest):

    def setUp(self):
        self.emu = Emulator()

    def test_register_and_fetch_player(self):
        p1, p2 = FoldMan(), FoldMan()
        self.emu.register_player("uuid-1", p1)
        self.emu.register_player("uuid-2", p2)
        self.eq(p1, self.emu.fetch_player("uuid-1"))
        self.eq(p2, self.emu.fetch_player("uuid-2"))

    @raises(TypeError)
    def test_register_invalid_player(self):
        self.emu.register_player("uuid", "hoge")

    def test_restore_game_state_two_players_game(self):
        restored = restore_game_state(TwoPlayerSample.round_state)
        table = restored["table"]
        players = restored["table"].seats.players
        self.eq(1, restored["next_player"])
        self.eq(2, restored["street"])
        self.eq(3, restored["round_count"])
        self.eq(5, restored["small_blind_amount"])
        self.eq(0, table.dealer_btn)
        self.eq(['D5', 'D9', 'H6', 'CK'], [str(card) for card in table.get_community_card()])
        self._assert_deck(table.deck, [Card.from_str(s) for s in ['D5', 'D9', 'H6', 'CK']])
        self.eq(2, len(players))
        self._assert_player(["p1", "tojrbxmkuzrarnniosuhct", [], 65, TwoPlayerSample.p1_round_action_histories,\
                TwoPlayerSample.p1_action_histories, 0, 35], players[0])
        self._assert_player(["p2", "pwtwlmfciymjdoljkhagxa", [], 80, TwoPlayerSample.p2_round_action_histories,\
                TwoPlayerSample.p2_action_histories, 0, 20], players[1])

    def test_restore_game_state_three_players_game(self):
        restored = restore_game_state(ThreePlayerGameStateSample.round_state)
        table = restored["table"]
        players = restored["table"].seats.players
        self.eq(0, restored["next_player"])
        self.eq(2, restored["street"])
        self.eq(2, restored["round_count"])
        self.eq(5, restored["small_blind_amount"])
        self.eq(1, table.dealer_btn)
        self.eq(['HJ', 'C8', 'D2', 'H4'], [str(card) for card in table.get_community_card()])
        self._assert_deck(table.deck, [Card.from_str(s) for s in ['HJ', 'C8', 'D2', 'H4']])
        self.eq(3, len(players))
        self._assert_player(["p1", "ruypwwoqwuwdnauiwpefsw", [], 35, ThreePlayerGameStateSample.p1_round_action_histories,\
                ThreePlayerGameStateSample.p1_action_histories, 0, 60], players[0])
        self._assert_player(["p2", "sqmfwdkpcoagzqxpxnmxwm", [], 0, ThreePlayerGameStateSample.p2_round_action_histories,\
                ThreePlayerGameStateSample.p2_action_histories, 1, 50], players[1])
        self._assert_player(["p3", "uxrdiwvctvilasinweqven", [], 85, ThreePlayerGameStateSample.p3_round_action_histories,\
                ThreePlayerGameStateSample.p3_action_histories, 0, 70], players[2])

    def _assert_player(self, expected_data, player):
        self.eq(expected_data[0], player.name)
        self.eq(expected_data[1], player.uuid)
        self.eq(expected_data[2], player.hole_card)
        self.eq(expected_data[3], player.stack)
        self.eq(expected_data[4], player.round_action_histories)
        self.eq(expected_data[5], player.action_histories)
        self.eq(expected_data[6], player.pay_info.status)
        self.eq(expected_data[7], player.pay_info.amount)


    def _assert_deck(self, deck, exclude_cards):
        self.eq(52-len(exclude_cards), deck.size())
        for card in exclude_cards:
            self.assertNotIn(card, deck.deck)

class TwoPlayerSample:
    valid_actions = [{'action': 'fold', 'amount': 0}, {'action': 'call', 'amount': 15}, {'action': 'raise', 'amount': {'max': 80, 'min': 30}}]
    hole_card = ['CA', 'S3']
    round_state = {
            'dealer_btn': 0,
            'round_count': 3,
            'small_blind_amount': 5,
            'next_player': 1,
            'street': 'turn',
            'community_card': ['D5', 'D9', 'H6', 'CK'],
            'pot': {'main': {'amount': 55}, 'side': []},
            'seats': [
                {'stack': 65, 'state': 'participating', 'name': 'p1', 'uuid': 'tojrbxmkuzrarnniosuhct'},
                {'stack': 80, 'state': 'participating', 'name': 'p2', 'uuid': 'pwtwlmfciymjdoljkhagxa'}
                ],
            'action_histories': {
                'preflop': [
                    {'action': 'SMALLBLIND', 'amount': 5, 'add_amount': 5, 'uuid': 'tojrbxmkuzrarnniosuhct'},
                    {'action': 'BIGBLIND', 'amount': 10, 'add_amount': 5, 'uuid': 'pwtwlmfciymjdoljkhagxa'},
                    {'action': 'CALL', 'amount': 10, 'uuid': 'tojrbxmkuzrarnniosuhct', 'paid': 5}
                    ],
                'flop': [
                    {'action': 'RAISE', 'amount': 5, 'add_amount': 5, 'paid': 5, 'uuid': 'tojrbxmkuzrarnniosuhct'},
                    {'action': 'RAISE', 'amount': 10, 'add_amount': 5, 'paid': 10, 'uuid': 'pwtwlmfciymjdoljkhagxa'},
                    {'action': 'CALL', 'amount': 10, 'uuid': 'tojrbxmkuzrarnniosuhct', 'paid': 5}
                    ],
                'turn': [
                    {'action': 'RAISE', 'amount': 15, 'add_amount': 15, 'paid': 15, 'uuid': 'tojrbxmkuzrarnniosuhct'}
                    ]
                }
            }

    p1_action_histories = [
            {'action': 'RAISE', 'amount': 15, 'add_amount': 15, 'paid': 15, 'uuid': 'tojrbxmkuzrarnniosuhct'}
            ]
    p2_action_histories = []
    p1_round_action_histories = [
            [
                {'action': 'SMALLBLIND', 'amount': 5, 'add_amount': 5, 'uuid': 'tojrbxmkuzrarnniosuhct'},
                {'action': 'CALL', 'amount': 10, 'uuid': 'tojrbxmkuzrarnniosuhct', 'paid': 5}
                ],
            [
                {'action': 'RAISE', 'amount': 5, 'add_amount': 5, 'paid': 5, 'uuid': 'tojrbxmkuzrarnniosuhct'},
                {'action': 'CALL', 'amount': 10, 'uuid': 'tojrbxmkuzrarnniosuhct', 'paid': 5}
                ],
            None,
            None
            ]
    p2_round_action_histories = [
            [
                {'action': 'BIGBLIND', 'amount': 10, 'add_amount': 5, 'uuid': 'pwtwlmfciymjdoljkhagxa'}
                ],
            [
                {'action': 'RAISE', 'amount': 10, 'add_amount': 5, 'paid': 10, 'uuid': 'pwtwlmfciymjdoljkhagxa'}
                ],
            None,
            None
            ]
    # player_pay_info = [pay_info.status, pay_info.amount]
    p1_pay_info = [0, 35]
    p2_pay_info = [0, 20]

class ThreePlayerGameStateSample:
    valid_actions = [{'action': 'fold', 'amount': 0}, {'action': 'call', 'amount': 10}, {'action': 'raise', 'amount': {'max': 35, 'min': 20}}]
    hole_card = ['S9', 'C5']
    round_state = {
            'dealer_btn': 1,
            'round_count': 2,
            'next_player': 0,
            'small_blind_amount': 5,
            'action_histories': {
                'turn': [
                    {'action': 'RAISE', 'amount': 10, 'add_amount': 10, 'paid': 10, 'uuid': 'uxrdiwvctvilasinweqven'}
                    ],
                'preflop': [
                    {'action': 'SMALLBLIND', 'amount': 5, 'add_amount': 5, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm'},
                    {'action': 'BIGBLIND', 'amount': 10, 'add_amount': 5, 'uuid': 'uxrdiwvctvilasinweqven'},
                    {'action': 'CALL', 'amount': 10, 'uuid': 'ruypwwoqwuwdnauiwpefsw', 'paid': 10},
                    {'action': 'CALL', 'amount': 10, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm', 'paid': 5}
                    ],
                'flop': [
                    {'action': 'CALL', 'amount': 0, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm', 'paid': 0},
                    {'action': 'CALL', 'amount': 0, 'uuid': 'uxrdiwvctvilasinweqven', 'paid': 0},
                    {'action': 'RAISE', 'amount': 50, 'add_amount': 50, 'paid': 50, 'uuid': 'ruypwwoqwuwdnauiwpefsw'},
                    {'action': 'CALL', 'amount': 40, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm', 'paid': 40},
                    {'action': 'CALL', 'amount': 50, 'uuid': 'uxrdiwvctvilasinweqven', 'paid': 50}
                    ]
                },
            'street': 'turn',
            'seats': [
                {'stack': 35, 'state': 'participating', 'name': 'p1', 'uuid': 'ruypwwoqwuwdnauiwpefsw'},
                {'stack': 0, 'state': 'allin', 'name': 'p2', 'uuid': 'sqmfwdkpcoagzqxpxnmxwm'},
                {'stack': 85, 'state': 'participating', 'name': 'p3', 'uuid': 'uxrdiwvctvilasinweqven'}
                ],
            'community_card': ['HJ', 'C8', 'D2', 'H4'],
            'pot': {'main': {'amount': 150}, 'side': [{'amount': 30, 'eligibles': ["dummy"]}]}
            }
    p1_action_histories = []
    p2_action_histories = []
    p3_action_histories = [{'action': 'RAISE', 'amount': 10, 'add_amount': 10, 'paid': 10, 'uuid': 'uxrdiwvctvilasinweqven'}]
    p1_round_action_histories = [
            [{'action': 'CALL', 'amount': 10, 'uuid': 'ruypwwoqwuwdnauiwpefsw', 'paid': 10}],
            [{'action': 'RAISE', 'amount': 50, 'add_amount': 50, 'paid': 50, 'uuid': 'ruypwwoqwuwdnauiwpefsw'}],
            None,
            None]
    p2_round_action_histories = [
            [
                {'action': 'SMALLBLIND', 'amount': 5, 'add_amount': 5, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm'},
                {'action': 'CALL', 'amount': 10, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm', 'paid': 5}
                ],
            [
                {'action': 'CALL', 'amount': 0, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm', 'paid': 0},
                {'action': 'CALL', 'amount': 40, 'uuid': 'sqmfwdkpcoagzqxpxnmxwm', 'paid': 40}
                ],
            None,
            None]
    p3_round_action_histories = [
            [
                {'action': 'BIGBLIND', 'amount': 10, 'add_amount': 5, 'uuid': 'uxrdiwvctvilasinweqven'}
                ],
            [
                {'action': 'CALL', 'amount': 0, 'uuid': 'uxrdiwvctvilasinweqven', 'paid': 0},
                {'action': 'CALL', 'amount': 50, 'uuid': 'uxrdiwvctvilasinweqven', 'paid': 50}
                ],
            None,
            None]
    # player_pay_info = [pay_info.status, pay_info.amount]
    p1_pay_info = [0, 60]
    p2_pay_info = [1, 50]
    p3_pay_info = [0, 70]

