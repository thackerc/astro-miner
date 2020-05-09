import math

def calculate_optimal_mining_time(units):
    '''A function to calculate the optimal number of days to mine an asteroid.

    Constraints:
        - Mine the asteroid as quickly as possible
        - Start with a single robot
        - A robot can mine one unit of ore in one day
        - A robot can build another robot in two days
        - For each day each robot can be tasked with mining OR building OR resting
        - Robots can’t collaborate to reduce the time it takes to build another robot

    Assumptions:
        - All bot building happens before any mining, it's just more efficient.
        - All bots are either mining together or building together. There is no efficiency gain to divide up.
        - A bot would only rest on the last day in the case that there is not enough ore to mine.
        - Building bots is expensive, don't build more bots than you need, BUT...
        - if mining is going to take more than 5 days you need more bots.

        5 Days:
        This assumption is born out of a pattern shown below. Each column (A, B, C) shows a scenario for how to build bots and 
        then mine all units. These examples below show the most simple case where it is more efficient to spend 2 more days 
        building more bots. More complex cases are simply multiples of this case, i.e., instead of considering 1 or 2 bots, a 
        more complex case would look at 2 vs. 4 bots, 16 vs. 32 bots, etc. The number of bots will always be a power of 2.

         5 units            6 units
        ---------------    ---------------
           A  B   C           A  B   C
        ---------------    ---------------
        1  m  b   b        1  m  b   b
        2  m  b   b        2  m  b   b
        3  m  mm  bb       3  m  mm  bb
        4  m  mm  bb       4  m  mm  bb
        5  m  m-  mmmm     5  m  mm  mmmm
        6         m---     6  m      mm--

        b = build, m = mine, - = rest

        Notice that it is not more efficient to build any bot until there are more than 5 units to be mined or, more importantly, 
        mining takes more that 5 days. This pattern repeats ad infinitum.
    '''

    # A build_session is a two day block when all bots are building another bot
    # Mining should take a most 5 days.
    # units / 5 tells us how many units per day we need to mine.
    # The log2 accounts for exponential increase in bots built per build_session.
    # log2(units/5) is roughly the number of build_sessions we need to create enough bots to meet our mining quota within 5 days
    # ceiling effectively prevents partial sessions.
    # build_sessions = max(build_sessions, 0) keeps build_sessions non-negative.
    build_sessions = max(math.ceil(math.log(units / 5, 2)), 0)

    # Each build session lasts two days.
    build_days = build_sessions * 2

    # because the bots all do the same task at the same time bot creation is exponential
    bots = 2 ** build_sessions

    # The ceiling accounts for the fact that there may be some bots resting on the last day because there isn't enough ore to mine.
    mining_days = math.ceil(units / bots)

    return build_days + mining_days


if __name__ == '__main__':

    test_count = int(input())
    for i in range(test_count):
        units, expected = map(int,input().split())
        total_days = calculate_optimal_mining_time(units)
        print(f'{units} units => {total_days} days [{expected} day expected]')

