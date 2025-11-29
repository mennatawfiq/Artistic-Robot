

LETTER_PATHS = {
    "A": [
        (0,50,0), (20,0,1), (40,50,1),    # /\ shape
        (10,25,0), (30,25,1)              # middle bar
    ],

    "B": [
    (0,0,0),      # start top-left, pen up
    (0,50,1),     # left vertical spine

    # --- Bottom curve ---
    (20,50,1),
    (35,40,1),
    (35,30,1),
    (20,25,1),

    # --- Middle horizontal line ---
    (0,25,0),     # pen up: move to left start of the middle bar
    (0,25,1),
    (20,25,1),    # draw middle bar to the right

    # --- Top curve ---
    (20,25,0),    # pen up to move to start of top curve
    (20,25,1),
    (35,20,1),
    (35,10,1),
    (20,0,1),

    (0,0,1)       # close back to top-left
],

    "C": [
    (40,0,0),   # pen up start at top-right
    (10,0,1),   # top horizontal
    (0,10,1),
    (0,40,1),
    (10,50,1),
    (40,50,1)   # bottom horizontal
],

"D": [
    (0,0,0),    # pen up start top-left
    (0,50,1),   # left vertical
    (25,50,1),  # bottom curve start
    (40,35,1),
    (40,15,1),
    (25,0,1),
    (0,0,1)     # back pen up to start
],

"E": [
    (40,0,0),   # pen up start top-right
    (0,0,1),    # top horizontal
    (0,25,1),   # left vertical
    (30,25,1),  # middle horizontal
    (0,25,0),   # pen up move back to left
    (0,50,1),   # left vertical down
    (40,50,1)   # bottom horizontal
],


    # Add the rest later...
}
