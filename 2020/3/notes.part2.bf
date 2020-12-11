# Solve AoC 2020 day 2 part 2 using BF

# Variables
#  GH GL is 16 bit counter for good passwords
#  RUN is loop condition for processing lines
#  IN is used to read input
#  TMP is a temporary variable zeroed before not after
#  A is the first target character index
#  B is the second target character index
#  C is the target character
#  S is the invalid bit for a password hence good if zero
#  GO is the loop condition for processing chars in a password
#  X Y Z are temporary variables

# ASCII Used
# newline 10
# space 32
# dash 45

# Memory layout
# Backstops (0 1) used where necessary or just suspected to be useful
# (GH GL) (0 1) (RUN) (IN) (0 1) (TMP) (A) (B) (C) (D) (S) (GO) (X) (Y) (Z) (0 1)
# Initialize backstops
     >   >  >+ >     >    >  >+ >     >   >   >   >   >   >    >   >   >   >  >+
     <   <  <  <     <    <  <  <     <   <   <   <   <   <    <   <   <   <  <

# RUN = 1
# while RUN:
>>>>+[

  ## A = read integer until dash
  # A = 0
  >>>>>[-]
  # IN = 1
  <<<<[-]+
  # while IN:
  [
    # IN = read()
    ,
    # SUB IN dashchar
    ---------------------------------------------
    # if IN is not DASH then roll next digit into A
    [
      # Adjust from dash relative to zero relative
      # Was dash relative subtract 3 to parse an int digit
      ---
      # A *= 10 using TMP
      >>>>[-<++>]<[->+++++<] 
      # IN to A and TMP
      # This will zero IN so that loop terminates
      # as well as adding the next place into A
      <<<<[->>>>+<+<<<]
    ]
    # IN is now zero but TMP is not if we should continue
    # Copy only the truth value of TMP back to IN for loop condition
    >>>[[-]<<<+]
  ]


  ## B = read integer until space
  # B = 0
  >>>>>>[-]
  # IN = 1
  <<<<<[-]+
  # while IN:
  [
    # IN = read()
    ,
    # SUB IN space
    --------------------------------
    # if IN is not DASH then roll next digit into B
    [
      # Adjust from dash relative to zero relative
      # Was space relative subtract 16 to parse an int digit
      ----------------
      # B *= 10 using TMP
      >>>>>[-<<++>>]<<[->>+++++<<] 
      # IN to B and TMP
      # This will zero IN so that loop terminates
      # as well as adding the next place into B
      <<<<<[->>>>>+<<+<<<]
    ]
    # IN is now zero but TMP is not if we should continue
    # Copy only the truth value of TMP back to IN for loop condition
    >>>[[-]<<<+]
  ]

  # C = read()
  >>>>>>,
  
  # read() read() to clear colon and space
  ,,

  # S = 1
  >>[-]+

  # GO = 1
  >[-]+

  # while GO:
  [
    # --A
    <<<<<-

    # --B
    >-

    # D = read()
    >>,

    # if d==c:
    # x = 0
    # d -> x, y
    # y -> d
    # c -> -x, y
    # y -> c
    # 
      if !a: s -= 1
      if !b: s -= 1
  
    if d=='\n':
      go = 0
    if !d:
      run = 0
  
   if !s: good += 1 

]
  
print good
