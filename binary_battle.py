

# change this to test various sized boards
row_len =  10 
board = [0 for i in range(0, row_len * row_len)]
hit_list = [0 for i in range(0,len(board))]

# mv in the form A1
# convert's to  x, y coords
def to_x_y(mv):
  x = ord(mv[0].upper()) - 65
  y = int(mv[1:len(mv)])
  return [x,y]

def to_one_dim(x, y):
  return x * row_len + y

def mv_to_indx(mv):
  x,y = to_x_y(mv)
  print "x %s y %s " % (x,y)
  return to_one_dim(x,y)

# mv in the form A1
# converts it to a binary string
def mv_to_bin(mv):
  mv_ls = [0 for i in range(0, len(board))]
  indx = mv_to_indx(mv)
  mv_ls[indx] = 1 
  return list_to_bin(mv_ls)

def clean(input_str):
    return str.replace(" ","")

# xs list of 0,1 
# return binary string 
def list_to_bin(xs):
  as_str = ''.join(str(e) for e in xs)
  sz = len(xs)
  fmt = "{:0%sb}" % sz
  bin_rep = fmt.format(int(as_str, 2))
  return bin_rep

# board and mv are bin strings
def check_hit(board, mv):
  a = int(board, base = 2)
  b = int(mv, base = 2)
  return bin(a & b) != '0b0'

def fire_shot(board_bin, mv):
  print "mv is %s " % mv
  mv_bin = mv_to_bin(mv)
  sz = len(board)
  fmt = "{:0%sb}" % sz
  is_hit = check_hit(board_bin, mv_bin)
  return is_hit

def calc_hit_list(hit_list, mv):
  mv_bin = mv_to_bin(mv)
  sz = len(board)
  fmt = "{:0%sb}" % sz
  a = int(hit_list, base = 2)
  b = int(mv_bin, base = 2)
  return bin(a | b)

def play_round(board, mv, hit_list):
  is_hit = fire_shot(board_bin, mv)
  print "is a hit %s" % is_hit
  if is_hit:
    hit_list = calc_hit_list(hit_list, mv)
  return hit_list

def process_input(ship_str):
  ship_list = ship_str.split(",")
  print ship_list
  ship_indices = []
  for s in ship_list:
    print s
    x, y = to_x_y(s)
    print "x is %s y is %s" % (x, y)
    one_dim = to_one_dim(x,y) 
    ship_indices.append(one_dim)
  return ship_indices

if __name__ == '__main__':
  # A1 , B2, C2
  #ship_str = raw_input("input ship: ")
  #ship_indxs = process_input(ship_str)
  #ship_indxs = process_input("A13,A14,A15,B10,B11,B12,B13")
  ship_indxs = process_input("A0,B0")
  print "ship indices %s " % ship_indxs
  for i in ship_indxs:
   board[i] = 1
  print
  print "board: %s " % board
  # test hit
  board_bin = list_to_bin(board)
  hit_list = list_to_bin(hit_list)
  print "bin board %s" % board_bin
  print

  mv = "A1"
  for mv in ["A1", "B1", "A0", "B0", "A2"]:
    print
    hit_list = play_round(board_bin, mv, hit_list)
    print "new hit list %s" % hit_list
    print "board list %s" % board_bin
    # check if hit_list == board if it does
    # then all the ship have been sunk
    fmt_str = "{:0%sb}" % len(board) 
    h = fmt_str.format(int(hit_list, 2))
    b = fmt_str.format(int(board_bin, 2))
    is_game_over = (h == b) 
    if is_game_over:
      print "All the ship have been sunk!"
